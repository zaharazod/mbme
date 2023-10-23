import re
from django.template import Library
from django.template.defaultfilters import stringfilter
# from django.conf import settings
from django.utils.safestring import mark_safe

from vaticinator import Vaticinator

register = Library()
vaticinator = Vaticinator()

FONTS = [
    'Shadows+Into+Light',
    'IM+Fell+English+SC',
    'Sedgwick+Ave+Display',
    'Acme',
    'Nothing+You+Could+Do',
    'VT323',
    'Jura',
    'Black+Ops+One',
    'Dosis:wght@200;300;400;500;600;700'
]
FONTS_PER_LINK = 3


@register.simple_tag
def random_fortune(*args, **kwargs):
    vaticinator.set_default_options()
    vaticinator.process_options(*args, **kwargs)
    return vaticinator.fortune


@register.filter(is_safe=True)
@stringfilter
def image_click(html, func):
    return re.sub(r'<img ([^>]*)>',
                  f'<img onclick="{func}" \\1>',
                  html)


@register.filter(is_safe=True)
@stringfilter
def html_attrs(html, element, **kwargs):
    attrs = ' '.join([
        f'{k}="{v}"'
        for k, v in kwargs.items()
    ])
    return re.sub(f'<{element} ([^>]*)>',
                  f'<{element} {attrs} \\1>',
                  html)


@register.simple_tag
def font_links():
    links = [
        '<link rel="preconnect" \
            href="https://fonts.googleapis.com" />',
        '<link rel="preconnect" \
            href="https://fonts.gstatic.com" crossorigin />'
    ]

    # links.append(
    #     '<link href="https://fonts.googleapis.com/css2?'
    #     + "family&".join([font for font in FONTS])
    #     + '&display=swap rel="stylesheet" />'
    # )

    font_list = FONTS.copy()
    while font_list:
        cur_fonts = []
        while font_list:
            cur_fonts.append(font_list.pop())
            if len(cur_fonts) > FONTS_PER_LINK:
                break
        links.append(
            '<link href="https://fonts.googleapis.com/css2?family='
            + ("&family=".join([font for font in cur_fonts]))
            + '&display=swap" rel="stylesheet" />'
        )

    # for font in FONTS:
    #     links.append(
    #         f'<link href="https://fonts.googleapis.com/css2?family={font}&display=swap" rel="stylesheet" / >'
    #     )

    return mark_safe('\n'.join(links))
