from django.contrib import admin

from dashboard.models import ProductModel, CategoryModel,\
                             SalesModel, CompanyModel

# Register your models here.
admin.site.register(ProductModel)
admin.site.register(CategoryModel)
admin.site.register(SalesModel)
admin.site.register(CompanyModel)
