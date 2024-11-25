from django.contrib import admin

from .models import (
    Booking,
    CampingSpot,
    Customer,
    PlekType,
    Price,
    Veld,
    VeldGps,
    Veldvulling,
)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order_number",
        "start_date",
        "end_date",
        "time_of_booking",
        "age_below",
        "age_above",
        "pdf",
        "checked_in",
        "paid",
    )
    list_filter = ("checked_in", "paid")
    search_fields = ("order_number", "pdf")


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("id", "phone_number", "newsletter", "user")
    list_filter = ("newsletter",)
    search_fields = ("phone_number",)


@admin.register(CampingSpot)
class CampingSpotAdmin(admin.ModelAdmin):
    list_display = ("id", "plekNummer", "plekType")
    search_fields = ("plekNummer",)


@admin.register(Veld)
class VeldAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "width", "length")


@admin.register(Veldvulling)
class VeldvullingAdmin(admin.ModelAdmin):
    list_display = ("id", "Veld", "PlekType", "number")


@admin.register(PlekType)
class PlekTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "width", "length")


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ("id", "price", "startDateTime", "endDateTime", "PlekType")


@admin.register(VeldGps)
class VeldGpsAdmin(admin.ModelAdmin):
    list_display = ("id", "veld", "lat", "lng")
