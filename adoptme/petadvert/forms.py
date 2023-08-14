from django import forms
from .models import PetAdvert, PetAdvertPhoto
from django.core.files.images import get_image_dimensions
from userprofile.utils import FormSquarePhotoMixin


class PetAdvertForm(FormSquarePhotoMixin, forms.ModelForm):
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

class PetAdvertPhotoForm(FormSquarePhotoMixin, forms.ModelForm):
    photo = forms.ImageField(widget=forms.widgets.FileInput)

    class Meta:
        model = PetAdvertPhoto
        fields = [
            'photo',
            'pet_advert'
        ]
        widgets = {'pet_advert': forms.HiddenInput()}