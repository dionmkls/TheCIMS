from django.urls import path
from . import views

app_name = 'misi_utama'
urlpatterns = [
    path('list_misi_utama', views.list_misi_utama, name='list_misi_utama'),
]