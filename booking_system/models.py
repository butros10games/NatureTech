from django.db import models
from django.contrib.auth.models import User

from NatureTech.programs.uuidv7 import uuid7

class Booking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid7, editable=False)
    order_number = models.IntegerField()
    start_date = models.DateField(auto_now=False, auto_now_add=False) 
    end_date = models.DateField(auto_now=False, auto_now_add=False)
    time_of_booking = models.DateTimeField(auto_now_add=True)
    age_below = models.IntegerField()
    age_above = models.IntegerField()
    pdf = models.CharField(max_length=255, blank=True, null=True)
    checked_in = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    # CampingSpot = models.ForeignKey()
    # ExtraServices = models.ForeignKey()
    customer = models.ForeignKey('Customer', on_delete=models.SET_NULL, null=True)

class Customer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid7, editable=False)
    phone_number = models.CharField(max_length=15)
    newsletter = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


