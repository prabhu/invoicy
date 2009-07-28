from django.conf.urls.defaults import *
from invoicy.guidy.views import guidy_default, guidy_home, guidy_login, guidy_logout
from django.conf import settings

urlpatterns = patterns('',
    (r'^$', guidy_default),
    (r'^login/$', guidy_login),
    (r'^logout/$', guidy_logout),
    (r'^guidy/$', guidy_home),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^(?P<path>(?:images|scripts|css|openlayers).*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
