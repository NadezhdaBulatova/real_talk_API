"""
Test custom Django management commands.
"""
from unittest.mock import patch
from psycopg2 import OperationalError as Psycopg2Error
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


@patch('core.management.commands.check_db_status.Command.check')
class CommandTest(SimpleTestCase):
    def test_check_db_status(self, patched_check):
        """Test the status of the DB"""
        patched_check.return_value = True
        call_command('check_db_status')
        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_check_db_status_delay(self, patched_sleep, patched_check):
        """Test the status of the DB when getting OperationalError"""

        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]
        call_command('check_db_status')
        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
