from django.conf.urls import patterns, url

urlpatterns = patterns('users.views',
        url(r'^email/$', 'email_form', name="friend_email_form"),
        url(r'^(?P<username>[-\w]+)/$', 'user_details', name="debt_user_details"),
        url(r'^friends/(?P<username>[-\w]+)/$', 'user_friends', name='debt_user_friends'),
        )