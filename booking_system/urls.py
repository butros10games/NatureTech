from django.urls import path
from .views import booking_form, confirm_booking

urlpatterns = [
    path('booking_form', booking_form, name='booking_form'),
    path('confirmation', confirm_booking, name='confirm_booking'),
]