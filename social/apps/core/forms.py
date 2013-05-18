# -*- coding: utf-8 -*-
from django.forms import ModelForm, HiddenInput

from social.apps.core.models import AnyPost


# Create the form class.
class WallPostForm(ModelForm):
    class Meta:
        model = AnyPost
        fields = ('text', 'sender', 'receiver')
        widgets = {
            'sender': HiddenInput,
            'receiver': HiddenInput,
        }

    def save(self, *args, **kwargs):
        instance = super(WallPostForm, self).save(commit=False)
        instance.post_type = AnyPost.WALL
        instance.save()
        return instance