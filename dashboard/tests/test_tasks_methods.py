from django.test import TestCase
from celery import group

from dashboard.tasks import ProcessFile

class TestTasks(TestCase):
    """Test tesks"""


    def test_update_database(self):
        
        task = ProcessFile()

        res = task.update_db('tmp6dy68oia.xlsx', 'Empresas Finxi')

        self.assertTrue(res)
