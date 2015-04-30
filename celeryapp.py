"""
This file sets up the environment for the Celery task queue.

You *MUST* import this file when running the oTree project in order to set
everything up. See the default ``wsgi.py`` and ``manage.py`` files for
examples. It's enough to simply put the following line in your startup code::

    import celeryapp

You can adjust this file to configure celery in specific ways, but in general
you can use these settings out of the box for local development or on Heroku.

To run celery, execute::

    ./otree celery worker --app=celeryapp:app --loglevel=INFO

See http://www.celeryproject.org/ for more information.
"""
import os
import otree.celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')


app = otree.celery.setup_celery_app()
app.conf.update(
    CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend',
)
