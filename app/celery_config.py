"""
Config for celery and Cron jobs
"""

import os

from celery.schedules import crontab

# Broker & Backend
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://redis:6379/0')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://redis:6379/0')

# General Settings
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
CELERY_TASK_SOFT_TIME_LIMIT = 300
CELERY_RESULT_EXPIRES = 3600

# Cron Jobs (Beat Schedule)

CELERY_BEAT_SCHEDULE = {
    'import-bgg-games-weekly': {
        'task': 'tasks.update_games_catalog',
        'schedule': crontab(minute=0, hour=4, day_of_week='friday'),
        'args': (5,),
    },
}
