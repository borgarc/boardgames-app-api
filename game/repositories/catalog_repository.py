from abc import ABC, abstractmethod


class CatalogRepository(ABC):
    @abstractmethod
    def update_catalog(self):
        """Abstract method to implement the update catalog"""
