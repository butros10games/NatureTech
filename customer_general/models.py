from django.db import models

# Create your models here.
class BtIpAdress(models.Model):
    ip_adress = models.CharField(max_length=20)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ip_adress

    class Meta:
        verbose_name_plural = 'BT IP Adressen'
        verbose_name = 'BT IP Adres'