from django.db import models
from userprofile.models import Profile

class Shelter(models.Model):
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL") 
    name = models.CharField(max_length=50, unique=True)
    main_photo = models.ImageField(upload_to="photos/%Y/%m/%d/")
    #location = 
    email = models.EmailField(unique=True)
    about = models.TextField()
    #phone_number = models.

    def __str__(self):
        return self.name


class ShelterPhoto(models.Model):
    shelter = models.ForeignKey(Shelter, on_delete=models.CASCADE, related_name='shelter_photos')
    image = models.ImageField(upload_to="photos/%Y/%m/%d/")
    time_create = models.DateTimeField(auto_now_add=True)

class ShelterProfile(models.Model):
    class RoleChoices(models.TextChoices):
        ADMIN = 'ADM', 'Admin'
        MODERATOR = 'MOD', 'Moderator'

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile')
    shelter = models.ForeignKey(Shelter, on_delete=models.CASCADE, related_name='shelter')
    role = models.CharField(max_length=3, choices=RoleChoices.choices)