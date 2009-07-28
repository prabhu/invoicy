from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('invoicy.guidy.views',
    url(r'^$', 'guidy_default', name='guidy-default'),
    url(r'^login/$', 'guidy_login', name='guidy-login'),
    url(r'^logout/$', 'guidy_logout', name='guidy-logout'),
    url(r'^guidy/$', 'guidy_home', name='guidy-home'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^(?P<path>(?:images|scripts|css|openlayers).*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
