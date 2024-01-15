from django.db import models
from django.contrib.auth.models import User    

from NatureTech.programs.uuidv7 import uuid7

class Booking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid7, editable=False)
    order_number = models.IntegerField(unique=True)
    start_date = models.DateField(auto_now=False, auto_now_add=False) 
    end_date = models.DateField(auto_now=False, auto_now_add=False)
    time_of_booking = models.DateTimeField(auto_now_add=True)
    age_below = models.IntegerField(null=True, blank=True)
    age_above = models.IntegerField(null=True, blank=True)
    pdf = models.CharField(max_length=255, blank=True, null=True)
    checked_in = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    CampingSpot = models.ForeignKey('CampingSpot', on_delete=models.SET_NULL, null=True)
    # ExtraServices = models.ForeignKey()
    customer = models.ForeignKey('Customer', on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
        if not self.order_number:
            # Get the maximum order_number from the existing entries
            last_order = Booking.objects.all().order_by('order_number').last()
            if last_order:
                self.order_number = last_order.order_number + 1
            else:
                self.order_number = 1
        super(Booking, self).save(*args, **kwargs)

class Customer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid7, editable=False)
    phone_number = models.CharField(max_length=15)
    newsletter = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='customer')
    kenteken_auto = models.CharField(max_length=255, blank=True, null=True)
    postal_code = models.CharField(max_length=255, blank=True, null=True)
    street = models.CharField(max_length=255, blank=True, null=True)
    house_number = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)

class CampingSpot(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid7, editable=False)
    plekNummer = models.IntegerField()
    plekType = models.ForeignKey('PlekType', on_delete=models.SET_NULL, null=True)
    veld = models.ForeignKey('Veld', on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return str(self.plekNummer)
    
class PlekType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid7, editable=False)
    name = models.CharField(max_length=255)
    width = models.IntegerField()
    length = models.IntegerField()
    omschrijving = models.TextField(blank=True, null=True)
    fixed_price = models.CharField(max_length=255, blank=True, null=True)
    daily_price = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return self.name
    
class Price(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid7, editable=False)
    name = models.CharField(max_length=255, blank=True, null=True)
    price = models.IntegerField()
    startDateTime = models.DateTimeField(auto_now=False, auto_now_add=False)
    endDateTime = models.DateTimeField(auto_now=False, auto_now_add=False)
    PlekType = models.ForeignKey('PlekType', on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return str(self.PlekType)
    
class Veld(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid7, editable=False)
    name = models.CharField(max_length=255)
    width = models.IntegerField()
    length = models.IntegerField()
    
    def __str__(self):
        return self.name
    
class Veldvulling(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid7, editable=False)
    Veld = models.ForeignKey('Veld', on_delete=models.SET_NULL, null=True)
    PlekType = models.ForeignKey('PlekType', on_delete=models.SET_NULL, null=True)
    number = models.IntegerField()
    
    def __str__(self):
        return str(self.Veld)
    
class VeldGps(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid7, editable=False)
    veld = models.ForeignKey('Veld', on_delete=models.SET_NULL, null=True)
    lat = models.FloatField()
    lng = models.FloatField()
    
    def __str__(self):
        return str(self.veld)