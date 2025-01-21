from functools import cache

# from .models import ProjectLink

# from django.conf import settings
from django.contrib.sites.models import Site
from awa.settings import config


@cache
def awa(request):
    site = Site.objects.get_current(request)
    project = config.get_current_project(request)
    return {
        "links": {
            # "header": ProjectLink.objects.filter(header=True).order_by("pk"),
            # "footer": ProjectLink.objects.filter(
            #     header=False, icon__isnull=True
            # ).order_by("pk"),
            # "icons": ProjectLink.objects.filter(
            #     header=False, icon__isnull=False
            # ).order_by("pk"),
        },
        "site": site,
        "config": config,
        "project": project,
    }
