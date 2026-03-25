from celery import shared_task

from game.repositories import get_catalog_repository


@shared_task(name="tasks.update_games_catalog")
def update_bgg_catalog():
    repository = get_catalog_repository()
    repository.update_catalog()
