from django.db import models
from ULBForms.models import *
from TUFIDCOapp.models import *

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


class ProgressNotEntered(MasterSanctionForm):
    class Meta:
        proxy = True
        verbose_name = 'Progress Detail Not Entered'
        verbose_name_plural = 'Progress Details Not Entered'


class SanctionNotEntered(MasterSanctionForm):
    class Meta:
        proxy = True
        verbose_name = 'Sanction Detail Not Entered'
        verbose_name_plural = 'Sanction Details Not Entered'


class PanDetailsNotEntered(ULBPanCard):
    class Meta:
        proxy = True
        verbose_name = 'PAN Detail Not Filled in'
        verbose_name_plural = 'PAN Details Not Filld in'


class BankDetailsNotEntered(AgencyBankDetails):
    class Meta:
        proxy = True
        verbose_name = 'Bank Detail Not Filled in'
        verbose_name_plural = 'Bank Details Not Filled in'

