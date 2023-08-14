from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse


class SexChoices(models.TextChoices):
        MALE = 'M', 'Male'
        FEMALE = 'F', 'Female'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    about = models.TextField(blank=True)
    profile_pic = models.ImageField(null=True, blank=True, upload_to="photos/%Y/%m/%d/")
    sex = models.CharField(max_length=1, choices=SexChoices.choices, default=SexChoices.MALE)

    def __str__(self) -> str:
        return self.user.username

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = "Users"

    def get_absolute_url(self):
        return reverse('profile:profile', kwargs={'profile_slug': self.slug})


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, slug=instance.username)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()



    

