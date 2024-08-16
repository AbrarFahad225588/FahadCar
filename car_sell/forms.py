from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .models import Car, Brand,Comment
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name','last_name','password1','password2']
class userChangeData(UserChangeForm):
    password=None
    class Meta:
        model=User
        fields=['username','first_name','last_name','email']     
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'comment']        