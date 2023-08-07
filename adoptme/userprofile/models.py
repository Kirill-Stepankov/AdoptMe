from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MaxValueValidator, MinValueValidator


class SexChoices(models.TextChoices):
        MALE = 'M', 'Male'
        FEMALE = 'F', 'Female'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    about = models.TextField(blank=True)
    sex = models.CharField(max_length=1, choices=SexChoices.choices, default=SexChoices.MALE)

    def __str__(self) -> str:
        return self.user.username

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = "Users"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, slug=instance.username)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Pet(models.Model):
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

    name = models.CharField(max_length=30)
    about = models.TextField(blank=True)
    gender = models.CharField(max_length=1, choices=SexChoices.choices, default=SexChoices.MALE)
    type = models.CharField(max_length=3, choices=TypeChoices.choices, default=TypeChoices.CAT)
    size = models.CharField(max_length=3, choices=SizeChoices.choices, default=SizeChoices.MEDIUM)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='owner')
    age = models.IntegerField(default=1, validators=[
            MaxValueValidator(100),
            MinValueValidator(1)
        ])
    breed = models.CharField(max_length=100)
    


    

