from django.urls import path
from .views import admin_index, booking_context, sort_bookings

urlpatterns = [
    path('', admin_index, name='booking_index'),
    path('booking_context/', booking_context, name='booking_context'),
    path('sort_bookings/', sort_bookings, name='sort_bookings')
] 