import json

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from celery.result import AsyncResult
from celery.task.control import inspect

from dashboard.forms import FileImportForm

def proc_state(request):
    """ A view to report the progress to the user """
    if 'job' in request.GET:
        job_id = request.GET['job']
    else:
        return HttpResponse('No job id given.')

    job = AsyncResult(job_id)
    data = job.result or job.state

    result = dict(id=job_id, status=data)

    return HttpResponse(json.dumps(result))
