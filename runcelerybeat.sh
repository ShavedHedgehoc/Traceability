#!/usr/bin/env bash

export FLASK_APP=traceability
export FLASK_ENV=development
# celery beat --loglevel=INFO
celery -A celery_worker.celery beat --loglevel=INFO


