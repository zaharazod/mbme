
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.template import Template, Context
from django.template.loader import get_template
from django.conf import settings
import sys
import os
import codecs
import json
import argparse

import awa.settings
from awa.util import AwaConfig


class Command(BaseCommand):
    help = "Create external server configuration"
    app_choices = ['apache']

    def add_arguments(self, parser):
        parser.add_argument(
            "-c", "--config",
            help="Path to alternate Awa config",
            type=argparse.FileType('r'),
        )
        parser.add_argument(
            "-o", "--output", help="Path to output file",
            type=argparse.FileType('')
        )
        parser.add_argument(
            "-a", "--app", choices=self.app_choices,
            help="Application to configure", type=str

        )
        parser.add_argument(
            "-v", "--verbose", action="store_true"
        )

    def handle(self, **kw):
        settings.configure(awa.settings)

        self.config = AwaConfig(config_file=kw['config']) \
            if kw['config'] else awa.settings.config
        out = kw['output'] or sys.stdout
