from django import template
from django.core.paginator import Paginator

register = template.Library()


@register.simple_tag
def is_shelter_admin(shelter, request):
    return shelter.shelter.filter(profile=request.user.profile).first().role == shelter.shelter.first().RoleChoices.ADMIN

