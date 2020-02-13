init:
	( \
		python3 -m pip install --user virtualenv; \
		python3 -m venv flybob-env; \
		. flybob-env/bin/activate; \
		pip3 install -r requirements.txt; \
	)

migrate:
	( \
		python3 manage.py db migrate; \
		python3 manage.py db upgrade; \
	)

test:
	nosetests

start:
	python3 application.py

redis-start:
	redis-server

celery:
	( \
		celery -A app.celery beat -l info; \
		celery -A app.celery worker -l info; \
	)

