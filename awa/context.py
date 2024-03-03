from functools import cache
from .models import BrandLink
# from django.conf import settings
from django.contrib.sites.models import Site
from awa.settings import config

@cache
def awa(request):
    return {
        'awa': {
            # FIXME
            'social': BrandLink.objects.all().order_by('pk'),
        },
        'site': Site.objects.get_current(),
        'config': config,
    }
