#!/bin/bash

if [ $DJANGO_TEST ]; then
    python manage.py test --noinput
    exit 0
fi

python manage.py collectstatic --noinput

python manage.py migrate

export SUPERUSER_NAME_FILE=/run/secrets/superuser_name
export SUPERUSER_PASSWORD_FILE=/run/secrets/superuser_password

if [ -f $SUPERUSER_NAME_FILE -a -f $SUPERUSER_PASSWORD_FILE ]; then
export DJANGO_SUPERUSER_NAME=$(cat $SUPERUSER_NAME_FILE)
export DJANGO_SUPERUSER_PASSWORD=$(cat $SUPERUSER_PASSWORD_FILE)
python manage.py createsuperuser --noinput || echo 'Error occured while creating superuser'
fi

python manage.py runserver 0.0.0.0:$BACKEND_PORT $@
