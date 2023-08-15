from django import template
from django.core.paginator import Paginator

register = template.Library()


@register.simple_tag
def get_GET_value(request, key):
    return request.GET.get(key)

