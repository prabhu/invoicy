from django.conf.urls.defaults import *
from django.conf import settings

# Clienty views
urlpatterns = patterns('clienty.views',
    url(r'^$', 'clienty_home', name='clienty-home'),    
)


