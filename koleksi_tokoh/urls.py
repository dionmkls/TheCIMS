from django.urls import path

from . import views
app_name = 'koleksi_tokoh'
urlpatterns = [
  path('', views.index, name='index'),
]
