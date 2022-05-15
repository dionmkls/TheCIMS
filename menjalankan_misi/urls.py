from django.urls import path
from . import views

app_name = 'menjalankan_misi_utama'
urlpatterns = [
    path('list_menjalankan_misi_utama', views.list_menjalankan_misi_utama, name='list_menjalankan_misi_utama'),
]
