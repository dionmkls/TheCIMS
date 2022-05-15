from django.urls import path

from . import views

app_name = 'level'

urlpatterns = [
    path('',views.index, name='index'),
]