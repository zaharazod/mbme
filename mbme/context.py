from functools import cache
from .models import SocialLink
from django.conf import settings


@cache
def mbme(request):
    return {
        'mbme': {
            'social': SocialLink.objects.all(),
        },
    }
