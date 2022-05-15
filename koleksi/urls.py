from django.urls import path

from . import views

app_name = 'koleksi'
urlpatterns = [
    path('', views.index, name='index'),
    path('menu_koleksi/',views.menu_koleksi, name='menu_koleksi'),
    path('list_rambut/',views.list_rambut, name='list_rambut'),
    path('list_mata/', views.list_mata, name='list_mata'),
    path('list_rumah/', views.list_rumah, name='list_rumah'),
    path('list_barang/', views.list_barang, name='list_barang'),
    path('list_apparel/', views.list_apparel, name='list_apparel'),
]
