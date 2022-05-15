from django.urls import path

from . import views

app_name = 'menggunakan_apparel'

urlpatterns = [
    path('',views.index, name='index'),
]