from django.utils import timezone
from django.views.generic.list import ListView

from dashboard.models import CategoryModel

class CategoryListView(ListView):

    model = CategoryModel
    template_name = "category_list.html"

    def get_queryset(self):
        queryset = super(CategoryListView, self).get_queryset()

        company = self.request.GET.get('company')

        queryset = queryset.filter(company=company)
        return queryset