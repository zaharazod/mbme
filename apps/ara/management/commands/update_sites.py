from logging import info, debug, getLogger, DEBUG, INFO

from django.core.management.base import BaseCommand, CommandError
from django.contrib.sites.models import Site

from awa.settings import config

from ...models import ContextRoot, ContextNode

log = getLogger("django")
log.level = INFO


class Command(BaseCommand):
    help = "Create or update site and context objects"

    def handle(self, *args, **kwargs):
        # TODO: actually handle config.projects elsewhere
        projects = config.projects or [config.project or None]
        for project in projects:
            root, root_new = ContextRoot.objects.get_or_create(
                name=project.name)
            if root_new:
                root.save()
                info(f"Project {project.name}... created.")
            else:
                info(f"Project {project.name}... found.")
            for domain in project.domains:
                site, site_new = Site.objects.get_or_create(
                    domain=domain, name=project.name
                )
                if site_new:
                    site.save()
                    info(f"  Site {site.name} ({site.domain})... created.")
                else:
                    info(f"  Site {site.name} ({site.domain})... found.")
                root.sites.add(site)
            ContextNode.objects.get_context_for_object(root, create=True)

        info("Done!")
