# from django.contrib.gis.db import models
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from userprofile.models import SexChoices, Profile
from shelter.models import Shelter

class PetAdvert(models.Model):
    class AdvertType(models.TextChoices):
        SITTER = 'SIT', 'Sitter Ad'
        PET = 'PET', 'Pet Ad'

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

    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='owner', null=True, blank=True)
    shelter = models.ForeignKey(Shelter, on_delete=models.CASCADE, related_name='shelter_owner', null=True, blank=True)
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, related_name='author', null=True, blank=True)
    is_published = models.BooleanField(default=True)

    # pet advert fields
    name = models.CharField(max_length=30, null=True)
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", null=True)
    color = models.CharField(max_length=30, null=True)
    about = models.TextField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=SexChoices.choices, default=SexChoices.MALE, null=True)
    type = models.CharField(max_length=3, choices=TypeChoices.choices, default=TypeChoices.CAT, null=True)
    size = models.CharField(max_length=3, choices=SizeChoices.choices, default=SizeChoices.MEDIUM, null=True)
    age = models.IntegerField(default=1, validators=[
            MaxValueValidator(100),
            MinValueValidator(1)
        ], null=True)
    house_trained = models.BooleanField(default=False)
    health = models.CharField(max_length=150, null=True)
    breed = models.CharField(max_length=150, null=True)

    # sitter advert fields
    content = models.TextField(null=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    experience = models.PositiveIntegerField(default=0, null=True)

    # common
    city = models.CharField(max_length=100, null=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    ad_type = models.CharField(max_length=3, choices=AdvertType.choices, default=AdvertType.PET)

    class Meta:
        ordering = ['time_create']

    def __str__(self):
        if self.name:
            return self.name
        return str(self.owner) + ": $" + str(self.salary)


    
class PetAdvertPhoto(models.Model):
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/")
    pet_advert = models.ForeignKey(PetAdvert, on_delete=models.CASCADE, related_name='photos')


class SitterAd(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sitterads')
    content = models.TextField()
    city = models.CharField(max_length=50)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    experience = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return str(self.owner) + " -- $" + str(self.salary)
