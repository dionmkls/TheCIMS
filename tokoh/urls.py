from django.urls import path
from . import views

app_name = 'tokoh'

urlpatterns = [
    path('', views.index, name='index'),
    path('detailTokoh/', views.detailTokoh, name='detailTokoh'),
    path('createTokoh/', views.createTokoh, name='createTokoh'),
]