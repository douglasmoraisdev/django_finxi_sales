from django.test import TestCase
from dashboard.forms import FileImportForm
from celery.result import AsyncResult


class TestForms(TestCase):
    """Test forms methods"""


    def test_process_file_import(self):
        """Test the file import method
        
        Must return a task object
        """

        new_file_proc = FileImportForm()
        res = new_file_proc.process_file('x')

        self.assertTrue(isinstance(res, AsyncResult))
