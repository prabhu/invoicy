from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.core.urlresolvers import NoReverseMatch
from django.contrib.auth.models import User, Group, Permission
from django.core.cache import cache

# Decorators specific to invoicy
def data_required(model=None, mincount=1, failure_view=None, filter_cond=None, user_filter=False):
    """
    Decorator which checks the given model for the minimum number of rows.
    If the models has lesser rows, then we will redirect to the failure_view.
    Otherwise we direct to the original view upon success.
    
    Eg from guidy/views.py:
    @data_required(model=OwnCompany, failure_view='/admin/clienty/owncompany/add/', user_filter=True)
    This would check the model OwnCompany for rows created by the current user. If not it will
    redirect to add screen with an additional session property OwnCompanyRequired.    
    """
    def decorate(view_func):
        def _dec(request, *args, **kw_args):
            if not model or not failure_view:
                raise AttributeError("Decorator requires both model and failure_view")
            count = 0
            rows = None
            if filter_cond:
                rows = model.objects.filter(**filter_cond)
            else:
                rows = model.objects.all()
            if user_filter and not request.user.is_superuser:
                rows = rows.filter(user=request.user)
            count = rows.count()

            if count < mincount:
                # Store the additional session argument in session. This will be used
                # by the workflow engine to decide on the next step.
                request.session[model._meta.object_name + "Required"] = True
                
                # See if you can reverse map the url.
                # There will be hardly any performance impact since django
                # maintains a map of views to viewresolves anyway.
                try:
                    return redirect(reverse(failure_view))
                except NoReverseMatch:
                    return redirect(failure_view)
            return view_func(request, *args, **kw_args)
        return _dec   
    return decorate

def group_create(name=None, models_list=None, permission_list=None):
    """
    Decorator to create a group for the given name. By default sets read, change, delete
    for the specified models.
    """
    def decorate(view_func):
        def _dec(request, *args, **kw_args):
            if not name or not models_list or len(models_list) < 1:
                raise AttributeError("Decorator requires both name and models list")
            try:
                group = Group.objects.get(name=name)
            except Group.DoesNotExist:
                group = Group()
                group.name = name
                # Save and re-load in-order to get the primary key.
                # Otherwise you cant have many-to-many relationship.
                group.save()
                codename_list = [perm + '_' + model for model in models_list for perm in permission_list]
                permissions = Permission.objects.filter(codename__in = codename_list)
                group.permissions = permissions
                group.save()
            
            return view_func(request, *args, **kw_args)
        return _dec
    return decorate

def rate_limit(time=60):
    """
    Decorator to limit the request rate. Redirects with a forbidden error code.
    Primarily used for fighting spams during registeration. No need for captcha hence. 
    """
    def decorate(view_func):
        def _dec(request, *args, **kw_args):
            ip = request.META['REMOTE_ADDR']
            val = cache.get(ip)
            if not val:
                cache.set(ip, "1", time)
                return view_func(request, *args, **kw_args)
            else:
                from django.http import HttpResponseForbidden
                return HttpResponseForbidden('Rate limit exceeded. Please wait for ' + str(time) + ' seconds')
        return _dec
    return decorate
        