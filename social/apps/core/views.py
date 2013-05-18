# -*- coding: utf-8 -*-
from django.views.generic.base import TemplateView
from django.views.generic import DetailView

from social.apps.core.models import SocialProfile, AnyPost


class HomeView(TemplateView):
    template_name = 'core/home.html'


class ProfileView(DetailView):
    template_name = 'core/profile.html'
    model = SocialProfile

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        wallposts = self.object.get_wallposts_received()
        context['wallposts'] = wallposts
        return context
class LoginView(TemplateView):
    template_name = 'core/login.html'

