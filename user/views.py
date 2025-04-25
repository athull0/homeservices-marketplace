from django.shortcuts import render,redirect,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from website.views import homepage,workerhomepage,worker_detail,dashboard
from .forms import *
from django.contrib import messages
from django.http import JsonResponse
from .models import*
from django.contrib.auth.decorators import login_required
# Create your views here.

from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from .task import *
def adduser(request):
    if request.method == 'POST':
        form = RegUser(request.POST)
        if form.is_valid():            
            user = form.save()
            send_welcome_email.delay(user.email,user.username)
            
            login(request,user)
            UserProfile.objects.create(user=user)
            messages.success(request,'User has been created successfully')
            return redirect(homepage)
    else:
        form = RegUser()
    return render(request,'register.html',{'form':form})

            

def loginpage(request):
    if request.method == 'POST':
        usern = request.POST.get('user')
        passw = request.POST.get('pass')
        user = authenticate(request,username=usern,password=passw)
        if user:
            if user.is_superuser:
                login(request,user)
                return redirect(dashboard)
            if not hasattr(user,'worker_profile'):
                login(request,user)
                messages.success(request,'user has been authenticated')
                return redirect(homepage)
            else:
                messages.error(request, 'Workers must log in through the worker login page.')
                return redirect(loginpage)
        else:
            messages.error(request,'Invalid username or password')
            return redirect(loginpage)
        
    return render(request,'login.html')
       

def logoutpage(request):
    logout(request)
    messages.success(request,'User has logged out')
    return redirect(homepage)


def addworker(request):
    if request.method == 'POST':
        form = Regworker(request.POST)
        if form.is_valid():
            user = form.save()
            WorkerProfile.objects.create(user = user)
            messages.success(request,'Worker has been created')
            login(request,user)
            return redirect(workerhomepage)
    else:
        form = Regworker()
    return render(request,'workerregister.html',{'form':form})

def loginworker(request):
    if request.method == 'POST':
        usern = request.POST.get('user')
        passw = request.POST.get('pass')
        user = authenticate(request,username=usern,password=passw)
        if user:
            if hasattr(user,'worker_profile'):
                login(request,user)
                messages.success(request,'You are authenticated!')
                return redirect(workerhomepage)
            else:
                messages.error(request,'You are not registered as a worker.Please log in as a user')
                return redirect(loginworker)
        else:
            messages.error(request,"Invalid username or password")
            return redirect(loginworker)
    return render(request,'workerlogin.html')


def logoutpage(request):
    logout(request)
    messages.success(request,'User has logged out')
    return redirect(homepage)


def base(request):
    if request.method == 'POST':
        form = RegUser(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'user has registered successfully')
            return redirect(homepage)
    else:
        form = RegUser()
    return render(request,'base.html',{'form':form})

def create_profile(request):
    return render(request,'createuser.html')

def profilepage(request):
    try:
        worker_profile = WorkerProfile.objects.get(user=request.user)
        return render(request,'workerprofile.html',{'pro':worker_profile})
    except WorkerProfile.DoesNotExist:
        
        try:
            user_profile = UserProfile.objects.get(user = request.user)
            return render(request, 'userprofile.html',{'pro':user_profile})
        except UserProfile.DoesNotExist:

            return redirect('create_profile')


def editprofile(request):
    profile = request.user.userprofile
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            user.username = form.cleaned_data['username']
            user.save()
            form.save()
            return redirect('editprofile')
    else:
            form = UserProfileForm(instance=profile,initial={'username':user.username})
    return render(request,'editprofile.html',{'form':form})

def edit_worker_profile(request):
    profile = request.user.worker_profile
    pending_requests_count = HireRequest.objects.filter(worker=profile, status='pending').count()
    user = request.user
    if request.method == 'POST':
        form = WorkerProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            user.username = form.cleaned_data['username']
            user.save()
            form.save()
            return redirect('weditprofile')  
    else:
        form = WorkerProfileForm(instance=profile,initial={'username':user.username})
    return render(request, 'workerprofileedit.html', {'form': form,'pending_requests_count':pending_requests_count})

def toggle_availability(request):
    user = request.user
    user.availability = not user.availability
    user.save()
    return JsonResponse({"availability": user.availability})



