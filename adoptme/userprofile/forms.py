from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile
from django.core.files.images import get_image_dimensions
from userprofile.utils import FormSquarePhotoMixin


class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'email', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

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

class ProfileUpdateForm(FormSquarePhotoMixin, forms.ModelForm):
    profile_pic = forms.ImageField(widget=forms.widgets.FileInput)
    class Meta:
        model = Profile
        fields = [
            'sex',
            'profile_pic',
            'about'
        ]