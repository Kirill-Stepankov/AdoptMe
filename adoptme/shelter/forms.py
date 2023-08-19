from django import forms
from .models import Shelter, ShelterPhoto, ShelterApply

class CreateShelterForm(forms.ModelForm):
    main_photo = forms.ImageField(widget=forms.widgets.FileInput, required=False)

    class Meta:
        model = Shelter
        fields = [
        'name',
        'main_photo',
        'email',
        'about',
        'city',
        'adress',
        'contact_ref'
    ]
        
class ShelterPhotoForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.widgets.FileInput)

    class Meta:
        model = ShelterPhoto
        fields = [
            'image',
            'shelter'
        ]
        widgets = {'shelter': forms.HiddenInput()}

class ShelterApplyForm(forms.ModelForm):
    class Meta:
        model = ShelterApply
        fields = [
            'content',
            'profile',
            'shelter'
        ]
        widgets = {'shelter': forms.HiddenInput(), 'profile': forms.HiddenInput()}
