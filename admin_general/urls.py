from django.urls import path
from .views import admin_index

urlpatterns = [
    path('', admin_index, name='booking_index'),
]