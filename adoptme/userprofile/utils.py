from django.shortcuts import redirect
from django.core.files.images import get_image_dimensions
from django import forms

def unauthenticated_user(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('profile:home')
		else:
			return view_func(request, *args, **kwargs)

	return wrapper_func

class FormSquarePhotoMixin:
	def clean_photo(self):
		picture = self.cleaned_data.get('photo')
		if not picture:
			raise forms.ValidationError("No image!")
		else:
			w, h = get_image_dimensions(picture)
			if w != h:
				raise forms.ValidationError("The image must be square")
		return picture
       	