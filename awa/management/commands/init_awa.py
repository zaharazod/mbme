from django.core.management.base import BaseCommand, CommandError
from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model
from logging import info, debug, getLogger, DEBUG, INFO

from django.core.management.base import BaseCommand, CommandError
from django.contrib.sites.models import Site

from apps.ara.models import ContextRoot, ContentNode
from apps.tuhi.models import Page
from awa.settings import config

log = getLogger("django")
log.level = INFO


class Command(BaseCommand):
    help = "Run initialization/sanity checks for AWA"

    def handle(self, *args, **kwargs):
        self.fix_sites()
        self.check_default_admin()

    def check_default_admin(self):
        self.stdout.write("checking if a default admin exists")
        UserClass = get_user_model()
        admin_user = config.admin_user or 'admin'
        user, is_new = UserClass.objects.get_or_create(username=admin_user)
        if is_new:
            user.is_superuser = True
            user.is_staff = True
            user.is_active = True
            user.set_password(config.admin_password)
            user.save()
            self.stdout.write(
                self.style.SUCCESS(
                    f"default admin {admin_user} was created")
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f"existing user {config.admin_user} not modified")
            )

    def create_site_contexts(self):
        projects = config.projects or [config.project or None]
        primary = True

        for project in projects:
            root, root_new = ContextRoot.objects.get_or_create(
                name=project.name)
            if root_new:
                page = Page(title='home', slug='index')
                pnf = Page(title='Page not found', slug='404')
                root.content_object = page
                root.save()
                info(f"Project {project.name}... created.")
            else:
                info(f"Project {project.name}... found.")

            for domain in project.domains:
                site, site_new = Site.objects.get_or_create(
                    domain=domain, name=project.slug
                ) if not primary else Site.objects.get_or_create(id=1)
                if primary:
                    site.domain = domain
                    site.name = project.slug
                if site_new:
                    site.save()
                    info(f"  Site {site.name} ({site.domain})... created.")
                else:
                    info(f"  Site {site.name} ({site.domain})... found.")
                root.sites.add(site)
                primary = False

    def fix_site(self, domain, project, primary=False):
        self.stdout.write(f'{project.slug} :: {domain} {
                          primary and "(PRIMARY)" or ""}')
        if primary:
            site, is_new = Site.objects.get_or_create(id=1)
            site.name = domain
            site.domain = domain
            site.save()
            if is_new:
                self.stdout.write("site 1 was created (??)")
            self.stdout.write(self.style.SUCCESS(
                f"primary site {domain} assimilated"))
        else:
            site, is_new = Site.objects.get_or_create(
                name=project.slug, domain=domain)
        if is_new:
            self.stdout.write(
                f"site {site.id} was created for domain {domain}")
        else:
            self.stdout.write(f"site {site.id} existed for domain {domain}")
        return site

    def fix_sites(self):
        try:
            self.stdout.write("doing stuff with sites")

            primary = True
            # TODO only create pages if they don't exist
            for project in config.projects:
                try:
                    project_context = ContextRoot.objects.get(
                        name=project.name)
                except ContextRoot.DoesNotExist:
                    project_context = ContextRoot(name=project.name)
                    home_page = Page.objects.create(
                        title=f"Home - {project.name}",
                        slug="index")
                    project_context.content = home_page
                    project_context.save()
                    pnf = Page(title="Page not found")
                    pnf.parent_context = project_context
                    pnf.context_path = "404"
                    pnf.save()

                for domain in project.domains:
                    site = self.fix_site(domain, project, primary)
                    project_context.sites.add(site)
                    primary = False
                project_context.save()

            self.stdout.write(self.style.SUCCESS("complete."))
        except CommandError as e:
            self.stderr.write(self.style.ERROR(e))
