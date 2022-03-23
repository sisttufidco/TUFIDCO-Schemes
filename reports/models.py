from django.db import models
from ULBForms.models import AgencyProgressModel, AgencySanctionModel


# Create your models here.

class ULBProgressIncompleted(AgencyProgressModel):
    class Meta:
        proxy = True
        verbose_name = 'Portal Progress Detail'
        verbose_name_plural = 'Portal Progress Details'


class ULBSanctionReportError(AgencySanctionModel):
    class Meta:
        proxy = True
        verbose_name = 'Portal Sanction Detail'
        verbose_name_plural = 'Portal Sanction Details'
