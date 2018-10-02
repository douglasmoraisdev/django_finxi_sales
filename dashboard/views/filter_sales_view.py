from django.views.generic import TemplateView
from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse


from dashboard.models import ProductModel

from dashboard.forms import FileImportForm

class FilterSalesView(TemplateView):
    template_name = "main.html"

    def post(self, request, *args, **kwargs):
        # form_class = self.get_form_class()
        # form = self.get_form(form_class)

        company = request.POST['company']
       
        if 'product_name' in request.POST:
            product_name = request.POST['product_name']
        use_product = 'use_product' in request.POST
        use_category = 'use_category' in request.POST

        category = request.POST.getlist('category')

        """
        print("company [%s]" % company)
        print("product_name [%s]" % product_name)
        print("use_product [%s]" % use_product)
        print("category [%s]" % category)
        print("use_category [%s]" % use_category)
        """

        # Loads the query according switch_filters - INITIAL
        if (use_product):
            res = ProductModel.objects.filter(category__company=company)
        else:
            res = ProductModel.objects.filter(category__company=company, category__in=category)            

        print('total products for [%s]-%s: %d' % (company, category, res.count()))

        data = dict(product='abacate', price='4.00')

        return JsonResponse(data)

        # return render(request, 'data_table.html', {'data': data})
        # return HttpResponse("ok")

        '''
        return self.form_valid(form)
        return self.form_invalid(form)
        '''
