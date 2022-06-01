from celery import Celery
from dotenv import dotenv_values

CONFIG = dotenv_values('_CI/.env')


PROTOCOL = CONFIG['CELERY_PROTOCOL']
USER = CONFIG['CELERY_USER']
PASSWD = CONFIG['CELERY_PASSWD']
HOST = CONFIG['CELERY_HOST']
PORT = CONFIG['CELERY_PORT']

broker_url = f'{PROTOCOL}://{USER}:{PASSWD}@{HOST}:{PORT}/'

app = Celery(
    'tasks',
    broker_url=broker_url,
    include=['api.tasks'],
)

app.autodiscover_tasks()
