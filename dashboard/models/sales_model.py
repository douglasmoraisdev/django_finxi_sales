from django.db import models

from .product_model import ProductModel
from .category_model import CategoryModel


class SalesManager(models.Manager):

    def get_sales_by_filters(self, company, filter_product, filter_category,
                             product_name, category):
        """Filter sales average by:
        company(always),
        product and/or category(optional)
        """
        # filter by product + category
        if (filter_product and filter_category):
            return self._get_sales_by_product_category(company, product_name,
                                                       category)

        # filter only by product
        if (filter_product):
            return self._get_sales_by_product(company, product_name)

        # filter only by category
        if (filter_category):
            return self._get_sales_by_category(company, category)

        # filter only by company
        if not (filter_product and filter_category):
            return self._get_sales_by_company(company)

    def _get_sales_by_company(self, company):

        return self._apply_sales_aggregations(self._default_company_filter(company))

    def _get_sales_by_product(self, company, product_name):

        return self._apply_sales_aggregations(self._default_company_filter(company)\
                                              .filter(product__name__contains=product_name))

    def _get_sales_by_category(self, company, category_name):

        return self._apply_sales_aggregations(self._default_company_filter(company)\
                                              .filter(product__category__in=category_name))

    def _get_sales_by_product_category(self, company, product_name, category_name):

        return self._apply_sales_aggregations(self._default_company_filter(company)\
                                              .filter(product__name__contains=product_name)\
                                              .filter(product__category__in=category_name))

    def _default_company_filter(self, company):

        return super().get_queryset().filter(product__category__company=company)

    def _apply_sales_aggregations(self, query_set):
        
        return query_set.values('product__name')\
                        .annotate(total_sold=models.Sum('unit_sales'))\
                        .annotate(avg_sales=models.Avg('sale_total'))\
                        .annotate(avg_cost=models.Avg('product__cost_price'))


class SalesModel(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE,
                                              blank=False, null=False)
    unit_sales = models.IntegerField(null=False, blank=False)
    sale_total = models.FloatField(null=False, blank=False)

    manager = SalesManager()

    def __str__(self):
        return str(self.id) + ' - ' + self.product.name + ': ' + str(self.sale_total)
