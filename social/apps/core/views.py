# -*- coding: utf-8 -*-
from django.views.generic.base import TemplateView
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.contrib.auth.views import login
from django.http import HttpResponseForbidden

from social.apps.core.models import SocialProfile, AnyPost
from social.apps.core.forms import WallPostForm

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
            form.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

def custom_login(request, **kwargs):
    if request.user.is_authenticated():
        return redirect('/', **kwargs)
    else:
        return login(request, **kwargs)
