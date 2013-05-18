# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class SocialProfile(models.Model):
    user = models.OneToOneField(User)

    date_of_birth = models.DateField(null=True)
    home_town = models.CharField(max_length=20, blank=True)
    phone_number = models.CharField(max_length=10, blank=True)
    skype_id = models.CharField(max_length=20, blank=True)
