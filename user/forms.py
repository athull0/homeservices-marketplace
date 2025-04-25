from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *
class RegUser(UserCreationForm):
      email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}))
      username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}))
      password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}))
      password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'}))

      class Meta:
         model = User
         fields = ['username' , 'email','password1','password2']

class Regworker(UserCreationForm):    
      username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your username'}))
      email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter your Email'}))
      password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}))
      password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'}))

      class Meta:
         model = User
         fields = ['username' , 'email','password1','password2']
    
    


class UserProfileForm(forms.ModelForm):
     username = forms.CharField(max_length=150,widget=forms.TextInput(attrs={'class':'form-control'}))
     address = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','rows':3}))
     profilepicture = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class':'form-control'}))
     contact = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}))
     class Meta:
          model = UserProfile
          exclude= ['user']



class WorkerProfileForm(forms.ModelForm):
      username = forms.CharField(max_length=150,widget=forms.TextInput(attrs={'class':'form-control'}))
      job_title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ' '})
    )
      skills = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': ' ', 'rows': 3})
    )
      profilepicture = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )
      contact = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ' ', 'pattern': '[0-9]+', 'title': 'Only numbers allowed'})
    )
      categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'})
     
    )
      availability = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

        
    
     
      class Meta:
          model = WorkerProfile
          exclude = ['user']

class FeedbackForm(forms.ModelForm):
     RATING_CHOICES = [(i, '★' * i + '☆' * (5 - i)) for i in range(5, 0, -1)]

     rating = forms.ChoiceField(
        label="Rate the service",
        choices=RATING_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'rating-stars'})
    )

     comment = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Write your comment here'})
    )
     class Meta:
          model = Feedback
          fields = ['rating','comment']



          