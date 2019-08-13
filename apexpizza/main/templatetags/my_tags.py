from django import template
import locale
try:
    locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')  # Use '' for auto, or force e.g. to 'en_US.UTF-8'
except Exception as e:
    locale.setlocale(locale.LC_ALL, 'Russian')  # Use '' for auto, or force e.g. to 'en_US.UTF-8'
    



register = template.Library()

@register.simple_tag
def multi(a,b):
    
    return '{:n}'.format(float(a) * float(b))

@register.simple_tag
def available(a):
    if len(a)>0:
        return True
    else:
        return False

    