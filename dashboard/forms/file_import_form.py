from django import forms
from dashboard.tasks import ProcessFile

from openpyxl import load_workbook


class FileImportForm(forms.Form):
    company_name = forms.CharField(max_length=50)
    sales_file = forms.FileField()

    def process_file(self, file_name):
        # a simple anti spam filter

        wb = load_workbook(filename=file_name)
        sheet_ranges = wb['Sheet1']

        rows = []
        for cells in sheet_ranges:
            rows.append(dict(product=cells[0].value,
                             category=cells[1].value,
                             units_sold=cells[2].value,
                             cost_price=cells[3].value,
                             total_sale=cells[4].value,
                             )
                        )

        # print(rows)
        '''
        file_content = []
        for chunk in file_name.chunks():
            file_content.append(chunk)

        print(file_content)
        '''
        proc_file_task = ProcessFile()
        proc_file_task.delay('desafio.xlsx')

        return True
        # return process_file.delay(file_name)
