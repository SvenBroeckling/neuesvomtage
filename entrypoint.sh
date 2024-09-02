#!/bin/sh

/venv/bin/python manage.py migrate
/venv/bin/python manage.py collectstatic --noinput

/venv/bin/gunicorn neuesvomtage.asgi:application --bind 0.0.0.0:8080 -w 7 -k uvicorn.workers.UvicornWorker
