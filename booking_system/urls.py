from django.urls import path

from .views import (
    beschikbaarheidsCheck,
    booking_form,
    booking_index,
    confirm_booking,
    get_full_price,
)

urlpatterns = [
    path("", booking_index, name="booking_index"),
    path("booking_form/", booking_form, name="booking_form"),
    path("confirmation/", confirm_booking, name="confirm_booking"),
    path("beschikbaarheidsCheck/", beschikbaarheidsCheck, name="beschikbaarheidsCheck"),
    path("api/total_price/", get_full_price, name="get_full_price"),
]
