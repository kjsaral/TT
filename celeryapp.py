import os
import otree.celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')


app = otree.celery.setup_celery_app()
app.conf.update(
    CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend',
)
