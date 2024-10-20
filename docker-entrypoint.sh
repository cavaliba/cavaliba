#!/bin/sh

# Collect static files
echo "system check"
python manage.py check
echo


echo "Collect static files"
python manage.py collectstatic --noinput
echo

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate
echo

# Compile Messages (translations)
echo "Compile messages (translations)"
python manage.py compilemessages
echo

# Apply database migrations
echo "Init/Update Sirene"
python manage.py sirene_init
echo


# Start server
echo "Starting server"
#python manage.py runserver 0.0.0.0:8001
gunicorn core.wsgi:application --bind 0.0.0.0:8001 --log-level info --workers=2 --access-logfile '-' --error-logfile '-' 