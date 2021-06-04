# from celery.schedules import crontab
from datetime import timedelta

imports = ('app.tasks')
accept_content = ['json']
result_serializer = 'json'
task_serializer = 'json'

beat_schedule = {
    # 'doc_reload':{
    #     'task': 'doc_reload',
    #     'schedule':  5,
    # },
    'doc_write': {
        'task': 'doc_write',
        'schedule': 5,
    }



    # 'documents_upload': {
    #     'task': 'dispatch',
    #     'schedule':  2,
    # },
    # 'test': {
    #     'task': 'test',
    #     'schedule':  1,
    # },
}
