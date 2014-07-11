from django.conf.urls import patterns, url

urlpatterns = patterns('users.views',
		url(r'^email/$', 'email_form', name="friend_email_form"),
		)