from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.core.urlresolvers import NoReverseMatch
from django.contrib.auth.models import User, Group, Permission

# Decorators specific to invoicy

def data_required(model=None, mincount=1, failure_view=None, filter_cond=None, user_filter=False):
    """
    Decorator which checks the given model for the minimum number of rows.
    If the models has lesser rows, then we will redirect to the failure_view.
    Otherwise we direct to the original view upon success.
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
            if user_filter:
                rows = rows.filter(user=request.user)
            count = rows.count()   
            if count < mincount:
                # See if you can reverse map the url.
                # There will be hardly any performance impact since django
                # maintains a map of views to viewresolves anyway.
                try:
                    return reverse(failure_view)
                except NoReverseMatch:
                    return redirect(failure_view)
            return view_func(request, *args, **kw_args)
        return _dec   
    return decorate

def group_required(name=None, models_list=None, permission_list=None):
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
                group = Group.objects.get(name=name)
                codename_list = [perm + '_' + model for model in models_list for perm in permission_list]
                permissions = Permission.objects.filter(codename__in = codename_list)
                group.permissions = permissions
                group.save()
            
            return view_func(request, *args, **kw_args)
        return _dec
    return decorate
    