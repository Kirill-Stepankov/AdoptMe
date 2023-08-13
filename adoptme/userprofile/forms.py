from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile, PetAdvert, PetAdvertPhoto
from django.core.files.images import get_image_dimensions


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

class ProfileUpdateForm(forms.ModelForm):
    profile_pic = forms.ImageField(widget=forms.widgets.FileInput)
    class Meta:
        model = Profile
        fields = [
            'sex',
            'profile_pic',
            'about'
        ]
    
    def clean_profile_pic(self):
       picture = self.cleaned_data.get("profile_pic")
       if not picture:
           raise forms.ValidationError("No image!")
       else:
           w, h = get_image_dimensions(picture)
           if w != h:
               raise forms.ValidationError("The image must be square")
       return picture

class PetAdvertForm(forms.ModelForm):
    photo = forms.ImageField(widget=forms.widgets.FileInput)
    class Meta:
        model = PetAdvert
        fields = [
            'name',
            'photo',
            'about',
            'gender',
            'type',
            'size',
            'age',
            'breed'
        ]

    def clean_photo(self):
       picture = self.cleaned_data.get("photo")
       if not picture:
           raise forms.ValidationError("No image!")
       else:
           w, h = get_image_dimensions(picture)
           if w != h:
               raise forms.ValidationError("The image must be square")
       return picture

class PetAdvertPhotoForm(forms.ModelForm):
    class Meta:
        model = PetAdvertPhoto
        fields = [
            'photo',
            'pet_advert'
        ]
        widgets = {'pet_advert': forms.HiddenInput()}