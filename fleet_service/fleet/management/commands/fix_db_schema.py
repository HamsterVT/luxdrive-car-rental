from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Fixes database schema by dropping rental table and clearing migration history for fleet app'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting database schema fix...')
        
        with connection.cursor() as cursor:
            # 1. Drop the table with incorrect schema
            self.stdout.write('Dropping fleet_rentalrecord table...')
            cursor.execute("DROP TABLE IF EXISTS fleet_rentalrecord;")
            
            # 2. Clear migration history for fleet app so Django reapplies 0001_initial
            self.stdout.write('Clearing migration history for fleet app...')
            cursor.execute("DELETE FROM django_migrations WHERE app = 'fleet';")
            
        self.stdout.write(self.style.SUCCESS('Successfully dropped table and cleared migration history. Now run python manage.py migrate to recreate tables.'))
