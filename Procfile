web: gunicorn core.wsgi
worker: celery -A core worker -B --loglevel=info