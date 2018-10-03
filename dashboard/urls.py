from django.urls import path
from django.conf.urls import url

from dashboard.views import FilterSalesView, FileImportView,\
                            DashboardView, ProcStateView,\
                            CompanyListView

urlpatterns = [
    path('', DashboardView.as_view()),
    path('import/', FileImportView.as_view()),
    path('filter/', FilterSalesView.as_view()),
    path('company_list/', CompanyListView.as_view()),
    url(r'^proc_state$', ProcStateView.as_view(), name="proc_state")

]