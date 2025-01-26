from functools import cache

from .models import SiteLink

# from django.conf import settings
from django.contrib.sites.models import Site
from awa.settings import config


@cache
def awa(request):
    site = Site.objects.get_current(request)
    project = config.get_current_project(request)
    context = {
        "links": {
            "header": SiteLink.objects.filter(role="header"),
            "footer": SiteLink.objects.filter(role="footer", icon__exact=""),
            "icons": SiteLink.objects.filter(role="footer").exclude(icon__exact=""),
        },
        "site": site,
        "config": config,
        "project": project,
    }
    return context
