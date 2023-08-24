from django import forms
from .models import PetAdvert, PetAdvertPhoto
from django.core.files.images import get_image_dimensions
from userprofile.utils import FormSquarePhotoMixin
from crispy_forms.helper import FormHelper


class PetAdvertForm(forms.ModelForm):
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

class FilterAdForm(forms.ModelForm):
    class Meta:
        model = PetAdvert
        fields = [
            'gender',
            'size',
            'house_trained'
        ]
    
    def __init__(self, *args, **kwargs):
        super(FilterAdForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False 

class PetAdvertPhotoForm(forms.ModelForm):
    photo = forms.ImageField(widget=forms.widgets.FileInput)

    class Meta:
        model = PetAdvertPhoto
        fields = [
            'photo',
            'pet_advert'
        ]
        widgets = {'pet_advert': forms.HiddenInput()}