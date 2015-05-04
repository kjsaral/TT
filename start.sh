#!/bin/bash

trap killgroup SIGINT

killgroup(){
  echo killing...
  kill 0
}

web() {
    newrelic-admin run-program gunicorn wsgi
}

worker() {
    python manage.py celery worker --app=celeryapp:app --loglevel=INFO
}

web &
worker &
wait
