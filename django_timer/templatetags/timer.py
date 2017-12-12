
from django import template

register = template.Library()

@register.inclusion_tag('django_timer/timer.html')
def render_timer(timer):
    return {'timer': timer}