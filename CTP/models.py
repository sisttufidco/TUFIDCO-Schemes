from django.contrib.auth.models import User
from django.db import models
from django.utils.datetime_safe import datetime
from TUFIDCOapp.models import *
from ULBForms.models import *


# Create your models here.
class TownPanchayatDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    name_tp = models.CharField('Name of Town Panchayat', max_length=40, null=True)
    district = models.CharField('District', max_length=40, null=True)
    zone = models.CharField('Zone', max_length=40, null=True)
    cell1 = models.CharField('Executive officer ( Cell No 1)', max_length=20, null=True)
    cell2 = models.CharField('Engineer Official Level 1 / AE ( Cell No 2)', max_length=20, blank=True, null=True)
    cell3 = models.CharField('Engineer Official Level 2 / JE ( Cell No 3)', max_length=20, blank=True, null=True)
    email = models.EmailField('Email ID', max_length=40, null=True)
    date_and_time = models.DateTimeField(default=datetime.now, null=True)

    def __str__(self):
        return self.name_tp

    class Meta:
        verbose_name = 'Town Panchayat Detail'
        verbose_name_plural = 'Town Panchayat Details'


class MasterReport(MasterSanctionForm):
    class Meta:
        proxy = True
        verbose_name = "KNMT Physical & Financial Progress Report"
        verbose_name_plural = "KNMT Physical & Financial Progress Reports"

class CTPDistrictWiseReport(MasterSanctionForm):
    class Meta:
        proxy = True
        verbose_name = "District Wise Report"
        verbose_name_plural = "District Wise Report"