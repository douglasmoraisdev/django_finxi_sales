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

        def simulate_proc(percent, filename):
            """Simulate a heavy proccess"""
            # update task progress state
            current_task.update_state(state='PROGRESS',
                                      meta={'current': percent,
                                            'total': 100,
                                            'filename': filename
                                            })
            logger.info("[%s]percent %s" % (filename, percent))
            # a fake delay
            if (percent < 100):
                sleep(1)

        logger.info("Start process file %s" % uploaded_file)

        # create a fake heavy process
        simulate_proc(10, uploaded_file)
        simulate_proc(30, uploaded_file)
        simulate_proc(60, uploaded_file)
        simulate_proc(90, uploaded_file)
        simulate_proc(100, uploaded_file)

        '''
        #it works - ok
        category = CategoryModel()

        category.name = 'new category'
        category.save()
        '''

        return CategoryModel.objects.all().count()

celery_app.tasks.register(ProcessFile())
