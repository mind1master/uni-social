from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
from social.apps.core.views import (HomeView, ProfileView, FriendsView,
                                    friends_manipulation, profile_edit)
                                    friends_manipulation, messages_list, message_write,
                                    check_messages, search_friends)
from django.contrib.auth.decorators import login_required


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', login_required(HomeView.as_view()), name='home_page'),
    url(r'^login/$', 'social.apps.core.views.custom_login', {
        'template_name':'core/login.html',
    }, name='login_page'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {
        'next_page': '/',
        }, name='logout_page'),
    url(r'^profile/(?P<pk>\d+)/$', login_required(ProfileView.as_view()), name='profile_page'),
    url(r'^profile/edit/$', login_required(profile_edit), name='profile_edit_page'),
    url(r'^friends/$', login_required(FriendsView.as_view()), name='friends_page'),
    url(r'^friends/search/$', search_friends, name='search_friends_page'),
    url(r'^messages/$', messages_list, name='messages_page'),
    url(r'^messages/check/$', check_messages, name='check_messages'),
    url(r'^messages/write/(?P<pk>\d+)/$', message_write, name='message_write_page'),
    url(r'^friends_manipulation/$', login_required(friends_manipulation), name='friends_manipulation'),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )


if settings.IS_TESTING:
    urlpatterns += patterns('',
        url(r'^user/(?P<username>[\w@\.+-]+)/$', 'helpers42cc.views.profile',
            name='profile')
    )