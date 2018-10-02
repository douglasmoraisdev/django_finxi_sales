from django.db import models

from .company_model import CompanyModel

class CategoryModel(models.Model):
    name = models.CharField(max_length=30)
    company = models.ForeignKey(CompanyModel, on_delete=models.CASCADE,
                                                blank=False, null=False)

    def __str__(self):
        return self.name
