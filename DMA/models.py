from django.contrib.auth.models import User
from django.db import models
from TUFIDCOapp.models import MasterSanctionForm
from django.utils.datetime_safe import datetime

# Create your models here.

class DistrictWiseReport(MasterSanctionForm):
    class Meta:
        proxy = True
        verbose_name = "District Wise Report"
        verbose_name_plural = "District Wise Report"


class MunicipalityDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    municipality_name = models.CharField('Name of Municipality', max_length=40, null=True)
    district = models.CharField('District', max_length=40, null=True)
    region = models.CharField('Region', max_length=40, null=True)
    email_id1 = models.EmailField('Email ID', max_length=40, null=True)
    email_id2 = models.EmailField('Alternative Email ID', max_length=40, blank=True, null=True)
    mc = models.CharField('Municipal Commissioner Phone Number', max_length=20, null=True)
    me = models.CharField('Municipal Engineer Phone Number', max_length=20, null=True)
    date_and_time = models.DateTimeField(default=datetime.now, null=True)
    def __str__(self):
        return self.municipality_name

    class Meta:
        verbose_name = 'Municipality Detail'
        verbose_name_plural = 'Municipality Details'


class MasterReport(MasterSanctionForm):
    class Meta:
        proxy = True
        verbose_name = "KNMT Physical & Financial Progress Report"
        verbose_name_plural = "KNMT Physical & Financial Progress Reports"