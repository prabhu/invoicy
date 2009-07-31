from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django.core.urlresolvers import reverse

from common.utils.decorators import data_required
from common.utils.middleware import get_current_user
from clienty.models import Client, Contact

@login_required(redirect_field_name='r')
@data_required(model=Client, failure_view='/admin/clienty/client/add/', user_filter=True)
def clienty_home(request, **args):
    """
    Default page in clients tab.
    """
    print request.user
    return redirect('/admin/clienty/client/')
   
    