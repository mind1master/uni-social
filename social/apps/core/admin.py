from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from social.apps.core.models import SocialProfile

class UserInline(admin.StackedInline):
    model = SocialProfile
    can_delete = False
    verbose_name_plural = 'social users'

# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (UserInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
