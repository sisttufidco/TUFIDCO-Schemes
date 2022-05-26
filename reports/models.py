from tabnanny import verbose
from django.db import models
from ULBForms.models import AgencyProgressModel, AgencySanctionModel
from TUFIDCOapp.models import *


# Create your models here.




class SRPAbstract(SRPMasterSanctionForm):
    class Meta:
        proxy = True
        verbose_name = 'SRP Abstract'
        verbose_name_plural = 'SRP Abstract'


class SectorMasterReport(MasterSanctionForm):
    class Meta:
        proxy = True
        verbose_name = "Sector wise Report"
        verbose_name_plural = "Sector wise Reports"

class Report(MasterSanctionForm):
    class Meta:
        proxy = True
        verbose_name = 'GO Wise Report'
        verbose_name_plural = 'GO Wise Reports'

class PhysicalandFinancialReport(MasterSanctionForm):
    class Meta:
        proxy = True
        verbose_name = "KNMT Physical & Financial Progress Report"
        verbose_name_plural = "KNMT Physical & Financial Progress Reports"

class DistrictWiseReport(MasterSanctionForm):
    class Meta:
        proxy = True
        verbose_name = "District Wise Report"
        verbose_name_plural = "District Wise Report"

class SingaraChennaiPhysicalandFinancialReport(MasterSanctionForm):
    class Meta:
        proxy=True
        verbose_name = "Singara Chennai 2.0 Physical & Financial Progress Report"
        verbose_name_plural = "Singara Chennai 2.0 Physical & Financial Progress Report"