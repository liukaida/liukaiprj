#!/usr/bin/env bash
#. /opt/virt/vote/bin/activate
cd ..
gunicorn --config gunicorn.conf liukaiprj.wsgi:application --daemon

