from django import forms
from .models import PetAdvert, PetAdvertPhoto
from django.core.files.images import get_image_dimensions


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
    
    def clean_photo(self):
       picture = self.cleaned_data.get("photo")
       if not picture:
           raise forms.ValidationError("No image!")
       else:
           w, h = get_image_dimensions(picture)
           if w != h:
               raise forms.ValidationError("The image must be square")
       return picture