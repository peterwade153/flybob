from datetime import timedelta

import app
from app.tasks import flight_reminder

# CELERY_IMPORTS = ('tasks')
CELERY_TASK_RESULT_EXPIRES = 30
CELERY_TIMEZONE = 'UTC'

CELERY_ACCEPT_CONTENT = ['json', 'msgpack', 'yaml']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERYBEAT_SCHEDULE = {
        'once-a-day': {
            'task': 'app.tasks.flight_reminder',
            'schedule': timedelta(hours=24)
        },
    }