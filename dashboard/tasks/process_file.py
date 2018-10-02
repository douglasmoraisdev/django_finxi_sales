from __future__ import absolute_import

from functools import reduce
from random import randint
from time import sleep

from celery.decorators import task
from celery import current_task, Task
from celery.utils.log import get_task_logger

from dashboard.models import CompanyModel, CategoryModel,\
                             ProductModel, SalesModel
from openpyxl import load_workbook


from finxi.celery import app as celery_app

logger = get_task_logger(__name__)


class ProcessFile(Task):
    name = "ProcessFile"

    def run(self, uploaded_file, company_name):

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
                             total_sold=cells[4].value,
                             )
                        )     
        
        simulate_proc(30, uploaded_file)        

        # insert category in database
        '''
        for i, d in enumerate(rows):
            logger.info("adding category to db %d" % (i))
            category = CategoryModel()
            category.name = d['category']
            category.save()
        '''

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

    def update_db(self, uploaded_file, company_name):

        # Reads a xslx file
        wb = load_workbook(filename=uploaded_file)
        # simulate_proc(10, uploaded_file)

        # get the Sheet1 data
        sheet_ranges = wb['Sheet1']

        # serialize cells data to Dict
        rows = []
        for cells in sheet_ranges:

            cost_price = cells[3].value.replace('R$ ', '')\
                                       .replace(',','.')
            # verify cost_price is a number
            try:
                if cost_price:
                    cost_price = float(cost_price)
                else:
                    cost_price = 0
            except ValueError:
                cost_price = 0

            # create a serialized dict
            rows.append(dict(product=cells[0].value,
                                category=cells[1].value,
                                units_sold=cells[2].value,
                                cost_price=cost_price,
                                total_sold=cells[4].value,
                                )
                        )     
        
        # simulate_proc(30, uploaded_file)

        # start process to DB

        # get company id or create one
        if CompanyModel.objects.filter(name=company_name).exists():
            company = CompanyModel.objects.get(name=company_name)
        else:
            company = CompanyModel()
            company.name = company_name
            company.save()
            company = company


        
        # filter unique category        
        all_categories = []
        for items in rows:
            all_categories.append(items['category'])
        filtered_category = set(all_categories)

        # update categories
        for cat in filtered_category:
            if CategoryModel.objects.filter(name=cat, company=company).exists():
                category_id = CategoryModel.objects.get(name=cat).id
            else:
                category = CategoryModel()
                category.name = str(cat)
                category.company = company
                category.save()
                category_id = category.id

            # update products
            for items in rows:
                # group by category
                if items['category'] == cat:

                    product_name = items['product']
                    cost_price = items['cost_price']

                    # update if not exists
                    if not ProductModel.objects.filter(name=product_name, category__name=cat).exists():
                        print('Adding Product %s' % product_name)
                        
                        product = ProductModel()
                        product.name = str(product_name)
                        product.cost_price = cost_price
                        product.category = category
                        product.save()
                        product_id = product.id

        print('Total added company %d' % CompanyModel.objects.all().count())
        print('Total added categories %d' % CategoryModel.objects.all().count())
        print('Total added product %d' % ProductModel.objects.all().count())
        print('---')

        return True


celery_app.tasks.register(ProcessFile())
