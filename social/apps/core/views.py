# -*- coding: utf-8 -*-
from django.views.generic.base import TemplateView
from django.views.generic import DetailView, ListView
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.contrib.auth.views import login
from django.views.decorators.http import require_POST
from django.http import HttpResponseForbidden

from social.apps.core.models import SocialProfile, AnyPost
from social.apps.core.forms import WallPostForm, ProfileForm



class HomeView(TemplateView):
    template_name = 'core/home.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('profile_page', kwargs={'pk': request.user.pk}))
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


class ProfileEditView(DetailView, FormMixin):
    template_name = 'core/profile_edit.html'
    model = SocialProfile
    form_class = ProfileForm

    def get_success_url(self):
        return reverse('profile_page', kwargs={'pk': self.get_object().pk})

    def get_context_data(self, **kwargs):
        context = super(ProfileEditView, self).get_context_data(**kwargs)
        form = ProfileForm(
            instance=self.request.user.get_profile(),
            initial={
                'name': self.request.user.first_name,
                'last_name': self.request.user.last_name,
            }
        )
        context['form'] = form

        return context

    def dispatch(self, request, *args, **kwargs):
        if not int(kwargs['pk']) == request.user.pk:
            return redirect(reverse('profile_page', kwargs={'pk': self.get_object().pk}))

        return super(ProfileEditView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=False)
            user = request.user
            user.first_name = form.cleaned_data['name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class FriendsView(ListView):
    template_name = 'core/friends_list.html'
    model = SocialProfile
    context_object_name = 'friends'

    def get_context_data(self, **kwargs):
        context = super(FriendsView, self).get_context_data(**kwargs)
        context['friends'] = self.request.user.get_profile().friends.all
        return context


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