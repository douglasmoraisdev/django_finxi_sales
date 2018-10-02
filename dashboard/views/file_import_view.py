from django.views.generic.edit import FormView

from dashboard.forms import FileImportForm


class FileImportView(FormView):
    template_name = "main.html"
    form_class = FileImportForm
    success_url = '/dashboard/#tab_filter'

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        file = request.FILES['sales_file']
        if form.is_valid():

            form.process_file(file)

            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):

        return super().form_valid(form)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        return response
