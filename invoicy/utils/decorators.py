from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.core.urlresolvers import NoReverseMatch

# Decorators specific to invoicy

def data_required(model=None, mincount=1, failure_view=None):
    """
    Decorator which checks the given model for the minimum number of rows.
    If the models has lesser rows, then we will redirect to the failure_view.
    Otherwise we direct to the original view upon success.
    """
    def decorate(view_func):
        def _dec(request, *args, **kw_args):
            if not model or not failure_view:
                raise AttributeError("Decorator requires both model and failure_view")
            if model.objects.count() < mincount:
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
