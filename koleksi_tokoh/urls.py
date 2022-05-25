from django.urls import path

from . import views
app_name = 'koleksi_tokoh'
urlpatterns = [
  path('', views.index, name='index'),
  path('create/', views.createKoleTokoh, name='create_kt'),
  path('delete/<str:namatokoh>/<str:id>', views.delKoleTokoh, name='delete_kt'),
]
