import os
#my comment here
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

from django.core.wsgi import get_wsgi_application

# Make sure the celery app is loaded.
import celeryapp

from dj_static import Cling
application = Cling(get_wsgi_application())
