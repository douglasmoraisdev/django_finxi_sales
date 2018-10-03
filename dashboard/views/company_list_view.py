from django.utils import timezone
from django.views.generic.list import ListView

from dashboard.models import CompanyModel

class CompanyListView(ListView):

    model = CompanyModel
    template_name = "company_list.html"
