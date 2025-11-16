from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def querystring_replace(context, **kwargs):
    """
    Update or remove querystring parameters from within templates.
    Usage:
        {% querystring_replace status='READING' %}
        {% querystring_replace tag=None %}
    """
    request = context.get('request')
    if request is None:
        return ''

    query = request.GET.copy()
    for key, value in kwargs.items():
        if value is None:
            query.pop(key, None)
        else:
            query[key] = value

    encoded = query.urlencode()
    return f"?{encoded}" if encoded else ''
