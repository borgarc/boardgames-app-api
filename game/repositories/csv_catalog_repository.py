import csv
from pathlib import Path

from django.conf import settings
from django.db import transaction

from game.models import BoardGame
from game.repositories.catalog_repository import CatalogRepository


class CSVCatalogRepository(CatalogRepository):
    def update_catalog(self):
        """
        Read csv from game/resources/ and populate boardgame table on db.
        """

        csv_path = Path(settings.BASE_DIR) / "game" / "resources" / "boardgames_ranks.csv"

        if not csv_path.exists():
            print(f"Error: File not found in {csv_path}.")
            return 0

        games = []

        try:
            with open(csv_path, encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                for row in reader:
                    game = BoardGame(
                        name=row['name'],
                        bgg_id=row['id'],
                        year_published=row['yearpublished'],
                        rating=row['average'],
                    )
                    games.append(game)

            with transaction.atomic():
                created_objs = BoardGame.objects.bulk_create(games, batch_size=500)
                return len(created_objs)

        except Exception as e:
            print(f"Error during import: {e}")
            return 0
