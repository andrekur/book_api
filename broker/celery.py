from celery import Celery
from dotenv import dotenv_values

CONFIG = dotenv_values('_CI/.env')


PROTOCOL = CONFIG['BROKER_PROTOCOL']
USER = CONFIG['BROKER_USER']
PASSWD = CONFIG['BROKER_PASSWORD']
HOST = CONFIG['BROKER_HOST']
PORT = CONFIG['BROKER_LOCAL_PORT']

broker_url = f'{PROTOCOL}://{USER}:{PASSWD}@{HOST}:{PORT}/'

app = Celery(
    'tasks',
    broker_url=broker_url,
    include=['api.tasks'],
)

app.autodiscover_tasks()
