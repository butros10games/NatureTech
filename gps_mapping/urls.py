from django.urls import path
from .views import gps_index, gps_scan

urlpatterns = [
    path('', gps_index, name='gps_index'),
    path('gps_scan/', gps_scan, name='gps_scan'),
]