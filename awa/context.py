from functools import cache
from .models import SocialLink
# from django.conf import settings
from django.contrib.sites.models import Site
from awa.settings import config

@cache
def awa(request):
    return {
        'awa': {
            'social': SocialLink.objects.all().order_by('pk'),
        },
        'site': Site.objects.get_current(),
        'config': config,
    }
