from __future__ import absolute_import

from functools import reduce
from random import randint
from time import sleep

from celery.decorators import task
from celery import current_task, Task
from celery.utils.log import get_task_logger

from dashboard.models import CategoryModel
from finxi.celery import app as celery_app

logger = get_task_logger(__name__)


class ProcessFile(Task):
    name = "ProcessFile"

    # @task(name="ProcessFile")
    def run(self, uploaded_file):

        def simulate_proc(self, percent):
            """Simulate a heavy proccess"""
            # update task progress state
            current_task.update_state(state='PROGRESS',
                                    meta={'current': percent,
                                            'total': 100
                                            })
            logger.info("percent %s" % percent)
            # a fake delay
            if (percent < 100):
                sleep(1)

        logger.info("Start process file %s" % uploaded_file)

        # create a fake process
        list_percents = (10, 20, 50, 80, 90, 100)
        reduce(simulate_proc, list_percents)

        '''
        #it works - ok
        category = CategoryModel()

        category.name = 'new category'
        category.save()
        '''

        return CategoryModel.objects.all().count()

celery_app.tasks.register(ProcessFile())
