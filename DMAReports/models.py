from django.db import models
from TUFIDCOapp.models import MasterSanctionForm
# Create your models here.

class DistrictWiseReport(MasterSanctionForm):
    class Meta:
        proxy = True
        verbose_name = "District Wise Report"
        verbose_name_plural = "District Wise Reports"