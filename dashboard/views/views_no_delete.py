import json

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from celery.result import AsyncResult
from celery.task.control import inspect


from .forms import CalculatorForm


def index(request):
    """A view to receive a POST example"""

    if request.method == 'POST':

        form = CalculatorForm(request.POST)

        if form.is_valid():

            x = int(form['x_value'].value())

            form.calc(x)

            task_inspect = inspect()
            
            for keys in task_inspect.active().keys():
                active_tasks = task_inspect.active()[keys]
                next_tasks = task_inspect.reserved()[keys]

            pid_list = []

            # get 'id' attribute from tasks lists
            pid_list = map(lambda x: x['id'], active_tasks + next_tasks)

            return render(request, 'index.html', {'proc_list': pid_list,
                                                  'form': form})
    else:
        form = CalculatorForm()

    return render(request, 'index.html', {'form': form})


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
