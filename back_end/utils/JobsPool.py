from celery import Celery
from flask import current_app as app
import globalConstants

celery = Celery(globalConstants.GROCERY_STORE,broker=globalConstants.REDIS_BROKER_URI, backend=globalConstants.REDIS_BACKEND_URI)

class taskHandler(celery.Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)

