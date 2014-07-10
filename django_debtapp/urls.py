from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'django_debtapp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^users/', include('users.urls')),
    (r'^accounts/', include('registration.backends.default.urls')),
    (r'^', include('django.contrib.auth.urls')),
    (r'^$', TemplateView.as_view(template_name="index.html")),
)
