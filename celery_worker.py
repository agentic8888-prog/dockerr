from celery import Celery

celery_app = Celery(
    "agent",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

celery_app.conf.enable_utc = True
celery_app.conf.timezone = "Asia/Kolkata"

import tasks  # ✅ this line registers the task with the worker