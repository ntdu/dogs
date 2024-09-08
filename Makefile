
run-celery-worker:
	celery -A src.media_service worker -l INFO -Q tasks,dead_letter

run-unittest:
	coverage run --source='.' manage.py test src -v 2
	coverage report
