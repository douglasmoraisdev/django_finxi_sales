from django.views.generic.edit import FormView
from django.http import JsonResponse
from celery.task.control import inspect

from dashboard.forms import FileImportForm


class FileImportView(FormView):
    template_name = "main.html"
    form_class = FileImportForm
    success_url = '/dashboard/#tab_filter'

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        company_name = request.POST['company_name']
        file = request.FILES['sales_file']

        if form.is_valid():

            form.process_file(file, company_name)

            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):

        task_inspect = inspect()

        for keys in task_inspect.active().keys():
            active_tasks = task_inspect.active()[keys]
            next_tasks = task_inspect.reserved()[keys]

        proc_list = []

        # get 'id' and 'args'(filename) attribute from tasks lists
        proc_list = list(map(lambda x: x['id'], active_tasks + next_tasks))

        result = dict(proc_data=proc_list)

        return JsonResponse(result)


    def form_invalid(self, form):
        response = super().form_invalid(form)
        return response
