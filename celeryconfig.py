# from celery.schedules import crontab
from datetime import timedelta

imports = ('app.tasks')
accept_content = ['json']
result_serializer = 'json'
task_serializer = 'json'

beat_schedule = {
    'documents_upload': {
        'task': 'dispatch',
        'schedule':  2,
    },
    # 'upload': {
    #     'task': 'base',
    #     'schedule':  30,
    # },
}
