from app.settings import GAME_CATALOG_SOURCE
from game.repositories.bgg_catalog_repository import BGGCatalogRepository
from game.repositories.csv_catalog_repository import CSVCatalogRepository


def get_catalog_repository():
    if GAME_CATALOG_SOURCE == 'CSV':
        return CSVCatalogRepository()
    return BGGCatalogRepository()
