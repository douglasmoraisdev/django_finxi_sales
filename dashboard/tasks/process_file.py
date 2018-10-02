from __future__ import absolute_import

from functools import reduce
from random import randint
from time import sleep

from celery.decorators import task
from celery import current_task, Task
from celery.utils.log import get_task_logger

from dashboard.models import CategoryModel
from openpyxl import load_workbook


from finxi.celery import app as celery_app

logger = get_task_logger(__name__)


class ProcessFile(Task):
    name = "ProcessFile"

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

        # Reads a xslx file
        wb = load_workbook(filename=uploaded_file)
        simulate_proc(10, uploaded_file)

        # get the Sheet1 data
        sheet_ranges = wb['Sheet1']

        # serialize cells data to Dict
        rows = []
        for cells in sheet_ranges:
            rows.append(dict(product=cells[0].value,
                             category=cells[1].value,
                             units_sold=cells[2].value,
                             cost_price=cells[3].value,
                             total_sale=cells[4].value,
                             )
                        )
        simulate_proc(30, uploaded_file)

        # insert category in database
        for i, d in enumerate(rows):
            logger.info("adding category to db %d" % (i))
            category = CategoryModel()
            category.name = d['category']
            category.save()

        simulate_proc(60, uploaded_file)
        simulate_proc(90, uploaded_file)
        simulate_proc(100, uploaded_file)

        '''
        #it works - ok
        category = CategoryModel()

        category.name = 'new category'
        category.save()
        '''

        return 'SUCCESS'

celery_app.tasks.register(ProcessFile())
