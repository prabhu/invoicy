from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.utils import simplejson as json
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django.core.urlresolvers import reverse

def guidy_default(request):
    """
    Handle request to the home page of invoicy before login.
    """
    user = request.user
    if user and user.is_authenticated():
        return redirect(reverse('guidy-home'))
    else:
        return render_to_response('guidy/default.html', {},
                                  context_instance=RequestContext(request))

@login_required(redirect_field_name='r')
def guidy_home(request):
    """
    Handle request to the home page after login.
    """    
    return render_to_response('guidy/home.html', {},
                              context_instance=RequestContext(request))
    
def guidy_login(request):
    """
    Handle login request
    """
    # If this is called using GET request, simply redirect to the homepage.
    # Home page takes care of displaying the login form.

    if request.method == 'GET':
        redirect_url = request.GET.get('r', '')
    else:
        redirect_url = request.REQUEST.get('r', '')
        
    if redirect_url and redirect_url != '':
        redirect_url = '?r=' + redirect_url

    if request.method == 'GET':
        return redirect(reverse('guidy-default'))
        
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    invalid_user = False
    reason = None
    if not username:
        invalid_user = True

    if username and password:
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # Redirect to a success page.
                return redirect(reverse('guidy-home'))
            else:
                # Return a 'disabled account' error message
                invalid_user = True
                reason = 'account_disabled'
        else:
            # Return an 'invalid login' error message.
            invalid_user = True      
    return render_to_response('guidy/default.html',
                              {'invalid_user' : invalid_user, 'reason' : reason},
                              context_instance=RequestContext(request))
    
def guidy_logout(request):
    """
    Handles logout.
    """
    logout(request)
    return redirect(reverse('guidy-default'))
   
