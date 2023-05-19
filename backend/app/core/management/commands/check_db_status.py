"""
Custom Django command to check the status of DB
"""

from django.core.management.base import BaseCommand
import time
from psycopg2 import OperationalError as Psycorpg2Error
from django.db.utils import OperationalError


class Command(BaseCommand):

    """Django command to check the DB status"""

    def handle(self, *args, **options):
        self.stdout.write('Waiting for db...')
        db_active = False
        while db_active is False:
            try:
                self.check(databases=['default'])
                db_active = True
            except (Psycorpg2Error, OperationalError):
                self.stdout.write('Db is unavailable, \
                                  wait 1 sec...')
                time.sleep(1)
        self.stdout.write('Db is available')