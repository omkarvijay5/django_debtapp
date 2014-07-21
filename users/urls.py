from django.conf.urls import patterns, url

urlpatterns = patterns('users.views',
        url(r'^email/$', 'add_friend', name="friend_email_form"),
        url(r'^(?P<username>[-\w]+)/$', 'user_details', name="debt_user_details"),
        url(r'^friends/(?P<username>[-\w]+)/$', 'user_friends', name='debt_user_friends'),
        url(r'^split/amount/$', 'split_amount', name='debt_split_amount'),
        url(r'^history/(?P<username>[-\w]+)/$','user_history', name='debt_user_history'),
        url(r'^debt/details/$', 'user_debt_details', name='user_debt_details'),
        )