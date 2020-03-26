#!/bin/bash

sleep 5

python manage.py db migrate

python manage.py db upgrade

# run server
python run.py

#run celery beat
celery -A app.celery beat -l info

# run celery worker
celery -A app.celery worker -l info
