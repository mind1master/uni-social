# -*- coding: utf-8 -*-
from django.views.generic.base import TemplateView
from django.views.generic import DetailView
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.contrib.auth.views import login

from social.apps.core.models import SocialProfile, AnyPost


class HomeView(TemplateView):
    template_name = 'core/home.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('profile_page', kwargs={'pk': request.user.pk}))
        return None


class ProfileView(DetailView):
    template_name = 'core/profile.html'
    model = SocialProfile

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        wallposts = self.object.get_wallposts_received()
        context['wallposts'] = wallposts
        return context

def custom_login(request, **kwargs):
    if request.user.is_authenticated():
        return redirect('/', **kwargs)
    else:
        return login(request, **kwargs)
