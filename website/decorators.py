from django.shortcuts import redirect
from functools import wraps 

def worker_required(view_func):
    @wraps(view_func)
    def wrapper(request,*args,**kwargs):
        if hasattr(request.user,'worker_profile'):
            return view_func(request,*args,**kwargs)
        else:
            return redirect('home')
    return wrapper

def user_required(view_func):
    @wraps(view_func)
    def wrapper(request,*args,**kwargs):
        if hasattr(request.user,'userprofile'):
            return view_func(request,*args,**kwargs)
        else:
            return redirect("workerhome")
    return wrapper