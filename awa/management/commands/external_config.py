import sys
import argparse
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.template import Context  # Template,
from django.template.loader import get_template
# from django.conf import settings


from awa.settings import config as default_config
from awa.util import AwaConfig


class Command(BaseCommand):
    help = "Create external server configuration"
    app_choices = {'apache': 'apache.conf.j2'}

    def add_arguments(self, parser):
        parser.add_argument(
            "-c", "--config",
            help="Path to alternate Awa config",
            type=argparse.FileType('r'),
        )
        parser.add_argument(
            "-o", "--output",
            help="Path to output file",
            type=argparse.FileType('w'),
            default=sys.stdout
        )
        parser.add_argument(
            "-t", "--type",
            help="Application type to configure",
            choices=self.app_choices.keys(), type=str,
            required=True
        )

    def handle(self, **kw):
        try:
            config = AwaConfig(path=kw['config']) \
                if kw['config'] else default_config
            out = kw['output'] or sys.stdout
            template_name = f'awa/config/{self.app_choices[kw["type"]]}'
            template = get_template(template_name)
            root_path = Path(__file__). \
                parent.parent. \
                parent.parent.resolve()
            storages = dict([
                (k, s) for k, s in config.storage.items()
                if isinstance(s, dict)
                and s.type == 'external'
            ])
            env_path = config.storages.env.root or '.env'
            if not env_path.startswith('/'):
                env_path = root_path / env_path
            context = {
                'project_path': root_path,
                'project_env': env_path,
                'config': config,
                'storages': storages
            }
            output = template.render(context)
            print(output, file=out)
        except Exception as e:
            raise e if config.debug else CommandError(e)
