from django import template
from django.core.paginator import Paginator

register = template.Library()


@register.simple_tag
def is_shelter_admin(shelter, profile):
    return shelter.shelter.filter(profile=profile).first().role == shelter.shelter.first().RoleChoices.ADMIN

@register.simple_tag
def is_participated(mod, shelter_id):
    return mod.profile.filter(shelter__id=shelter_id).first()


