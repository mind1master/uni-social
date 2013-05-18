# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class SocialUser(AbstractBaseUser):
    first_name = models.CharField(max_length=20, required=True)
    last_name = models.CharField(max_length=20)
    date_of_birth = models.DateField()

    home_town = models.CharField(max_length=20)

    phone_number = models.CharField(max_length=10)
    skype_id = models.CharField(max_length=20)
