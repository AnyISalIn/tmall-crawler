from tmall_crawler.core import Tmall
from celery import Celery

import logging

app = Celery('tasks', broker='redis://localhost:6379/0')


@app.task
def add(x, y):
    return x + y


@app.task
def run(site, path=None):
    t = Tmall(site, path=path)
    try:
        t.get()
    except Exception as e:
        logging.warning(e)
        t.close()
