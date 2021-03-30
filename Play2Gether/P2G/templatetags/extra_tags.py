from django import template
from P2G.models import Category, Game, User, UserProfile, Group, Message, Score

register = template.Library()

@register.simple_tag
def get_keys(dictionary):
    return dictionary.keys()

@register.simple_tag
def get_values(dictionary):
    return dictionary.values()


