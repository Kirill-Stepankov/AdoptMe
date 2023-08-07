from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username', 
            'email', 
            'password1', 
            'password2'
        ]

class LoginForm(AuthenticationForm):
    class Meta:
        fields = [
            'username',
            'password'
        ]

class ProfileUpdateForm(forms.ModelForm):
    profile_pic = forms.ImageField(widget=forms.widgets.FileInput)
    class Meta:
        model = Profile
        fields = [
            'sex',
            'profile_pic',
            'about'
        ]
