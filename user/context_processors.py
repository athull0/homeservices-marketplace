from .forms import RegUser

def registration_form(request):
    return {'form':RegUser()}