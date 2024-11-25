from django.contrib import admin

from .models import BtIpAdress, BtMACAdress, BtnState, pirState


# Register your models here.
class BtIpAdressAdmin(admin.ModelAdmin):
    list_display = ("ip_adress", "date")  # Fields to display in the list view
    search_fields = ("ip_adress",)  # Fields to search in the search bar
    ordering = ("-date",)  # Order by date in descending order


admin.site.register(BtIpAdress, BtIpAdressAdmin)


class BtnStateAdmin(admin.ModelAdmin):
    list_display = ("ip_adress", "state", "date")  # Fields to display in the list view


admin.site.register(BtnState, BtnStateAdmin)


class pirStateAdmin(admin.ModelAdmin):
    list_display = (
        "ip_adress",
        "PIR_state",
        "date",
    )  # Fields to display in the list view


admin.site.register(pirState, pirStateAdmin)


class BtMACAdressAdmin(admin.ModelAdmin):
    list_display = (
        "ip_adress",
        "hostname",
        "BLE_rssi",
        "BLE_adress",
        "BLE_name",
        "BLE_count",
        "date",
    )  # Fields to display in the list view


admin.site.register(BtMACAdress, BtMACAdressAdmin)
