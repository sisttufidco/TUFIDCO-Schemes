from django.contrib.auth.models import User
from django.db import models
from django.utils.datetime_safe import datetime

# Create your models here.
class TownPanchayatDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    name_tp = models.CharField('Name of Town Panchayat', max_length=40, null=True)
    district = models.CharField('District', max_length=40, null=True)
    zone = models.CharField('Zone', max_length=40, null=True)
    cell1 = models.CharField('Cell 1', max_length=20, null=True)
    cell2 = models.CharField('Cell 2', max_length=20, blank=True, null=True)
    cell3 = models.CharField('Cell 3', max_length=20, blank=True, null=True)
    email = models.EmailField('Email ID', max_length=40, null=True)
    date_and_time = models.DateTimeField(default=datetime.now, null=True)
    def __str__(self):
        return self.name_tp

    class Meta:
        verbose_name = 'Town Panchayat Detail'
        verbose_name_plural = 'Town Panchayat Details'
