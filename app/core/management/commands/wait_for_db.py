"""
Command to wait for the database to be available before starting the app.
"""

import time
from psycopg2 import OperationalError as PsycopgError
from django.db.utils import OperationalError
from django.db import connection
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to wait for db."""

    def handle(self, *args, **options):
        """Entrypoint for command."""
        self.stdout.write("Waiting for the database...")
        db_up = False

        while db_up is False:
            try:
                self.check(databases=['default'])
                connection.ensure_connection()
                db_up = True
            except (PsycopgError, OperationalError):
                self.stdout.write("Database unavailable. \
                                  Waiting for 1 second...")
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("Database available!"))
