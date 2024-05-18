from celery import Celery, Task


def celery_init_app(app):
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.conf.broker_url = "redis://localhost:6379/1"
    celery_app.conf.result_backend = "redis://localhost:6379/2"
    celery_app.conf.timezone = "Asia/Kolkata"  
    celery_app.conf.broker_connection_retry_on_startup=True  
    
    
    return celery_app
