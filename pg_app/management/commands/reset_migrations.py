from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Resets the migration history by clearing the django_migrations table'

    def handle(self, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM django_migrations;")
        self.stdout.write(self.style.SUCCESS('Successfully reset migration history'))