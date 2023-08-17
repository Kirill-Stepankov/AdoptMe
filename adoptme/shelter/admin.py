from django.contrib import admin
from .models import Shelter, ShelterPhoto, ShelterProfile, ShelterApply
# from django.contrib.gis.admin import OSMGeoAdmin


# @admin.register(Shelter)
# class ShelterAdmin(OSMGeoAdmin):
#     list_display = ('name', 'location')

admin.site.register(Shelter)
admin.site.register(ShelterPhoto)
admin.site.register(ShelterProfile)
admin.site.register(ShelterApply)