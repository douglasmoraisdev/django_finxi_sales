from django.urls import path
from django.conf.urls import url


from . import views

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^proc_state$', views.proc_state, name="proc_state"),
]