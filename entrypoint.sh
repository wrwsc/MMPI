#!/bin/sh

echo "Ожидание postgres..."
while ! nc -z postgres 5432; do
  sleep 1
done
echo "Postgres доступен"

python manage.py migrate --noinput
python manage.py collectstatic --noinput --verbosity 2
gunicorn mmpi.wsgi:application --bind 0.0.0.0:8000
echo "Запуск Nginx"
nginx -g "daemon off;"
