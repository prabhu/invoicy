# Basic workflow engine. This might become ugly and might require redesigning
from clienty.models import Client, OwnCompany

def workflow_processor(request):
    """
    Processor which takes care of the workflow.
    
    Logic:
    If the user is new, he should start with creating his own company. OwnCompanyAdd
    """
    # List of models for which data needs to be present 
    # before other operation can be allowed.
    add_workflow_list = ['OwnCompany']
    ret_args = {}
    
    # Traverse the required list first
    for key in add_workflow_list:
        newkey = key + 'Required'     
        if request.session.get(newkey, None):
            # Remove this key inorder to prevent the flag from getting carried 
            # over and over.
            ret_args.update({'workflow' : key + 'Add'})
            del request.session[newkey]
    
    # Find if the user is new. 
    # FIXME: User is new if he has no own company.
    if not request.user.is_superuser:
        count = OwnCompany.objects.filter(user=request.user).count()
        if not count:
            ret_args.update({'newuser' : True})
    return ret_args
            