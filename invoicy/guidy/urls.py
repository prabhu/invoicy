from django.conf.urls.defaults import *
from django.conf import settings

# Guidy views
urlpatterns = patterns('guidy.views',
    url(r'^$', 'guidy_default', name='guidy-default'),
    url(r'^login/$', 'guidy_login', name='guidy-login'),
    url(r'^logout/$', 'guidy_logout', name='guidy-logout'),
    url(r'^guidy/$', 'guidy_home', name='guidy-home'),
    url(r'^admin/$', 'guidy_home', name='admin-home'),
    url(r'^admin/login/$', 'guidy_login', name='guidy-login'),
    url(r'^admin/logout/$', 'guidy_logout', name='guidy-logout'),
)

# Handle admin urls belonging to each app.
urlpatterns += patterns('clienty.views',
    url(r'^admin/clienty/$', 'clienty_home', name='clienty-admin-home'),
)

# Handle admin urls belonging to each app.
urlpatterns += patterns('exporty.views',
    url(r'^admin/exporty/$', 'exporty_home', name='exporty-admin-home'),
)
