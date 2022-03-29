from broker.celery import app
from celery.utils.log import get_task_logger

celery_log = get_task_logger(__name__)


@app.task(name='api.add_book')
def add_book(book):
    get_task_logger('+1')
    return None
