from celery import Celery
# TODO ADD ENV FILE

PROTOCOL = 'amqp'
USER = 'test_user'
PASSWD = 'test_password'
HOST = 'localhost'
PORT = '5672'

broker_url = f'{PROTOCOL}://{USER}:{PASSWD}@{HOST}:{PORT}/'

app = Celery('tasks', broker_url=broker_url, include=['api.tasks'])

app.autodiscover_tasks()
