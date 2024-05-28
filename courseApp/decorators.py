from django.shortcuts import redirect

def notLoggedUser(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return view_func(request, *args, **kwargs)
    
    return wrapper_func


def allowedUsers(allowedGroups=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowedGroups:
                return view_func(request, *args, **kwargs)
            else:
                return redirect('/')
        return wrapper_func
    return decorator


def forAdmins(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'admin':
            return view_func(request, *args, **kwargs)
        elif group == 'students':
            student = request.user.student
            return redirect('student', student.pk) 
        else:
            return redirect('login') 
        
    return wrapper_func