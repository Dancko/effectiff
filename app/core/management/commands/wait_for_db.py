"""
Command to wait for the database to be available before starting the app.
"""

import time
from psycopg2 import OperationalError as PsycopgError
from django.db.utils import OperationalError
from django.db import connection
from django.core.management.base import BaseCommand, CommandParser


class Command(BaseCommand):
    """Django command to wait for db."""

    help = "Django command to wait for db."

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "--sleep", type=int, default=1, help="Sleep duration for simulating delay"
        )

    def handle(self, *args, **options):
        """Entrypoint for command."""
        self.stdout.write("Waiting for the database...")
        db_up = False

        while db_up is False:
            try:
                self.check(databases=["default"])
                connection.ensure_connection()
                db_up = True
            except (PsycopgError, OperationalError):
                self.stdout.write(
                    f"Database unavailable. \
                                  Waiting for {options['sleep']} seconds..."
                )
                time.sleep(options["sleep"])

        self.stdout.write(self.style.SUCCESS("Database available!"))
