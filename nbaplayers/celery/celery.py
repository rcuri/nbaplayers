from celery import Celery
from nbaplayers.config import DevelopmentConfig


app = Celery('nbaplayers',
             broker=DevelopmentConfig.CELERY['BROKER_URL'],
             backend=DevelopmentConfig.CELERY['RESULT_BACKEND'],
             include=DevelopmentConfig.CELERY['TASK_IMPORTS']
             )


def start_celery_app():
    app.start()

if __name__ == '__main__':
    app.start()