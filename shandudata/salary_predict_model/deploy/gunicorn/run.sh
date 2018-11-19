#!/bin/bash

NAME="SXZ"                                            # Name of the application
DJANGODIR=/home/deploy/salary_predict_model/web
SXZ_DIR=/home/deploy/salary_predict_model
SOCKFILE=/mnt/sxz/tmp/gunicorn.sock     # we will communicte using this unix socket
USER=deploy                                                   # the user to run as
GROUP=deploy                                                  # the group to run as
NUM_WORKERS=5                                               # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=web.settings                   # which settings file should Django use, change to
# myproject.settings.prod if necessary
DJANGO_WSGI_MODULE=web.wsgi                           # WSGI module name
LOG_FILE='/mnt/sxz/log/gunicorn/access.log'
ERROR_LOG_FILE='/mnt/sxz/log/gunicorn/err.log'
RUN_LOG_FILE='/mnt/sxz/log/gunicorn/run.log'

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$SXZ_DIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec gunicorn ${DJANGO_WSGI_MODULE}:application \
    --name $NAME \
    --workers $NUM_WORKERS \
    --user=$USER --group=$GROUP \
    --log-level=info \
    --bind=unix:$SOCKFILE \
    --access-logfile=$LOG_FILE \
    --error-logfile=$ERROR_LOG_FILE \
    --log-file=$RUN_LOG_FILE
