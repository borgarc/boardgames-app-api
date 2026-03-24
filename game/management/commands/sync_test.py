from django.core.management.base import BaseCommand

from game.tasks import update_bgg_catalog


class Command(BaseCommand):
    help = 'Starts board game synchronization from BGG.'

    def add_arguments(self, parser):
        # Allows passing the number of batches as an optional argument.
        parser.add_argument(
            'batches', 
            type=int, 
            nargs='?', 
            default=1, 
            help='Number of 20-game batches to download (default: 1).'
        )

    def handle(self, *args, **options):
        batches = options['batches']
        self.stdout.write(self.style.SUCCESS(f'Starting download of {batches * 20} games...'))
        
        # Executing the function directly (synchronously) to monitor progress in the console.
        update_bgg_catalog(batch_count=batches)
        
        self.stdout.write(self.style.SUCCESS('Synchronization completed successfully!'))
