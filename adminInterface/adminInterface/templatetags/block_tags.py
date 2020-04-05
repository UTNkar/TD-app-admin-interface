from django import template

register = template.Library()

@register.inclusion_tag('navigation_bar.html')
def navigation_bar():
    data = ['start','page2']
    return {'links':data}
