from django.urls import path
from .views import readTokoh, detailTokoh

urlpatterns = [
    path('listTokoh', readTokoh, name='index'),
    path('detailtokoh', detailTokoh, name='index')
]