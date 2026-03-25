from django.core.management.base import BaseCommand

from game.tasks import update_bgg_catalog


class Command(BaseCommand):
    help = 'Starts board game synchronization from BGG.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting downloading games...'))
        
        update_bgg_catalog()
        
        self.stdout.write(self.style.SUCCESS('Synchronization completed successfully!'))
