from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# Support for running invoicy with a url prefix rather than assuming
# invoicy will always run as the root application.
try:
    urlprefix = settings.URL_PREFIX
except:
    urlprefix = ''

urlpatterns = patterns('',
    (r'^' + urlprefix, include('guidy.urls')),
    (r'^clienty/' + urlprefix, include('clienty.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^' + urlprefix + 'admin/', include(admin.site.urls)),
        (r'^(?P<path>(?:images|scripts|css|openlayers).*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
