web: gunicorn wsgi
worker: python manage.py celery worker --app=celeryapp:app --loglevel=INFO
