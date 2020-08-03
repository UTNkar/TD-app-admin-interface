from django import template

register = template.Library()


@register.inclusion_tag("navigation_bar.html", takes_context=True)
def navigation_bar(context):
    # The links must have the title as the key and the link as the value
    links = {
        'Start': "/start",
        'Sektioner': "/sections",
        'Biljettsläpp': "/ticket-system",
        'Notiser': "/notifications",
    }
    return {
        'links': links,
        'request': context['request']
    }


@register.inclusion_tag("header.html", takes_context=True)
def header(context):
    # The links must have the title as the key and the link as the value
    links = {
        'Start': "/start",
        'Sektioner': "/sections",
        'Biljettsläpp': "/ticket-system"
    }
    return {
        'links': links,
        'request': context['request']
    }
