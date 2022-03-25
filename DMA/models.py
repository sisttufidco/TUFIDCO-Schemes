from django.contrib.auth.models import User
from django.db import models
from TUFIDCOapp.models import MasterSanctionForm


# Create your models here.

class DistrictWiseReport(MasterSanctionForm):
    class Meta:
        proxy = True
        verbose_name = "District Wise Report"
        verbose_name_plural = "District Wise Reports"


class MunicipalityDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    municipality_name = models.CharField('Name of Municipality', max_length=40, null=True)
    district = models.CharField('District', max_length=40, null=True)
    region = models.CharField('Region', max_length=40, null=True)
    email_id1 = models.EmailField('Email ID', max_length=40, null=True)
    email_id2 = models.EmailField('Alternative Email ID', max_length=40, blank=True, null=True)
    mc = models.CharField('Municipal Commissioner Phone Number', max_length=20, null=True)
    me = models.CharField('Municipal Engineer Phone Number', max_length=20, null=True)

    def __str__(self):
        return self.municipality_name

    class Meta:
        verbose_name = 'Municipality Detail'
        verbose_name_plural = 'Municipality Details'
