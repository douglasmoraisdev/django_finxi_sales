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

        simulate_proc(30, uploaded_file)        
        simulate_proc(60, uploaded_file)
        simulate_proc(90, uploaded_file)
        simulate_proc(100, uploaded_file)

        self.update_db(uploaded_file, company_name)

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

            # verify cost_price is a number
            cost_price = cells[3].value.replace('R$ ', '')\
                                       .replace(',','.')
            try:
                if cost_price:
                    cost_price = float(cost_price)
                else:
                    cost_price = 0
            except ValueError:
                cost_price = 0

            # verify total_sold is a number
            total_sold = cells[4].value.replace('R$ ', '')\
                                       .replace(',','.')
            try:
                if total_sold:
                    total_sold = float(total_sold)
                else:
                    total_sold = 0
            except ValueError:
                total_sold = 0

            # verify units_sold is a number
            units_sold = cells[2].value
            try:
                if units_sold:
                    units_sold = int(units_sold)
                else:
                    units_sold = 0
            except ValueError:
                units_sold = 0

            # create a serialized dict
            rows.append(dict(product=cells[0].value,
                             category=cells[1].value,
                             units_sold=units_sold,
                             cost_price=cost_price,
                             total_sold=total_sold,
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
            if CategoryModel.objects.filter(name=cat, company=company)\
                                     .exists():
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
                    units_sold = items['units_sold']
                    total_sold = items['total_sold']

                    # update product if not exists
                    if not ProductModel.objects.filter(name=product_name,
                                                       category__name=cat)\
                                               .exists():

                        # print('Adding Product %s' % product_name)
                        product = ProductModel()
                        product.name = str(product_name)
                        product.cost_price = cost_price
                        product.category = category
                        product.save()
                        product_id = product.id
                    else:
                        product = ProductModel.objects.get(name=product_name,
                                                           category__name=cat)
                        product_id = product.id

                    # update sales

                    # update sales if not exists
                    # if not SalesModel.objects.filter(product=product).exists():
                    # print('Added Sale %s' % product)
                    sales = SalesModel()
                    sales.product = product
                    sales.unit_sales = units_sold
                    sales.sale_total = total_sold
                    sales.save()
                    sales_id = sales.id

        print('Total added company %d' % CompanyModel.objects.all().count())
        print('Total added categories %d' % CategoryModel.objects.all().count())
        print('Total added product %d' % ProductModel.objects.all().count())
        print('Total added sales %d' % SalesModel.objects.all().count())
        print('---')

        return True


celery_app.tasks.register(ProcessFile())
