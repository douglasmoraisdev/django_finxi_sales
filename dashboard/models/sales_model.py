from django.db import models

from .product_model import ProductModel
from .category_model import CategoryModel


class SalesModel(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE,
                                              blank=False, null=False)
    unit_sales = models.IntegerField(null=False, blank=False)
    sale_total = models.FloatField(null=False, blank=False)
