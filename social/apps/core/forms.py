# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm, HiddenInput, ModelChoiceField, CharField
from django.contrib.auth.models import User

from social.apps.core.models import AnyPost, SocialProfile


# Create the form class.
class WallPostForm(ModelForm):
    sender = ModelChoiceField(queryset=User.objects.all(), widget=HiddenInput, required=False)
    receiver = ModelChoiceField(queryset=User.objects.all(), widget=HiddenInput, required=False)

    class Meta:
        model = AnyPost
        fields = ('text', 'sender', 'receiver')

    def save(self, force_insert=False, force_update=False, commit=True):
        instance = super(WallPostForm, self).save(commit=False)
        instance.post_type = AnyPost.WALL
        if commit:
            instance.save()
        return instance


class ProfileForm(ModelForm):
    name = CharField(max_length=20)
    last_name = CharField(max_length=20)

    class Meta:
        model = SocialProfile
        exclude = ['friends', 'user']
