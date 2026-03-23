"""
Board games database models.
"""

from django.db import models


class BoardGame(models.Model):
    bgg_id = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    year_published = models.IntegerField(null=True, blank=True)
    min_players = models.PositiveIntegerField(null=True)
    max_players = models.PositiveIntegerField(null=True)
    playing_time = models.PositiveIntegerField(null=True)  # en minutos
    image_url = models.URLField(max_length=500, null=True, blank=True)
    rating = models.FloatField(default=0.0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
