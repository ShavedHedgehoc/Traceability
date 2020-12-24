# from celery.schedules import crontab
from datetime import timedelta

imports = ('app.tasks')
accept_content = ['json']
result_serializer = 'json'
task_serializer = 'json'

beat_schedule = {
    'documents_upload': {
        'task': 'base_update',
        'schedule':  20,
    }
}
