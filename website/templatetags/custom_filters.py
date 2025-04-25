from django import template

register = template.Library()

@register.filter
def star_rating(value):
    return "⭐" * value + "☆" * (5 - value)