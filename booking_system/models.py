from django.db import models

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
    # Customer = models.ForeignKey()

