from celery import shared_task

from game.repositories import get_catalog_repository


@shared_task(name="tasks.update_games_catalog")
def update_bgg_catalog(batch_count=10):
    get_catalog_repository(batch_count)
