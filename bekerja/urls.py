from django.urls import path

from . import views

app_name = 'bekerja'
urlpatterns = [
    path('list_bekerja', views.list_bekerja, name='list_bekerja'),
]
