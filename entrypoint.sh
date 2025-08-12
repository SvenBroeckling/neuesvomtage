#!/bin/sh

/app/.venv/bin/python manage.py migrate
/app/.venv/bin/python manage.py collectstatic --noinput
/app/.venv/bin/python manage.py compress -f

/app/.venv/bin/hypercorn -w 5 -b 0.0.0.0:8080 neuesvomtage.asgi:application
