from django.urls import path
from . import views

app_name = 'makan'
urlpatterns = [
    path('list_makan', views.list_makan, name='list_makan'),
]
