from django.urls import path

from . import views

app_name = 'pekerjaan'
urlpatterns = [
    path('list_pekerjaan', views.list_pekerjaan, name='list_pekerjaan'),
]
