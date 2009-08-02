from django.conf.urls.defaults import *
from django.conf import settings

# exporty views
urlpatterns = patterns('exporty.views',
    url(r'^$', 'exporty_home', name='exporty-home'),
)

