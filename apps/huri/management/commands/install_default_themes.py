from typing import Any
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError, CommandParser

command_path = Path(__file__)
app_path = command_path / ".." / ".." / ".."
theme_root = command_path / "resources" / "themes"


class Command(BaseCommand):
    help = "install default UI themes"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "-t",
            "--theme",
            nargs=1,
            required=False,
            action="store",
            choices=[p.name for p in theme_root.glob("*")],
        )
        parser.add_argument(
            "-l",
            "--list",
            action="store_true",
            nargs=0,
            required=False,
        )

        return super().add_arguments(parser)

    def handle(self, *args: Any, **options: Any) -> str | None:
        return super().handle(*args, **options)
