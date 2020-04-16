from django import template

register = template.Library()

@register.inclusion_tag("navigation_bar.html", takes_context=True)
def navigation_bar(context):
    links = {
        'Start': "/start",
        'Nåt annat': "/page2"
    }
    return {
        'links': links,
        'request': context['request']
    }

# funkar ej, raderar om jag inte får det att funka 
