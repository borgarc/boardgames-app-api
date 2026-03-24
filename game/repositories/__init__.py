from abc import ABC, abstractmethod

from app.settings import GAME_CATALOG_SOURCE
from game.repositories import bgg_catalog_repository, csv_catalog_repository


def get_catalog_repository():
    if GAME_CATALOG_SOURCE == 'CSV':
        return csv_catalog_repository()
    return bgg_catalog_repository()

class CatalogRepository(ABC):
    @abstractmethod
    def update_catalog(self):
        """Abstract method to implement the update catalog"""
