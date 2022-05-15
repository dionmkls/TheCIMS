from django.urls import path
from .views import readTokoh, detailTokoh

urlpatterns = [
    path('listTokoh', readTokoh, name='listTokoh'),
    path('detailtokoh', detailTokoh, name='detailTokoh')
]