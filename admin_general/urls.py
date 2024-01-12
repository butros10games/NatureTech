from django.urls import path
from .views import admin_index, booking_context, sort_bookings, create_modal, save_modal, usage_data

urlpatterns = [
    path('', admin_index, name='booking_index'),
    path('booking_context/', booking_context, name='booking_context'),
    path('sort_bookings/', sort_bookings, name='sort_bookings'),
    path('create_modal/', create_modal, name='create_modal'),
    path('usage_data/', usage_data, name='usage_data'),
    path('save_modal/', save_modal, name='save_modal')
] 