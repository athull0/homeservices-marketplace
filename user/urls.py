from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('base',base),
    path('reguser',adduser,name='register'),
    path('login',loginpage,name='loginpage'),
    path('logout',logoutpage,name='logout'),
    path('regworker',addworker,name='regworker'),
    path('loginworker',loginworker,name='loginw'),
    path('profile',profilepage,name='profile'),
    path('editprofile',editprofile,name='editprofile'),
    path('workerprofileedit',edit_worker_profile,name='weditprofile'),
    
    path('toggle-availability/', toggle_availability, name='toggle_availability'),
    

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)