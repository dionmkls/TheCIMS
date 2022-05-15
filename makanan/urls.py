from django.urls import path
from . import views

app_name = 'makanan'
urlpatterns = [
    path('list_makanan', views.list_makanan, name='list_makanan'),
]
