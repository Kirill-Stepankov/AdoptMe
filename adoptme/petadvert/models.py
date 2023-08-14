from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from userprofile.models import SexChoices, Profile

class PetAdvert(models.Model):
    class TypeChoices(models.TextChoices):
        CAT = 'CAT', 'Cat'
        DOG = 'DOG', 'Dog'
        HORSE = 'HRS', 'Horse'
        BIRD = 'BRD', 'Bird'
        EXOTIC = 'EXC', 'Exotic'

    class SizeChoices(models.TextChoices):
        SMALL = 'SML', 'Small'
        MEDIUM = 'MDM', 'Medium'
        LARGE = 'LRG', 'Large'
        EXTRA_LARGE = 'XXL', 'Extra large'

    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='owner')
    name = models.CharField(max_length=30)
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/")
    color = models.CharField(max_length=30)
    about = models.TextField(blank=True)
    gender = models.CharField(max_length=1, choices=SexChoices.choices, default=SexChoices.MALE)
    type = models.CharField(max_length=3, choices=TypeChoices.choices, default=TypeChoices.CAT)
    size = models.CharField(max_length=3, choices=SizeChoices.choices, default=SizeChoices.MEDIUM)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    age = models.IntegerField(default=1, validators=[
            MaxValueValidator(100),
            MinValueValidator(1)
        ])
    house_trained = models.BooleanField()
    health = models.CharField(max_length=150)
    breed = models.CharField(max_length=150)
    city = models.CharField(max_length=100)
    
class PetAdvertPhoto(models.Model):
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/")
    pet_advert = models.ForeignKey(PetAdvert, on_delete=models.CASCADE, related_name='photos')