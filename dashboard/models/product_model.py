from django.db import models

from .category_model import CategoryModel


class ProductModel(models.Model):
    name = models.CharField(max_length=100)
    cost_price = models.FloatField()
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE,
                                                blank=False, null=False)