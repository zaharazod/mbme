from awa.settings import config
from logging import info, debug, getLogger, DEBUG, INFO

from django.core.management.base import BaseCommand, CommandError, CommandParser
from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model

from apps.ara.models import ContextRoot
from apps.tuhi.models import Page

log = getLogger("django")
log.level = INFO


class Command(BaseCommand):
    help = "Run initialization/sanity checks for AWA"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('-c', '--clean', action='store_true')
        return super().add_arguments(parser)

    def handle(self, *args, **kwargs):
        if (kwargs['clean']):
            ContextRoot.objects.all().delete()  # self.clean()
        self.admin = self.check_default_admin()
        self.fix_sites()

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
        return user

    def fix_sites(self):
        try:
            self.stdout.write("checking site configurations")

            # TODO only create pages if they don't exist
            for project in config.projects:
                project_context, ctx_is_new = \
                    ContextRoot.objects.get_or_create(
                        project_name=project.name)
                if ctx_is_new:
                    home_page = Page(
                        title=f"Home | {project.name}",
                        slug="index",
                        created_by=self.admin)
                    home_page.parent_context = project_context
                    home_page.save()
                    pnf = Page(
                        title=f"Page not found | {project.name}",
                        slug="404",
                        created_by=self.admin)
                    pnf.parent_context = project_context
                    pnf.save()

                project_context.sites.clear()
                for domain in project.domains:
                    site, site_is_new = Site.objects.get_or_create(
                        name=project.slug, domain=domain)
                    project_context.sites.add(site)
                project_context.save()

            self.stdout.write(self.style.SUCCESS("complete."))
        except CommandError as e:
            self.stderr.write(self.style.ERROR(e))
