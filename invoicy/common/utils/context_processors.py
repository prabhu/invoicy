# Basic workflow engine. 
# FIXME: This might become ugly and might require redesigning
from clienty.models import Client, OwnCompany

def workflow_processor(request):
    """
    Processor which takes care of the workflow.
    Currently is very simple and returns a dict with some useful keys.    
    """
    tabs_list = ['guidy', 'clienty', 'exporty', 'settings']
    ret_args = {}
    
    # Traverse the required list first
    for key in request.session.keys():
        if 'Required' in key:     
            if request.session.get(key, None):
                # Remove this key inorder to prevent the flag from getting carried 
                # over and over.
                ret_args.update({'workflow' : key})
            del request.session[key]
    
    # Find if the user is new. 
    # FIXME: User is new if he has no own company.
    user = request.user
    if user and not user.is_superuser and not user.is_anonymous():
        count = OwnCompany.objects.filter(user=user, own_company=True).count()
        if not count:
            ret_args.update({'newuser' : True})
                                    
    # Find tab_name
    tab_name = 'guidy'
    for tab in tabs_list:
        if tab in request.path:
            tab_name = tab
            break
    ret_args.update({'tab_name' : tab_name})
    return ret_args
            