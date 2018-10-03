import tempfile
from zipfile import BadZipfile
from openpyxl import load_workbook

from django import forms
from dashboard.tasks import ProcessFile
from django.core.serializers import serialize, deserialize


class FileImportForm(forms.Form):
    company_name = forms.CharField(max_length=50)
    sales_file = forms.FileField()

    def process_file(self, file_name, company_name):
        # create a temp_file name
        temp_file = tempfile.NamedTemporaryFile(dir='/code', suffix='.xlsx')
        temp_file_name = temp_file.name

        # write file_name contents to temp file
        temp_file.close()
        with open(temp_file_name, 'wb+') as destination:
            for chunk in file_name.chunks():
                destination.write(chunk)

        # validate xlsx file
        try:
            wb = load_workbook(filename=destination.name)
        except BadZipfile:
            return False

        proc_file_task = ProcessFile()
        proc_file_task.delay(temp_file_name, company_name)

        return True
