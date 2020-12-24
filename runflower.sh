#!/usr/bin/env bash

export FLASK_APP=traceability
export FLASK_ENV=development

celery -A celery_worker.celery flower




