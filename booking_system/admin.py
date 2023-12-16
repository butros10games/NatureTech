from django.contrib import admin
from .models import Booking, Customer, CampingSpot, PlekType, Price, Veld, Veldvulling

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_number', 'start_date', 'end_date', 'time_of_booking', 'age_below', 'age_above', 'pdf', 'checked_in', 'paid')
    list_filter = ('checked_in', 'paid')
    search_fields = ('order_number', 'pdf')

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone_number', 'newsletter', 'user')
    list_filter = ('newsletter',)
    search_fields = ('phone_number',)
    
@admin.register(CampingSpot)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'plekNummer', 'plekType')
    search_fields = ('plekNummer',)
    
@admin.register(Veld)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'width', 'length')
    
@admin.register(Veldvulling)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'Veld', 'PlekType', 'number')
    
@admin.register(PlekType)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'width', 'length')
    
@admin.register(Price)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'price', 'startDateTime', 'endDateTime', 'PlekType')