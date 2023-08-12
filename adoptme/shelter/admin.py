from django.contrib import admin
from .models import Shelter, ShelterPhoto, ShelterProfile

admin.site.register(Shelter)
admin.site.register(ShelterPhoto)
admin.site.register(ShelterProfile)