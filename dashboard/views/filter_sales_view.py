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

        sales_filter = SalesModel.manager.get_sales_by_filters(company=company,
                                                      filter_product=use_product,
                                                      product_name=product_name,
                                                      filter_category=use_category,
                                                      category=category)
        print(sales_filter)

        result = []
        for items in sales_filter:
            result.append(dict(
                product=items['product__name'],
                total_sold=items['total_sold'],
                sale_price_avg=items['avg_sales'],
                cost_price_avg=items['avg_cost']
            ))

        return render(request, 'data_table.html', context={'data': result})
