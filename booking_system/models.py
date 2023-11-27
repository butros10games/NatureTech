from django.db import models

# Create your models here.
class booking(models.Model):
    Identity = ()
    OrderNummer = models.IntegerField()
    StartDate = models.DateField(auto_now=False, auto_now_add=False) 
    EndDate = models.DateField(auto_now=False, auto_now_add=False)
    TimeofBooking = models.DateField()
    AgeBelow = models.IntegerField()
    AgeAbove = models.IntegerField()
    PDF = models.CharField(max_length=255)
    CheckedIn = models.BooleanField()
    Payed = models.BooleanField()
    # CampingSpot = models.ForeignKey()
    # ExtraServices = models.ForeignKey()
    # Customer = models.ForeignKey()

