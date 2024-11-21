from django.urls import path

from .views import admin_index, booking_context

urlpatterns = [
    path("", admin_index, name="booking_index"),
    path("booking_context/", booking_context, name="booking_context"),
]
