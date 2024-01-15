from django.urls import path
from .views import booking_form, confirm_booking, booking_index, beschikbaarheidsCheck, get_full_price

urlpatterns = [
    path('', booking_index, name='booking_index'),
    path('booking_form/', booking_form, name='booking_form'),
    path('confirmation/', confirm_booking, name='confirm_booking'),
    path('beschikbaarheidsCheck/', beschikbaarheidsCheck, name='beschikbaarheidsCheck'),
    path('api/total_price/', get_full_price, name='get_full_price')
]