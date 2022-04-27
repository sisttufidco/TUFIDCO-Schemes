from django.db import models
from TUFIDCOapp.models import *
# Create your models here.
def purpose_choices():
    return [
        ('Project','Project'),
        ('DPR Preparation', 'DPR Preparation')
        
    ]

def product_id_make_choices():
    a = [(str(c), str(c)) for c in
            MasterSanctionForm.objects.values_list('Project_ID', flat=True).order_by('SNo').distinct()]
    a.append(("--------", "--------"))
    return a

class ReleaseRequestModel(models.Model):
    Scheme = models.ForeignKey(Scheme, on_delete=models.CASCADE, null=True)
    AgencyType = models.ForeignKey(AgencyType, blank=True, on_delete=models.CASCADE, null=True, verbose_name='ULB Type')
    AgencyName = models.ForeignKey(AgencyName, blank=True, on_delete=models.CASCADE, null=True, verbose_name='ULB Name')
    Sector = models.CharField(max_length=100, choices=sector_make_choices(), blank=True, null=True)
    Project_ID = models.CharField(max_length=900, choices=product_id_make_choices(), blank=True, null=True, verbose_name='Project ID')
    purpose = models.CharField(max_length=900, choices=purpose_choices(), blank=True, null=True, verbose_name='Purpose of Release')
    bank_name_ulb = models.CharField('Name of the ULB', blank=True, max_length=100, null=True)
    bank_branch_name = models.CharField('Name of the Bank', blank=True, max_length=100, null=True)
    bank_branch = models.CharField('Branch', blank=True, max_length=100, null=True)
    account_number = models.CharField('Account Number', blank=True, max_length=100, null=True)
    ifsc_code = models.CharField('IFSC Code', blank=True, max_length=100, null=True)
    release1Date = models.DateField('Release Date 1', blank=True, null=True)
    release1Amount = models.CharField('Release Amount 1', blank=True, max_length=10, null=True)
    release2Date = models.DateField('Release Date 2', blank=True, null=True)
    release2Amount = models.CharField('Release Amount 2', blank=True, max_length=10, null=True)
    sqm_report2 = models.FileField('Instruction Report by SQM', upload_to='SQMreport/', blank=True, null=True)
    release3Date = models.DateField('Release Date 3', blank=True, null=True)
    release3Amount = models.CharField('Release Amount 3', blank=True, max_length=10, null=True)
    sqm_report3 = models.FileField('Instruction Report by SQM', upload_to='SQMreport/', blank=True, null=True)
    release4Date = models.DateField('Release Date 4', blank=True, null=True)
    release4Amount = models.CharField('Release Amount 4', blank=True, max_length=10, null=True)
    sqm_report4 = models.FileField('Instruction Report by SQM', upload_to='SQMreport/', blank=True, null=True)
    release5Date = models.DateField('Release Date 5', blank=True, null=True)
    release5Amount = models.CharField('Release Amount 5', blank=True, max_length=10, null=True)
    sqm_report5 = models.FileField('Instruction Report by SQM', upload_to='SQMreport/', blank=True, null=True)

    def __str__(self):
        return '{} - {}'.format(str(self.AgencyName ), str(self.Project_ID))

    class Meta:
        verbose_name = 'Ledger: Release to ULBs'
        verbose_name_plural = 'Ledger: Release to ULBs'