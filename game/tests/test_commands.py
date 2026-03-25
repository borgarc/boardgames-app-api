"""
Test custom Django management commands.
"""

from io import StringIO
from unittest.mock import patch

from django.core.management import call_command
from django.test import TestCase


class SyncBggCommandTest(TestCase):

    @patch('game.tasks.update_bgg_catalog')
    def test_sync_bgg_command_calls_task(self, mock_update_task):
        """Checks command it executed once."""
        
        out = StringIO()
        
        call_command('sync_test', stdout=out)

        mock_update_task.assert_called_once()

        output = out.getvalue()
        self.assertIn('Starting downloading games...', output)
        self.assertIn('Synchronization completed successfully!', output)
