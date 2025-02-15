#!/bin/sh

# Collect static files
echo "system check"
python manage.py check
echo


echo "Collect static files"
python manage.py collectstatic --noinput
echo


echo "Apply database migrations"
python manage.py migrate
echo


echo "Compile messages (translations)"
python manage.py compilemessages
echo


echo "Create admin superuser if absent"
python manage.py createsuperuser --no-input --username admin
echo

echo "Init/Update Sirene"
python manage.py cavaliba_update
echo


# Start server
echo "Starting server"
#python manage.py runserver 0.0.0.0:8001
gunicorn core.wsgi:application --bind 0.0.0.0:8001 --log-level info --workers 4 --access-logfile '-' --error-logfile '-' --graceful-timeout 2