import json
import random

from django.views.generic import View
from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse

from dashboard.models import ProductModel, SalesModel
from dashboard.forms import FileImportForm


class FilterSalesView(View):

    def get(self, request, *args, **kwargs):

        company = request.GET['company']

        # Retrieve Filters
        if 'use_product' in request.GET:
            use_product = (request.GET['use_product'] == 'on')

        if 'use_category' in request.GET:
            use_category = (request.GET['use_category'] == 'on')            

        if 'product_name' in request.GET:
            product_name = request.GET['product_name']
            if product_name == '':
                use_product = False
        else:
            use_product = False

        if 'category' in request.GET:            
            category = request.GET['category'].split(',')
            if category == ['']:
                use_category = False
        else:
            use_category = False

        sales_filter = SalesModel.manager.get_sales_by_filters(company=company,
                                                      filter_product=use_product,
                                                      product_name=product_name,
                                                      filter_category=use_category,
                                                      category=category)

        result = []
        for items in sales_filter:

            # Format monetary values
            avg_sales = 'R$ %.2f' % items['avg_sales']
            avg_cost = 'R$ %.2f' % items['avg_cost']

            result.append(dict(
                product=items['product__name'],
                total_sold=items['total_sold'],
                sale_price_avg=avg_sales,
                cost_price_avg=avg_cost,
            ))

        return render(request, 'data_table.html', context={'data': result})
