from broker.celery import app
from celery.utils.log import get_task_logger

from db.crud import create_book_parser
from db.connector import Session

celery_log = get_task_logger(__name__)


def error_decorator(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as ex:
            celery_log.error(ex)
    return wrapper


@app.task(name='api.create_book')
@error_decorator
def create_or_upd_book(book):
    with Session() as db:
        create_book_parser(db, book)
