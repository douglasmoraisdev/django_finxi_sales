# some_app/views.py
from django.views.generic import TemplateView


class DashboardView(TemplateView):
    template_name = "main.html"
