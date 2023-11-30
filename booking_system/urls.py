from django.urls import path
from .views import booking_form, confirm_booking, contact_form

urlpatterns = [
    path('booking_form', booking_form, name='booking_form'),
    path('confirmation', confirm_booking, name='confirm_booking'),
    path('contact_form', contact_form, name='contact_form')
]