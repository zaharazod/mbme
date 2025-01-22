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
            # "header": Link.objects.get(name="header"),
            # "footer": Link.objects.filter(icon__isnull=True
            # ).order_by("pk"),
            # "icons": Link.objects.filter(
            #     header=False, icon__isnull=False
            # ).order_by("pk"),
        },
        "site": site,
        "config": config,
        "project": project,
    }
