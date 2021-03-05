from celery import Celery


def make_celery_app(flask_app):
    celery = Celery(
        flask_app.import_name,
        broker="sqla+sqlite:///celery_broker.db",
    )

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with flask_app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
