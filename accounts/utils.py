def detectUser(user):
    '''
    This function will help us user role and after logging in it will 
    redirect user to their respective dashboard
    '''
    redirecturl = 'login'
    if user.role == 1:
        redirecturl = 'venddashboard'
    elif user.role == 2:
        redirecturl = 'custdashboard'
    elif user.role == None and user.is_superadmin:
        redirecturl = '/admin'
    
    return redirecturl