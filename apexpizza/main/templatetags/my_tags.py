from django import template
register = template.Library()

@register.simple_tag(name="get_objects")
def get_objects(value):
    
    return "<button>PUSH</button>"