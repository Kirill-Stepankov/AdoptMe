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
            'color',
            'health',
            'gender',
            'type',
            'size',
            'age',
            'breed',
            'city',
            'about',
            'house_trained',
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