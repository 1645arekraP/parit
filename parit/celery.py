import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'parit.settings')

app = Celery('parit', 
             broker=f"redis://{os.getenv('REDIS_USERNAME')}:{os.getenv('REDIS_PASSWORD')}@{os.getenv("REDIS_HOST")}:{os.getenv('REDIS_PORT')}/{os.getenv('REDIS_BROKER_DB')}", 
             backend=f"redis://{os.getenv('REDIS_USERNAME')}:{os.getenv('REDIS_PASSWORD')}@{os.getenv("REDIS_HOST")}:{os.getenv('REDIS_PORT')}/{os.getenv('REDIS_BACKEND_DB')}")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# Set engine to use postgres
app.conf.beat_scheduler = 'django_celery_beat.schedulers:DatabaseScheduler'
