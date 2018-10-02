from django.urls import path
from django.conf.urls import url

from dashboard.views import FilterSalesView, FileImportView, DashboardView

urlpatterns = [
    path('', DashboardView.as_view()),
    path('import/', FileImportView.as_view()),
    path('filter/', FilterSalesView.as_view()),
    # url(r'^proc_state$', views.proc_state, name="proc_state")

]