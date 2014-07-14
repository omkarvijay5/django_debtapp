from django.conf.urls import patterns, include, url
from users.views import UserDetails
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^accounts/', include('registration.auth_urls')),
    url(r'^$', UserDetails.as_view(), name='home_page'),
    url(r'^users/', include('users.urls')),
)
