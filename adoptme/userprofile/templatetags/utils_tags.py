from django import template
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from shelter.models import Shelter

register = template.Library()


@register.simple_tag
def get_GET_value(request, key):
    return request.GET.get(key)

@register.simple_tag
def get_value_from_iterable(tuple, index):
    return tuple[index]

@register.simple_tag
def get_shelter(id):
    return get_object_or_404(Shelter, pk=id)