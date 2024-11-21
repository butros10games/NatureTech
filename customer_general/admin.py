from django.contrib import admin

from .models import BtIpAdress


class BtIpAdressAdmin(admin.ModelAdmin):
    list_display = ("ip_adress", "date")  # Fields to display in the list view
    search_fields = ("ip_adress",)  # Fields to search in the search bar
    ordering = ("-date",)  # Order by date in descending order


admin.site.register(BtIpAdress, BtIpAdressAdmin)
