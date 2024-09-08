
run-celery-worker:
	celery -A src.media_service worker -l INFO -Q tasks,dead_letter
