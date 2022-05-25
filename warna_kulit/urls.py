from django.urls import path

from . import views

app_name = 'warna_kulit'

urlpatterns = [
    path('',views.index, name='index'),
    path('createWarnaKulit/',views.createWarnaKulit, name='createWarnaKulit'),
    path('deleteWarnaKulit/<str:kode>',views.deleteWarnaKulit, name='deleteWarnaKulit'),
]