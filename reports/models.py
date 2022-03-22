from django.db import models
from ULBForms.models import AgencyProgressModel


# Create your models here.

class ULBProgressReport(AgencyProgressModel):
    class Meta:
        proxy = True
        verbose_name = 'ULB Progress Report'
        verbose_name_plural = 'ULB Progress Report'
