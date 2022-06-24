from django.contrib.auth.models import User
from django.db import models
from TUFIDCOapp.models import MasterSanctionForm
from django.utils.datetime_safe import datetime

class GCCDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    corporation_name = models.CharField('Name of Corporation', max_length=40, null=True)
    district = models.CharField('District', max_length=40, null=True)
    region = models.CharField('Region', max_length=40, null=True)
    email_id1 = models.EmailField('Email ID', max_length=40, null=True)
    email_id2 = models.EmailField('Alternative Email ID', max_length=40, blank=True, null=True)
    mc = models.CharField('GCC Commissioner Phone Number', max_length=20, null=True)
    me = models.CharField('GCC Engineer Phone Number', max_length=20, null=True)
    date_and_time = models.DateTimeField(default=datetime.now, null=True)
    
    def __str__(self):
        return self.corporation_name

    class Meta:
        verbose_name = 'GCC Detail'
        verbose_name_plural = 'GCC Details'