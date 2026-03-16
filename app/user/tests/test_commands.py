"""
Test custom Django management commands.
"""
from unittest.mock import patch

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase
from psycopg2 import OperationalError as Psycopg2OpError


@patch('user.management.commands.wait_for_db.connections')
class CommandTests(SimpleTestCase):
    """Test commands."""

    def test_wait_for_db_ready(self, patched_connections):
        """Test waiting for db when db is ready."""
        patched_connections.__getitem__.return_value.cursor.return_value = True

        call_command('wait_for_db')

        patched_connections.__getitem__.assert_called_once_with('default')

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_connections):
        """Test waiting for db when getting OperationalError."""
        patched_connections.__getitem__.return_value.cursor.side_effect = [Psycopg2OpError] * 2 + \
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_connections.__getitem__.return_value.cursor.call_count, 6)
        patched_connections.__getitem__.assert_called_with('default')
