from django.contrib import admin
from .models import Profile, PetAdvert, PetAdvertPhoto

admin.site.register(Profile)
admin.site.register(PetAdvert)
admin.site.register(PetAdvertPhoto)