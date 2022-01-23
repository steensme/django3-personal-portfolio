from django import template
from ..models import Blog
register = template.Library()
# @register.simple_tag

# from django.utils.safestring import mark_safe
from django.template.defaultfilters import stringfilter
import markdown as md
@register.filter()
@stringfilter
def markdown(value):
    return md.markdown(value, extensions=['markdown.extensions.fenced_code'])
