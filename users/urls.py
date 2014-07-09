from django.conf.urls import patterns, url

urlpatterns = patterns('users.views',
	url(r'^signup/$','register', name='user_signup'),
	url(r'^(?P<username>[-\w]+)/$', 'details', name='user_details'),
	)