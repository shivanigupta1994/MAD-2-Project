
from utils.celery_worker import celery_init_app
from celery.schedules import crontab
from app import app

celery_app = celery_init_app(app)


# @celery_app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
    
#     # Run monthly activity report every minute
#     sender.add_periodic_task(crontab(minute='*', hour='*'), tasks.monthly_activity_report.s())
#     # Run daily reminders every minute
#     sender.add_periodic_task(crontab(minute='*', hour='*'), tasks.daily_reminders.s())
#     # Run store manager report every minute
#     sender.add_periodic_task(crontab(minute='*', hour='*'), tasks.store_manager_report.s())


