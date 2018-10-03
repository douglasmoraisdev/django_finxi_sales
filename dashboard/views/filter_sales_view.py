import json
import random

from django.views.generic import View
from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse

from dashboard.models import ProductModel, SalesModel
from dashboard.forms import FileImportForm


class FilterSalesView(View):

    def post(self, request, *args, **kwargs):
        # form_class = self.get_form_class()
        # form = self.get_form(form_class)

        company = request.POST['company']

        use_category = 'use_category' in request.POST
        use_product = 'use_product' in request.POST

        if 'product_name' in request.POST:
            product_name = request.POST['product_name']
        else:
            product_name = ''

        if 'category' in request.POST:
            category = request.POST.getlist('category')
        else:
            category = ''

        """
        print("company [%s]" % company)
        print("product_name [%s]" % product_name)
        print("use_product [%s]" % use_product)
        print("category [%s]" % category)
        print("use_category [%s]" % use_category)
        """
        sales_filter = SalesModel.manager.get_sales_by_filters(company=company,
                                                      filter_product=use_product,
                                                      product_name=product_name,
                                                      filter_category=use_category,
                                                      category=category)
        print(sales_filter)

        result = []
        for items in sales_filter:
            result.append(dict(
                product=items.product.name,
                total_sold=items.unit_sales,
                sale_price_avg=items.sale_total,
                cost_price_avg=items.product.cost_price
            ))

        """Mock data"""
        '''
        total_sold = random.randrange(1, 10)
        sale_price_avg = random.randrange(13, 120)
        cost_price_avg = random.randrange(43, 520)
        data = [dict(product="abacate9", total_sold=total_sold+3, 
                     sale_price_avg=sale_price_avg+3, cost_price_avg=cost_price_avg+8),
                dict(product="abacate3", total_sold=total_sold+4, 
                     sale_price_avg=sale_price_avg+4, cost_price_avg=cost_price_avg+9),
                dict(product="abacate2", total_sold=total_sold+5, 
                     sale_price_avg=sale_price_avg+5, cost_price_avg=cost_price_avg+2),
                dict(product="abacate3", total_sold=total_sold+2, 
                     sale_price_avg=sale_price_avg+2, cost_price_avg=cost_price_avg+4),
                ]
        '''

        return render(request, 'data_table.html', context={'data': result})
