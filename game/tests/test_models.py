"""
Tests for the models in the game app.
"""

from django.db.utils import IntegrityError
from django.test import TestCase

from game.models import BoardGame


class BoardGameModelTest(TestCase):

    def setUp(self):
        """Initial conf for the tests."""
        self.game_data = {
            "bgg_id": 174430,
            "name": "Gloomhaven",
            "year_published": 2017,
            "rating": 8.7
        }
        self.game = BoardGame.objects.create(**self.game_data)

    def test_boardgame_creation(self):
        """Object created with the basic data."""
        self.assertTrue(isinstance(self.game, BoardGame))
        self.assertEqual(self.game.__str__(), self.game.name)

    def test_default_values(self):
        """Default values as rating works."""
        game_no_rating = BoardGame.objects.create(bgg_id=1, name="Test Game")
        self.assertEqual(game_no_rating.rating, 0.0)

    def test_bgg_id_uniqueness(self):
        """Cant duplicate bgg_id."""
        with self.assertRaises(IntegrityError):
            BoardGame.objects.create(
                bgg_id=174430,
                name="Duplicate Game"
            )

    def test_nullable_fields(self):
        """Optional fields None."""
        try:
            game = BoardGame.objects.create(
                bgg_id=999,
                name="Minimal Game",
                description=None,
                min_players=None,
                image_url=None
            )
            self.assertIsNone(game.description)
        except Exception as e:
            self.fail(f"Optional field creation failed with: {e}")

    def test_string_representation(self):
        """__str__ returns name."""
        self.assertEqual(str(self.game), "Gloomhaven")

    def test_auto_now_updated(self):
        """Checks that last_updated is automatically updated."""
        old_update = self.game.last_updated
        self.game.name = "Gloomhaven Second Edition"
        self.game.save()
        self.assertGreater(self.game.last_updated, old_update)
