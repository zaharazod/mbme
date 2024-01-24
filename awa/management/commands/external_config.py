from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = "Create external configuration (e.g. Apache)"

    def handle(self, *args, **kwargs):
        pass
