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
    # CampingSpot = models.ForeignKey()
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
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


class Notes(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid7, editable=False)
    message_note = models.CharField(max_length=255, blank=True, null=True)
    booking_note = models.CharField(max_length=255, blank=True, null=True)
    staff_note = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    customer = models.ForeignKey('Customer', on_delete=models.SET_NULL, null=True)




