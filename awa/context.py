from functools import cache
from .models import SocialLink
# from django.conf import settings


@cache
def awa(request):
    return {
        'awa': {
            'social': SocialLink.objects.all().order_by('pk'),
        },
    }
