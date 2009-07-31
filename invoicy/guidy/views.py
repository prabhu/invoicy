from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group, Permission
from django.template import RequestContext
from django.core.urlresolvers import reverse

from common.utils.decorators import group_required

def guidy_default(request, **args):
    """
    Handle request to the home page of invoicy before login.
    """
    user = request.user
    if user and user.is_authenticated():
        return redirect(reverse('guidy-home'))
    else:
        return render_to_response('default.html', args,
                                  context_instance=RequestContext(request))

@login_required(redirect_field_name='r')
def guidy_home(request, **args):
    """
    Handle request to the home page after login.
    """    
    return render_to_response('guidy/home.html', args,
                              context_instance=RequestContext(request))

@group_required(name = 'invoicy_users', models_list=['client', 'contact'], permission_list=['add', 'change', 'delete'])
def create_user(username, password):
    """
    Method to create a user with proper permissions
    """
    user = User.objects.create_user(username, '', password)
    user.is_staff = True
    user.save()
    # Assign this user to a group.
    try:
        groups = Group.objects.filter(name = 'invoicy_users')
        user.groups = groups
        user.save()
    except Group.DoesNotExist:
        print "Group invoicy_users does not exist!"

def guidy_login(request, **args):
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
    register = request.POST.get('register', '0')
    if register == '1':
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:   
            create_user(username, password)
        
    invalid_user = False
    register_allowed = False
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
                register_allowed = False
                reason = 'account_disabled'
        else:
            # Find if the username exists. Otherwise ask if they want to register
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                register_allowed = True
            # Return an 'invalid login' error message.
            invalid_user = True
        args.update({'invalid_user' : invalid_user,
                     'reason' : reason, 
                     'register_allowed' : register_allowed})
        if register_allowed:
            args.update({'username' : username, 'password' : password})
        else:
            password = None
    return render_to_response('default.html',
                              args,
                              context_instance=RequestContext(request))
    
def guidy_logout(request, **args):
    """
    Handles logout.
    """
    logout(request)
    return redirect(reverse('guidy-default'))
   
