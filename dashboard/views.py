import json

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from celery.task.control import inspect


def index(request):
    """A view to receive a POST example"""

    return HttpResponse('Hello World 2')
