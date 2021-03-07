import os
from celery import Celery


def make_celery_app(flask_app):
    celery = Celery(
        flask_app.import_name,
        broker=os.getenv("CELERY_BROKER_URI"),
    )

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with flask_app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
