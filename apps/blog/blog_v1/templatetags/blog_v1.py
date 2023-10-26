import re
from django.template import Library
from django.template.defaultfilters import stringfilter

register = Library()


@register.filter(is_safe=True)
@stringfilter
def lightbox(html, label):
    return re.sub(r'<img ([^>]*)>',
                  '<img data-lily \\1>',
                  html)
    # return re.sub(r'<img ([^>]*)>',
    #               f'<img data-lightbox="{label}" \\1>',
    #               html)
