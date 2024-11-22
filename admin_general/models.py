from django.db import models


# Create your models here.
class BtIpAdress(models.Model):
    ip_adress = models.CharField(max_length=20)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ip_adress

    class Meta:
        verbose_name_plural = "BT IP Adressen"
        verbose_name = "BT IP Adres"


class BtnState(models.Model):
    ip_adress = models.CharField(max_length=20)
    state = models.BooleanField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ip_adress

    class Meta:
        verbose_name_plural = "BTN presses"
        verbose_name = "BTN press"


class pirState(models.Model):
    ip_adress = models.CharField(max_length=20)
    PIR_state = models.BooleanField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ip_adress

    class Meta:
        verbose_name_plural = "PIRs info"
        verbose_name = "PIR info"


class BtMACAdress(models.Model):
    ip_adress = models.CharField(max_length=20)
    hostname = models.CharField(max_length=20, null=True, blank=True)
    BLE_rssi = models.CharField(max_length=6)
    BLE_adress = models.CharField(max_length=20)
    BLE_name = models.CharField(max_length=20)
    BLE_count = models.CharField(max_length=4)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ip_adress

    class Meta:
        verbose_name_plural = "BLEs info"
        verbose_name = "BLE info"


class get_ble_data(models.Model):
    ip_adress = models.CharField(max_length=20)
    BLE_count = models.CharField(max_length=4)
