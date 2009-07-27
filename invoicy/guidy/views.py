from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.utils import simplejson as json
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext

def guidy_home(request):
    """
    Handle request to the home page.
    """
    return render_to_response('guidy/home.html', {})
    
def guidy_login(request):
    """
    Handle login request
    """
    # If this is called using GET request, simply redirect to the homepage.
    # Home page takes care of displaying the login form.
    if request.method == 'GET':
        return render_to_response('guidy/home.html', {})
        
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
                invalid_user = False
            else:
                # Return a 'disabled account' error message
                invalid_user = True
                reason = 'account_disabled'
        else:
            # Return an 'invalid login' error message.
            invalid_user = True      
    return render_to_response('guidy/home.html',
                              {'invalid_user' : invalid_user, 'reason' : reason},
                              context_instance=RequestContext(request))
    
def guidy_logout(request):
    logout(request)
    return render_to_response('guidy/home.html', {'logout' : True})
