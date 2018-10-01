from __future__ import absolute_import

from functools import reduce
from random import randint
from time import sleep

from celery.decorators import task
from celery import current_task
from celery.utils.log import get_task_logger

from dashboard.models import CategoryModel

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
        sleep(1)


@task(name="process_file")
def process_file(uploaded_file):
    logger.info("Start process file %s" % uploaded_file)

    # create a fake process
    percent_list = [10, 30, 80, 100]
    reduce(simulate_proc, percent_list)

    '''
    #it works - ok
    category = CategoryModel()

    category.name = 'new category'
    category.save()
    '''

    return CategoryModel.objects.all().count()