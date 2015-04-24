#import os
#
#
#def setup_celery():
#    # set the default Django settings module for the 'celery' program.
#    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
#
#    from django.conf import settings
#    from celery import Celery
#
#    app = Celery('otree')
#
#    # Using a string here means the worker will not have to
#    # pickle the object when using Windows.
#    app.config_from_object('django.conf:settings')
#    app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
#
#    app.conf.update(
#        CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend',
#    )
#
#
#celery_app = setup_celery()


from __future__ import absolute_import

import os

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

from django.conf import settings

from celery import Celery
app = Celery('otree-lib')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
