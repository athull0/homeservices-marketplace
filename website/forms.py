from django import forms

from .models import *

class CategoryForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':""}))
    details = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','placeholder':""}))
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class':'form-control'}))
    class Meta:
        model = Category
        fields = "__all__"