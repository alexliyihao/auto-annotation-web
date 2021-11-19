from django import template
from django.template.defaulttags import register
import json
register = template.Library()

@register.filter
def get_value(dictionary, key):
    return json.loads(dictionary)[key]
