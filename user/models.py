from django.db import models
from django.contrib.auth.models import User
from website.models import Category
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='userprofile')

    address = models.TextField()
    profilepicture = models.ImageField(upload_to='userprofilepics')
    contact = models.IntegerField(null=True)
    reward_points = models.IntegerField(default=0,blank=True)

    def __str__(self):
        return self.user.username


class WorkerProfile(models.Model):
    status_choices = (('pending','Pending'),
                      ('accepted','Accepted'),
                      ('rejected','Rejected'))
    status = models.CharField(max_length=150,choices=status_choices,default='pending',blank=True)
    rejection_message = models.TextField(blank=True,null=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='worker_profile')
    job_title = models.CharField(max_length=100,blank=True)
    skills = models.TextField(null=True)
    profilepicture = models.ImageField(upload_to='workerprofilepics',blank=True,null=True)
    contact = models.IntegerField(null=True)
    categories = models.ManyToManyField('website.Category')
    availability = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False,blank=True)
    points = models.IntegerField(default=0,blank=True)

class WishList(models.Model):
    worker = models.ForeignKey(WorkerProfile,on_delete=models.CASCADE,related_name="wishlist_worker")
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_wishlist')
    message = models.TextField()
class HireRequest(models.Model):
    STATUS_CHOICES = [
        ('pending','Pending'),
        ('accepted','Accepted'),
        ('rejected','Rejected')

    ]

    worker = models.ForeignKey(WorkerProfile, on_delete=models.CASCADE,related_name='worker_hire_requests')
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_hire_requests')
    message = models.TextField(blank=True,null=True)
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    used_points = models.IntegerField(default=0)
    def __str__(self):
        return f"Hire request from {self.user.username} to {self.worker.user.username} ({self.status})"
    
class Feedback(models.Model):
    worker = models.ForeignKey(WorkerProfile,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    rating = models.IntegerField(default=5)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
class ChatMessage(models.Model):
    sender = models.ForeignKey(User,on_delete=models.CASCADE,related_name="sent_messages")
    receiver = models.ForeignKey(User,on_delete=models.CASCADE,related_name='receiver_message')
    message = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True,blank=True)
    is_read = models.BooleanField(default=False,blank=True)
    class Meta:
        ordering = ['timestamp']


    