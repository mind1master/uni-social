# -*- coding: utf-8 -*-
from annoying.decorators import render_to
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormMixin
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render
from django.contrib.auth.views import login
from django.views.decorators.http import require_POST
from django.http import HttpResponseForbidden, Http404, HttpResponse

from social.apps.core.models import SocialProfile, AnyPost
from social.apps.core.forms import WallPostForm, MessageForm
from django.db.models import Q
from social.apps.core.forms import ProfileForm, UserForm
from django.contrib.auth import authenticate, login as log_in
from django.contrib.auth.forms import UserCreationForm


class HomeView(TemplateView):
    template_name = 'core/home.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('profile_page', kwargs={'pk': request.user.get_profile().pk}))
        return None


class ProfileView(DetailView, FormMixin):
    template_name = 'core/profile.html'
    model = SocialProfile
    form_class = WallPostForm

    def get_success_url(self):
        return reverse('profile_page', kwargs={'pk': self.get_object().pk})

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context['form'] = form

        wallposts = self.object.get_wallposts_received()
        context['wallposts'] = wallposts
        return context

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            post = form.save(commit=False)
            post.receiver = self.get_object().user
            post.sender = request.user
            post.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


def profile_edit(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.get_profile())
        if form.is_valid():
            form.save()

            request.user.first_name = form.cleaned_data['name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.save()

            return redirect(reverse('profile_page', kwargs={'pk': request.user.get_profile().pk}))
        else:
            return render(request, 'core/profile_edit.html', {'form': form})

    form = ProfileForm(
        instance=request.user.get_profile(),
        initial={
            'name': request.user.first_name,
            'last_name': request.user.last_name,
            }
    )
    return render(request, 'core/profile_edit.html', {'form': form})


def register_user(request):
    if request.user.is_authenticated and not request.user.is_anonymous:
        return redirect(reverse('profile_page', kwargs={'pk': request.user.get_profile().pk}))
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            SocialProfile.objects.create(user=user)
            user.first_name = user.username
            user.save()

            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            if user:
                log_in(request, user)
            return redirect(reverse('profile_edit_page'))
        else:
            return render(request, 'core/register.html', {'form': form})

    form = UserCreationForm()
    return render(request, 'core/register.html', {'form': form})



class FriendsView(ListView):
    template_name = 'core/friends_list.html'
    model = SocialProfile
    context_object_name = 'friends'

    def get_context_data(self, **kwargs):
        context = super(FriendsView, self).get_context_data(**kwargs)
        context['friends'] = self.request.user.get_profile().friends.all
        return context

@login_required
@render_to('core/messages_list.html')
def messages_list(request):
    messages = AnyPost.objects.filter(
        post_type=AnyPost.MESSAGE,
    )
    messages = messages.filter(
        Q(receiver=request.user) |
        Q(sender=request.user)
    ).order_by('seen', '-timestamp')
    messages.filter(receiver=request.user).update(seen=True)
    return {
        'messages': messages[:50],
    }

@login_required
@render_to('core/message_write.html')
def message_write(request, pk):
    friend = User.objects.get(pk=pk)

    if not friend.get_profile() in request.user.get_profile().friends.all():
        raise Http404

    form = MessageForm(request.POST or None)
    if form.is_valid():
        message = form.save(commit=False)
        message.receiver = friend
        message.sender = request.user
        message.save()
        return redirect(reverse('messages_page'))

    return {
        'form': form,
        'friend': friend,
    }

@login_required
@render_to('core/search_friends.html')
def search_friends(request):
    found = None
    q = request.GET.get('q', None)
    if q:
        found = User.objects.filter(
            Q(first_name__icontains=q) |
            Q(last_name__icontains=q)
        ).order_by('first_name').exclude(pk=request.user.pk)[:10]

    return {
        'found': found,
        'q': q,
    }

def custom_login(request, **kwargs):
    if request.user.is_authenticated():
        return redirect('/', **kwargs)
    else:
        return login(request, **kwargs)


@require_POST
def friends_manipulation(request):
    if request.POST.get('add'):
        #Adding a friend
        request.user.get_profile().friends.add(SocialProfile.objects.get(pk=request.POST["pk"]))
        return redirect(reverse('home_page'))

    if request.POST.get('remove'):
        #Adding a friend
        request.user.get_profile().friends.remove(SocialProfile.objects.get(pk=request.POST["pk"]))
        return redirect(reverse('home_page'))

@csrf_exempt
@require_POST
def check_messages(request):
    if request.POST.get('user_pk'):
        user = User.objects.get(pk=request.POST.get('user_pk'))
        return HttpResponse(user.get_profile().get_new_messages_count())
    raise HttpResponseForbidden
