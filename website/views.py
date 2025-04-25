from django.shortcuts import render,redirect,get_object_or_404
from .forms import CategoryForm
from .models import *
from django.http import JsonResponse,HttpResponseForbidden
from user.forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from user.models import *
from .decorators import worker_required,user_required
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
import json
from django.templatetags.static import static

import logging
logger = logging.getLogger(__name__)

# from user.views import loginpage

# Create your views here.


def homepage(request):
    cat = Category.objects.all()
    if request.user.is_authenticated:
        if hasattr(request.user,'worker_profile'):
            return redirect(workerhomepage)
        elif request.user.is_superuser:
            return redirect(dashboard)
    
    return render(request,'home.html',{'cat':cat})
@worker_required
def workerhomepage(request):
    worker_profile = WorkerProfile.objects.get(user=request.user)
    pending_requests_count = HireRequest.objects.filter(worker=worker_profile, status='pending').count()
    
    return render(request,'workerhomepage.html',{'pending_requests_count':pending_requests_count})

def addcategory(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Category added successfully')
            return redirect(dashboard)
        else:
            messages.error(request,'Invalid data')
    else:
        form = CategoryForm()
    return render(request,'addcat.html',{'form':form})
def is_admin(user):
    return user.is_superuser
# @login_required
# @user_passes_test(is_admin)
def dashboard(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You are not allowed to view this page.")

    return render(request,'dashboard.html')

def manage_users(request):
    users = UserProfile.objects.all()
    return render(request,'userslist.html',{'users':users})
def manage_workers(request):
    workers = WorkerProfile.objects.all()
    return render(request,'workerslist.html',{'workers':workers})
def pending_workers(request):
    workers = WorkerProfile.objects.filter(status='pending')
    return render(request,'pending_workers.html',{'workers':workers})
def pending_workers_action_accept(request,user_id):
    worker_profile = WorkerProfile.objects.get(id=user_id)
    if request.method == 'POST':
        
        worker_profile.status = 'accepted'
        worker_profile.save()
        return redirect(pending_workers)
def pending_workers_action_reject(request,user_id):
    worker_profile = WorkerProfile.objects.get(id=user_id)
    if request.method == 'POST':
        worker_profile.status = 'rejected'
        worker_profile.rejection_message = "Your application was rejected due to incomplete profile , Please update your profile and apply again."
        worker_profile.save()
        
        return redirect(pending_workers)

def worker_reapply(request):
    worker_profile = request.user.worker_profile
    worker_profile.status = 'pending'
    worker_profile.rejection_message = ''
    worker_profile.save()
    return redirect(workerhomepage)
    
def userdelete(request,user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        
  
        user.delete()
        messages.success(request,'User successfully removed')
        return redirect(manage_users)
    return render(request,'userdelete.html',{'user':user})
def workerdelete(request,user_id):
    worker = User.objects.get(id=user_id)
    if request.method == 'POST':
        worker.delete()
        messages.success(request,'Worker successfully removed')
        return redirect(manage_workers)
    
    return render(request,'workerdelete.html',{'worker':worker})

def get_categories(request):
    categories = Category.objects.all()
    return render(request,'categories.html',{'categories':categories})

def catupdate(request,category_id):
    cat = Category.objects.get(id = category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST,request.FILES,instance=cat)
        if form.is_valid():
            form.save()
            messages.success(request,'Category updated')
            return redirect(get_categories)
        else:
            messages.warning(request,'Invalid data')
            return redirect(catupdate)
        
    else:
        form = CategoryForm(instance=cat)
    return render(request,'editcat.html',{'form':form})
def catdelete(request,category_id):
    cat = Category.objects.get(id = category_id)
    if request.method == 'POST':

        cat.delete()
        messages.success(request,'Category deleted successfully')
        return redirect(get_categories)
        
       
    else:
     return render(request,'catdel.html',{'cat':cat})   

def worker_list_by_category(request,category_id):
    category = Category.objects.get(id = category_id)
    workers = WorkerProfile.objects.filter(categories=category,status = 'accepted')
    
    return render(request,'worker_list.html',{'category':category,'workers':workers})

def worker_detail(request,wid):
    if not request.user.is_authenticated:
        messages.warning(request, "You need to log in to view the worker's profile.")
        return redirect('loginpage')
    worker = WorkerProfile.objects.get(id = wid)
    user_profile= request.user.userprofile

    wishlist = WishList.objects.filter(user=request.user,worker = worker)
    hire_request = HireRequest.objects.filter(user=request.user,worker=worker).order_by('-id').first()
    feedbacks = Feedback.objects.filter(worker=worker).order_by('created_at')
    can_give_feedback = False
    if hire_request and hire_request.completed:
        existing_feedback = Feedback.objects.filter(worker=worker,user=request.user,created_at__gte=hire_request.created_at).exists()
        if not existing_feedback:
            can_give_feedback = True
    if request.method == 'POST' and can_give_feedback:
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.worker = worker
            feedback.save()
            messages.success(request,"Your feedback has been submitted successfully!")
            return redirect(worker_detail,wid=wid)
    else:
        form = FeedbackForm()
    return render(request,'workerdetail.html',{'worker':worker,'hire_request':hire_request,'feedbacks':feedbacks,'can_give_feedback':can_give_feedback,'form':form,'user_profile':user_profile,'wishlist':wishlist})

def send_hire_request(request,worker_id):
    if request.method == 'POST':
        print(f"User ID: {request.user.id}")
        worker = WorkerProfile.objects.get(id = worker_id)
        user = User.objects.get(id = request.user.id)
        user_profile = user.userprofile
        existing_request = HireRequest.objects.filter(user=user, worker = worker ,status='pending').first()
        if existing_request:
            messages.warning(request,'You have already sent a hire request to this worker')
            return redirect(worker_detail,wid=worker_id)
        else:
            try:
                points_to_use = int(request.POST.get('points_to_use', 0))
            except (ValueError, TypeError):
                points_to_use = 0


            if points_to_use > user_profile.reward_points:
                messages.error(request,"You dont have enough reward points.")
                return redirect(worker_detail,wid=worker_id)
            
            user_profile.reward_points -=points_to_use
            user_profile.save()




            hire_request = HireRequest.objects.create(user=request.user,worker=worker,used_points=points_to_use)
            hire_request.save()
            messages.success(request,'Hire request sent successfully')
        return redirect(worker_detail,wid=worker_id)
    return redirect(homepage)

@login_required
def cancel_hire_request(request, request_id):
    hire_request = HireRequest.objects.get(id=request_id, user=request.user)
    user_profile = request.user.userprofile
    user_profile.reward_points += hire_request.used_points
    user_profile.save()
    hire_request.delete()
    messages.success(request, "Hire request canceled successfully.")
    return redirect(worker_detail, wid=hire_request.worker.id)
@login_required
def mark_completed(request, request_id):
    hire_request = HireRequest.objects.get(id=request_id, user=request.user)
    user_profile = request.user.userprofile
    worker_profile = hire_request.worker
    
    if hire_request.status == "accepted" and not hire_request.completed:
        
        user_profile.reward_points += 10
        worker_profile.points += 1
        worker_profile.save()
        hire_request.completed = True
        hire_request.save()
        user_profile.save()
        messages.success(request, "Work marked as completed. You can now rehire the worker.")
    else:
        messages.error(request, "This hire request cannot be marked as completed.")

    return redirect(worker_detail,wid=hire_request.worker.id)

def add_to_wishlist(request,wid):
    user = request.user
    worker = WorkerProfile.objects.get(id = wid)
    if request.method == 'POST':
        WishList.objects.create(user=user,worker=worker)

    return redirect(worker_detail,wid)

def delete_from_wishlist(request,wid):
    worker = WorkerProfile.objects.get(id = wid)
    wishlist = WishList.objects.get(user=request.user,worker = worker)
    if request.method == 'POST':
        wishlist.delete()
    
    return redirect(worker_detail,wid)

def wishlist(request):

    wishlists = WishList.objects.filter(user = request.user)
    return render(request,'wishlist.html',{'wishlists':wishlists})

def worker_requests(request):
    worker_profile = WorkerProfile.objects.get(user=request.user)
    hire_requests = HireRequest.objects.filter(worker = worker_profile, status = 'pending')
    for hire_request in hire_requests:
        hire_request.user_profile = UserProfile.objects.get(user=hire_request.user)
    return render(request,'worker_request.html',{'hire_requests':hire_requests})

@login_required
def respond_hire_request(request, request_id):
    worker_profile = WorkerProfile.objects.get(user=request.user)
    hire_request = HireRequest.objects.get(id=request_id,worker = worker_profile)
    
    if request.method == "POST":
        response = request.POST.get("response")
        if response in ["accepted", "rejected"]:
            hire_request.status = response
            hire_request.message = f"Your hire request was {response} by {request.user.username}"
            hire_request.save()
            messages.success(request, f"Hire request has been {response}.")
        else:
            messages.error(request, "Invalid response.")

    return redirect('worker_requests')

@login_required
def user_hire_requests(request):
    user_requests = HireRequest.objects.filter(user=request.user).order_by('-id')
    return render(request, 'user_hire_requests.html', {'user_requests': user_requests})

def search_workers(request):
    search_query = request.GET.get('q', '')  
    workers = WorkerProfile.objects.all()  

    if search_query:
        workers = workers.filter(Q(categories__name__icontains=search_query) |
                                 Q(user__username__icontains=search_query) |
                                 Q(job_title__icontains=search_query)

                                 ).distinct()  

    return render(request, 'search_results.html', {'workers': workers, 'search_query': search_query})

def search_users(request):
    search_query = request.GET.get('q','')
    users = User.objects.all()
    if search_query:
        users = users.filter(username__icontains =search_query,worker_profile__isnull=True)  

    return render(request,'search_resutls_users.html',{'users':users,'search_query':search_query})
def search_workers_admin(request):
    search_query = request.GET.get('q','')
    workers = User.objects.all()
    if search_query:
        workers = workers.filter(username__icontains=search_query,worker_profile__isnull=False)
    return render(request,'search_results_workers.html',{'workers':workers,'search_query':search_query})

@login_required
def chat_page(request, receiver_id):
    receiver = get_object_or_404(User, id=receiver_id)
    messages = ChatMessage.objects.filter(
        sender=request.user, receiver=receiver
    ) | ChatMessage.objects.filter(
        sender=receiver, receiver=request.user
    )
    return render(request, 'chat_page.html', {
        'receiver': receiver,
        'messages': messages
    })

@csrf_exempt
@login_required
def send_message(request):
    if request.method == "POST":
        data = json.loads(request.body)
        receiver = User.objects.get(id=data['receiver_id'])
        msg = ChatMessage.objects.create(
            sender=request.user,
            receiver=receiver,
            message=data['message']
        )
        if hasattr(request.user, 'userprofile') and request.user.userprofile.profilepicture:
            profile_url = request.user.userprofile.profilepicture.url
        elif hasattr(request.user, 'worker_profile') and request.user.worker_profile.profilepicture:
            profile_url = request.user.worker_profile.profilepicture.url
        else:
            from django.templatetags.static import static
            profile_url = static('images/default.png')
        return JsonResponse({
            'status': 'ok',
            'message': msg.message,
            'sender': request.user.username,
            'sender_image':profile_url
        })



@login_required
def get_new_messages(request, receiver_id):
    logger.info("get_new_messages view called!") 
    print("🔔 get_new_messages view called!")

    receiver = get_object_or_404(User, id=receiver_id)
    messages = ChatMessage.objects.filter(
        sender=receiver, receiver=request.user, is_read=False
    ).order_by('timestamp')

    msg_list = []
    for msg in messages:
        
        
        if hasattr(msg.sender, 'userprofile') and msg.sender.userprofile.profilepicture:
            profile_url = msg.sender.userprofile.profilepicture.url
        elif hasattr(msg.sender, 'worker_profile') and msg.sender.worker_profile.profilepicture:
            profile_url = msg.sender.worker_profile.profilepicture.url
        else:
            profile_url = static('images/default.png')
        msg_list.append({
            'sender': msg.sender.username,
            'message': msg.message,
            'sender_image': profile_url,
        })
        msg.is_read = True  
        msg.save()

    return JsonResponse({'messages': msg_list})


def allmessages_worker(request):
    messages = ChatMessage.objects.filter(receiver = request.user).order_by('-timestamp')

    unique_messages = {}
    
    for message in messages:
        if message.sender not in unique_messages:
            unique_messages[message.sender] = message

        messages = list(unique_messages.values())
    return render(request,'allmessages.html',{'messages':messages})