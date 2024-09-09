
CMD_MAKEMIGRATIONS := python manage.py makemigrations
CMD_MIGRATE := python manage.py migrate
CMD_START_API := python manage.py runserver

makemigrations:
	$(CMD_MAKEMIGRATIONS)

migrate:
	$(CMD_MIGRATE)

start-api:
	$(CMD_MAKEMIGRATIONS)
	$(CMD_MIGRATE)
	$(CMD_START_API)

run-celery-worker:
	celery -A src.media_service worker -l INFO -Q tasks,dead_letter

run-unittest:
	coverage run --source='.' manage.py test src
	coverage report

run-unittest-details:
	coverage run --source='.' manage.py test src -v 2
	coverage report
