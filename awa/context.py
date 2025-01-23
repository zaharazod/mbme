from functools import cache

from .models import Link

# from django.conf import settings
from django.contrib.sites.models import Site
from awa.settings import config


@cache
def awa(request):
    site = Site.objects.get_current(request)
    project = config.get_current_project(request)
    return {
        "links": {
            "header": Link.objects.filter(role="header"),
            "footer": Link.objects.filter(role="footer", icon__isnull=True),
            "icons": Link.objects.filter(role="footer", icon__isnull=False),
        },
        "site": site,
        "config": config,
        "project": project,
    }
