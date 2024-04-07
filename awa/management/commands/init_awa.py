from django.core.management.base import BaseCommand, CommandError
from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model
from apps.tara.models import ContextRoot
from awa.settings import config


class Command(BaseCommand):
    help = "Run initialization/sanity checks for AWA"

    def handle(self, *args, **kwargs):
        self.fix_sites()
        self.check_default_admin()
        self.create_default_pages()

    def create_default_pages(self):
        for root in ContextRoot.objects.all():
            page = Page()


    def check_default_admin(self):
        self.stdout.write("checking if a default admin exists")
        UserClass = get_user_model()
        user, is_new = UserClass.objects.get_or_create(username=config.admin_user)
        if is_new:
            user.is_superuser = True
            user.is_staff = True
            user.is_active = True
            user.set_password(config.admin_password)
            user.save()
            self.stdout.write(
                self.style.SUCCESS(f"default admin {config.admin_user} was created")
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f"existing user {config.admin_user} not modified")
            )

    def fix_site(self, domain, project, primary=False):
        self.stdout.write(f'{project.slug} :: {domain} {primary and "(PRIMARY)" or ""}')
        if primary:
            site, is_new = Site.objects.get_or_create(id=1)
            site.name = domain
            site.domain = domain
            site.save()
            if is_new:
                self.stdout.write("site 1 was created (??)")
            self.stdout.write(self.style.SUCCESS(f"primary site {domain} assimilated"))
        else:
            site, is_new = Site.objects.get_or_create(name=project.slug, domain=domain)
        if is_new:
            self.stdout.write(f"site {site.id} was created for domain {domain}")
        else:
            self.stdout.write(f"site {site.id} existed for domain {domain}")
        return site

    def fix_sites(self):
        try:
            self.stdout.write("doing stuff with sites")

            primary = True
            for project in config.projects:
                project_context = ContextRoot.objects.create(name=project.name)
                for domain in project.domains:
                    site = self.fix_site(domain, project, primary)
                    project_context.sites.add(site)
                    primary = False
                project_context.save()

            self.stdout.write(self.style.SUCCESS("complete."))
        except CommandError as e:
            self.stderr.write(self.style.ERROR(e))
