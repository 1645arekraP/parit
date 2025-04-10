import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'parit.settings')

app = Celery('parit', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# Set engine to use postgres
app.conf.beat_scheduler = 'django_celery_beat.schedulers:DatabaseScheduler'


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

app.conf.beat_schedule = {
    #'update-group-solutions-tasks': {
    #    'task': 'questions.tasks.update_group_solutions_tasks',
    #     'schedule': 60.0,  # Every minute for testing
    #},
    'update-group-questions-tasks': {
        'task': 'questions.tasks.update_group_quesions_tasks',
        'schedule': 60.0,  # Every minute for testing
    },
}