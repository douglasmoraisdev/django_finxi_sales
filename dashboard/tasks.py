from __future__ import absolute_import

from functools import reduce
from random import randint
from time import sleep

from celery.decorators import task
from celery import current_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


def simulate_proc(self, percent):
    """Simulate a heavy proccess"""

    # update task progress state
    current_task.update_state(state='PROGRESS',
                              meta={'current': percent,
                                    'total': 100
                                    })

    # logger.info("status: %s" % percent)

    # a fake delay
    if (percent < 100):
        sleep(5)


@task(name="some_proccess")
def some_proccess(x):
    """a mock proccess to simulate heavy load"""
    logger.info("Some heavy proccess")

    # create a fake process
    percent_list = [10, 20, 30, 60, 80, 100]
    reduce(simulate_proc, percent_list)

    # return x # comment for return default 'SUCCESS'
