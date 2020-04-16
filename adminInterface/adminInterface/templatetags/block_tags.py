from django import template

register = template.Library()

@register.inclusion_tag('navigation.html')
def navigation():
    data = ['start','page2']
    return {'links':data}

# funkar ej, raderar om jag inte får det att funka 
