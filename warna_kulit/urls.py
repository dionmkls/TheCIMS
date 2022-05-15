from django.urls import path

from . import views

app_name = 'warna_kulit'

urlpatterns = [
    path('',views.index, name='index'),
]