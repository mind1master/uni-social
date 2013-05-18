# -*- coding: utf-8 -*-
from django.forms import ModelForm, HiddenInput, ModelChoiceField
from django.contrib.auth.models import User

from social.apps.core.models import AnyPost


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