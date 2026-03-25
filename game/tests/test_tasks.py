"""
Tests for the tasks in the game app.
"""

from unittest.mock import MagicMock, mock_open, patch

from django.test import TestCase

from game.models import BoardGame
from game.repositories.bgg_catalog_repository import BGGCatalogRepository
from game.repositories.csv_catalog_repository import CSVCatalogRepository


class CSVCatalogRepositoryTest(TestCase):

    def setUp(self):
        self.repository = CSVCatalogRepository()
        self.csv_content = (
            "id,name,yearpublished,average\n"
            "174430,Gloomhaven,2017,8.7\n"
            "161936,Pandemic Legacy: Season 1,2015,8.6\n"
        )

    @patch("game.repositories.csv_catalog_repository.Path.exists")
    def test_update_catalog_file_not_found(self, mock_exists):
        """Checks returns 0 if files doesnt exist."""
        mock_exists.return_value = False
        
        result = self.repository.update_catalog()
        
        self.assertEqual(result, 0)
        self.assertEqual(BoardGame.objects.count(), 0)

    @patch("game.repositories.csv_catalog_repository.Path.exists")
    def test_update_catalog_success(self, mock_exists):
        """Checks registries created on db."""
        mock_exists.return_value = True
        
        with patch("builtins.open", mock_open(read_data=self.csv_content)):
            result = self.repository.update_catalog()

        self.assertEqual(result, 2)
        self.assertEqual(BoardGame.objects.count(), 2)
        
        gloomhaven = BoardGame.objects.get(bgg_id=174430)
        self.assertEqual(gloomhaven.name, "Gloomhaven")
        self.assertEqual(gloomhaven.year_published, 2017)
        self.assertEqual(gloomhaven.rating, 8.7)

    @patch("game.repositories.csv_catalog_repository.Path.exists")
    def test_update_catalog_atomic_transaction(self, mock_exists):
        """If something fails doesnt save anythinf on db."""
        mock_exists.return_value = True
        
        invalid_csv = (
            "id,name,yearpublished,average\n"
            "100,Game 1,2020,5.0\n"
            "invalid_id,Game 2,2020,5.0\n"
        )
        
        with patch("builtins.open", mock_open(read_data=invalid_csv)):
            result = self.repository.update_catalog()

        self.assertEqual(result, 0)
        self.assertEqual(BoardGame.objects.count(), 0)

class BGGCatalogRepositoryTest(TestCase):

    def setUp(self):
        self.repository = BGGCatalogRepository()
        self.mock_xml = """<?xml version="1.0" encoding="utf-8"?>
        <items>
            <item type="boardgame" id="1">
                <name type="primary" value="Gloomhaven" />
                <statistics><ratings><average value="8.7" /></ratings></statistics>
            </item>
            <item type="expansion" id="2">
                <name type="primary" value="Expansion" />
            </item>
        </items>
        """

    @patch('game.repositories.bgg_catalog_repository.requests.Session.get')
    @patch('game.repositories.bgg_catalog_repository.time.sleep')
    def test_update_catalog_success(self, mock_sleep, mock_get):
        """Donwload, create rows and no game expansion its added."""
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = self.mock_xml.encode('utf-8')
        mock_get.return_value = mock_response

        with patch.object(BGGCatalogRepository, '_get_current_id', return_value=1):
            with patch('game.repositories.bgg_catalog_repository.range', return_value=[0]):
                self.repository.update_catalog()

        self.assertEqual(BoardGame.objects.count(), 1)
        self.assertTrue(BoardGame.objects.filter(bgg_id=1).exists())
        self.assertFalse(BoardGame.objects.filter(bgg_id=2).exists())

    @patch('game.repositories.bgg_catalog_repository.requests.Session.get')
    @patch('game.repositories.bgg_catalog_repository.time.sleep')
    def test_update_catalog_rate_limit_429(self, mock_sleep, mock_get):
        """Status code 429 stopsthe process."""
        
        mock_response = MagicMock()
        mock_response.status_code = 429
        mock_get.return_value = mock_response

        self.repository.update_catalog()

        self.assertEqual(BoardGame.objects.count(), 0)

        mock_sleep.assert_called_with(60)

    def test_get_current_id_logic(self):
        """We get the current id."""
        BoardGame.objects.create(bgg_id=50, name="Test")
        self.assertEqual(self.repository._get_current_id(), 51)
