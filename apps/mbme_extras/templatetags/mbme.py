import re
from django.template import Library
from django.template.defaultfilters import stringfilter
from django.conf import settings
from vaticinator.vaticinator import Vaticinator

register = Library()
vaticinator = Vaticinator()

@register.simple_tag
def random_fortune(*args, **kwargs):
    vaticinator.set_default_options()
    vaticinator.process_options(*args, **kwargs)
    return vaticinator.fortune


@register.filter(is_safe=True)
@stringfilter
def image_click(html, func):
    return re.sub(r'<img.*src="data:image\/([a-zA-Z]*);base64,([^"]*)"s>',
                  f'<img src="data:image/\1;base64,\2" onclick="{func}" />',
                  html)
