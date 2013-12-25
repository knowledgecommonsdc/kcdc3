# Sorts a list at random
# Not original - see http://stackoverflow.com/questions/7162629/django-shuffle-in-templates

from django import template
import random

register = template.Library()

@register.filter
def shuffle(arg):
    tmp = [i for i in arg]
    random.shuffle(tmp)
    return tmp
    


