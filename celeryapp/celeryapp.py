from celery import Celery

import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv(".env"))
TOKEN = os.getenv("OFFERS_TOKEN")
BASE_URL = os.getenv("OFFERS_BASE_URL")


def make_celery_app(flask_app):
    celery = Celery(
        flask_app.import_name,
        broker="sqla+sqlite:///celery_broker.db",
        # backend=flask_app.config["CELERY_RESULT_BACKEND"],
        # broker=flask_app.config["CELERY_BROKER_BACKEND"],
    )
    # celery.conf.update(flask_app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with flask_app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
