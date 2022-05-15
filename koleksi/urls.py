from django.urls import path

from . import views

app_name = 'koleksi'
urlpatterns = [
    path('', views.index, name='index'),
    path('menu_koleksi/',views.menu_koleksi, name='menu_koleksi'),
    path('menu_koleksi/list_rambut/',views.list_rambut, name='list_rambut'),
    path('menu_koleksi/list_rumah/', views.list_rumah, name='list_rumah'),
    path('menu_koleksi/list_barang/', views.list_barang, name='list_barang'),
    path('menu_koleksi/list_apparel/', views.list_apparel, name='list_apparel'),
    path('menu_koleksi/list_mata/', views.list_mata, name='list_mata'),
    path('buat_koleksi/', views.buatKoleksi, name='buat_koleksi'),
    path('buat_koleksi/apparel', views.buatAppa, name='buat_apparel'),
    path('buat_koleksi/barang', views.buatBar, name='buat_barang'),
    path('buat_koleksi/mata', views.buatMat, name='buat_mata'),    
    path('buat_koleksi/rambut', views.buatRam, name='buat_rambut'),
    path('buat_koleksi/rumah', views.buatRum, name='buat_rumah'),
    path('update/apparel', views.updaAppa, name='update_apparel'),
    path('update/barang', views.updaBar, name='update_barang'),
    path('update/mata', views.updaMat, name='update_mata'),
    path('update/rambut', views.updaRam, name='update_rambut'),
    path('update/rumah', views.updaRum, name='update_rumah'),    
]
