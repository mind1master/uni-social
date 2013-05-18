# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class SocialProfile(models.Model):
    user = models.OneToOneField(User)

    date_of_birth = models.DateField(null=True)
    home_town = models.CharField(max_length=20, blank=True)
    phone_number = models.CharField(max_length=10, blank=True)
    skype_id = models.CharField(max_length=20, blank=True)

    def get_wallposts_received(self):
        return AnyPost.objects.filter(receiver=self, post_type=AnyPost.WALL).order_by('-timestamp')

class AnyPost(models.Model):
    MESSAGE = 'message'
    WALL = 'wall'
    POST_TYPES = (
        (MESSAGE, 'Message'),
        (WALL, 'Wall'),
    )

    sender = models.ForeignKey(User, related_name='posts_sent')
    receiver = models.ForeignKey(User, related_name='posts_received')
    text = models.TextField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)
    post_type = models.CharField(max_length=50, choices=POST_TYPES, default=MESSAGE)