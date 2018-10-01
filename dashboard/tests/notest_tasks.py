from django.test import TestCase
from celery.result import AsyncResult
from celery import group

from dashboard.tasks import process_file
from dashboard.models import CategoryModel


class TestTasks(TestCase):
    """Test tesks"""


    def test_task_process_file_status(self):
        """Test the file import method status
        
        Must return state='SUCCESS'
        """

        job = group([
            process_file.s(2),
        ])

        result = job.apply_async()

        result.join()

        self.assertEqual(result[0].state, 'SUCCESS')

    def test_task_process_insert_db(self):
        """Test a insertion in the database
        
        Must assert a new record count
        """

        job = group([
            process_file.s(2),
        ])

        result = job.apply_async()

        result.join()

        total_records = CategoryModel.objects.all().count()

        self.assertEqual(total_records, 1)
