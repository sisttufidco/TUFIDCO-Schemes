from weakref import proxy
from django.contrib.auth.models import User
from django.db import models
from django.utils.safestring import mark_safe
import ULBForms

"""
    Models
    1. tufidco_info
    2. Officer
    3. body_images
    4. postphotogallery_slider
"""


class tufidco_info(models.Model):
    logo = models.ImageField(upload_to='headerimages/')
    title = models.TextField(blank=True, null=True)
    govt_title = models.TextField(blank=True, null=True)
    india_flag = models.ImageField(upload_to='headerimages/', null=True)
    tamilnadulogo = models.ImageField(upload_to='headerimages/', null=True)
    Number = models.CharField(max_length=13, null=True)
    about = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    fax = models.TextField(blank=True, null=True)
    webURL = models.CharField(max_length=20, null=True)

    class Meta:
        verbose_name = "Tufidco Info"
        verbose_name_plural = "Tufidco Infos"


class Officer(models.Model):
    name = models.CharField(max_length=40, null=True)
    Designation = models.CharField(max_length=40, null=True)

    class Meta:
        verbose_name = "Officer"
        verbose_name_plural = "Officers"


class body_images(models.Model):
    main_slider = models.FileField(null=True, blank=True)
    reform_slider = models.FileField(null=True, blank=True)
    photogallery_slider = models.FileField(blank=True, null=True)

    class Meta:
        verbose_name = "Body Image"
        verbose_name_plural = "Body Images"


class postphotogallery_slider(models.Model):
    body_img = models.ForeignKey(body_images, default=None, on_delete=models.CASCADE)
    photogallery_sliders = models.FileField(upload_to='photogallery/', null=True)


class postreformslider(models.Model):
    reform_img = models.ForeignKey(body_images, default=None, on_delete=models.CASCADE)
    title = models.CharField(max_length=30, blank=True, null=True)
    reform_sliders = models.FileField(upload_to='reforms/', null=True)


class postmainslider(models.Model):
    mainslider = models.ForeignKey(body_images, default=None, on_delete=models.CASCADE)
    mainsliders = models.FileField(upload_to='mainslider/', null=True)


class About(models.Model):
    title = models.CharField(max_length=200, null=True)
    about_text = models.TextField(null=True)


class gallery_Images(models.Model):
    gallery_img = models.FileField(upload_to='gallery/', null=True)
    place = models.CharField(max_length=40, null=True)
    type = models.CharField(max_length=40, blank=True, null=True)
    Date = models.DateField(null=True)

    @property
    def image_preview(self):
        if self.gallery_img:
            return mark_safe('<img src="{}" width="300" height="300" />'.format(self.gallery_img.url))
        return ""

    class Meta:
        verbose_name = "Gallery Image"
        verbose_name_plural = "Gallery Images"


class Scheme(models.Model):
    Scheme = models.CharField('Scheme', max_length=80, null=True)

    def __str__(self):
        return self.Scheme


class Scheme_Faq_Questions(models.Model):
    name = models.ForeignKey(Scheme, on_delete=models.CASCADE, null=True)
    question_id = models.CharField('Number', max_length=50, null=True)
    question = models.TextField(null=True)
    answer = models.TextField(null=True)

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = "Scheme FAQ Question"
        verbose_name_plural = "Scheme FAQ Questions"


class Scheme_Page(models.Model):
    scheme = models.ForeignKey('Scheme', on_delete=models.CASCADE, null=True)
    name = models.CharField('Name', max_length=200, null=True)
    introduction = models.TextField("Introduction", null=True)
    ppt1 = models.FileField(upload_to="pdf/", blank=True, null=True)
    ppt_name = models.CharField("PPT Name", max_length=100, blank=True, null=True)
    pdf_guidelines = models.FileField(upload_to="pdf/", blank=True, null=True)
    pdf_guidelines2 = models.CharField("PDF Name", max_length=100, blank=True, null=True)

    def __str__(self):
        return str(self.scheme)

    class Meta:
        verbose_name = "Scheme Page"
        verbose_name_plural = "Scheme Pages"


class SchemeSanctionPdf(models.Model):
    scheme = models.ForeignKey('Scheme', on_delete=models.CASCADE, null=True)
    pdf = models.FileField(upload_to='pdf/', blank=True, null=True)
    Pdf_name = models.CharField('PDF Name', max_length=200, null=True)

    def __str__(self):
        return self.Pdf_name


class PageCounter(models.Model):
    count = models.IntegerField('Page Counter', null=True)

    def __str__(self):
        return str(self.count)


# Master Sanction Form


class AgencyType(models.Model):
    AgencyType = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.AgencyType

    class Meta:
        verbose_name = "ULB Type"
        verbose_name_plural = "ULB Types"


class AgencyName(models.Model):
    Pid = models.IntegerField(blank=True, null=True)
    AgencyName = models.CharField('AgencyName', max_length=80, null=True)
    AgencyType = models.ForeignKey(AgencyType, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.AgencyName

    class Meta:
        verbose_name = "ULB Name"
        verbose_name_plural = "ULB Names"


class District(models.Model):
    Pid = models.IntegerField(blank=True, null=True)
    District = models.CharField('District', max_length=80, null=True)
    Latitude = models.DecimalField("Latitude", blank=True, decimal_places=4, max_digits=10, null=True)
    Longitude = models.DecimalField('Longitude', blank=True, decimal_places=4, max_digits=10, null=True)

    def __str__(self):
        return self.District


class Region(models.Model):
    id = models.IntegerField(blank=True, null=True)
    Pid = models.IntegerField(primary_key=True)
    Region = models.CharField('Region', max_length=80, null=True)

    def __str__(self):
        return self.Region


class MasterSanctionForm(models.Model):
    SNo = models.IntegerField("S.No.", blank=True, null=True)
    AgencyType = models.ForeignKey(AgencyType, blank=True, on_delete=models.CASCADE, null=True, verbose_name="ULB Type")
    AgencyName = models.ForeignKey(AgencyName, blank=True, on_delete=models.CASCADE, null=True, verbose_name="ULB Name")
    District = models.ForeignKey(District, blank=True, on_delete=models.CASCADE, null=True)
    Region = models.ForeignKey(Region, blank=True, on_delete=models.CASCADE, null=True)
    Scheme = models.ForeignKey(Scheme, blank=True, on_delete=models.CASCADE, null=True)
    Sector = models.CharField("Sector", max_length=200, blank=True, null=True)
    ProjectName = models.TextField("Name of the Work", blank=True, null=True)
    ProjectCost = models.DecimalField("Project Cost", decimal_places=2, blank=True, max_digits=10, null=True)
    ProposedCostByULB = models.DecimalField("Proposed Cost by ULB", decimal_places=2, blank=True, max_digits=10,
                                            null=True)
    ApprovedProjectCost = models.DecimalField("Approved Project Cost", blank=True, decimal_places=2, max_digits=10,
                                              null=True)
    SchemeShare = models.DecimalField("Scheme Share", decimal_places=2, blank=True, max_digits=10, null=True)
    ULBShare = models.DecimalField("ULB Share", decimal_places=2, blank=True, max_digits=10, null=True)
    GoMeeting = models.IntegerField("GO", blank=True, null=True)
    Date_AS = models.DateField("Date of AS", blank=True, null=True)
    Project_ID = models.CharField('Project ID', max_length=40, blank=True, null=True)
    total = models.DecimalField("Total", decimal_places=2, blank=True, max_digits=10, null=True)
    zone = models.IntegerField("Zone", blank=True, null=True)

    def save(self, **kwargs):
        self.Project_ID = "%s_%s_%.3d_%d_%s_%.4d" % (self.Scheme.Scheme[:1],
                                                     self.AgencyType.AgencyType[:1] + self.AgencyType.AgencyType[
                                                                                      5:6].upper(),
                                                     self.GoMeeting, self.Date_AS.year, self.Sector[0:1], self.SNo)
        self.total = "%f" % (self.SchemeShare + self.ULBShare)
        super(MasterSanctionForm, self).save(**kwargs)

    class Meta:
        verbose_name = "Master Sanction Detail"
        verbose_name_plural = "Master Sanction Details"

    def __str__(self):
        return self.Project_ID


class Report(MasterSanctionForm):
    class Meta:
        proxy = True
        verbose_name = 'GO Wise Report'
        verbose_name_plural = 'GO Wise Reports'


# Agency Form


class MasterReport(MasterSanctionForm):
    class Meta:
        proxy = True
        verbose_name = "KNMT Physical & Financial Progress Report"
        verbose_name_plural = "KNMT Physical & Financial Progress Reports"


class SectorMasterReport(MasterSanctionForm):
    class Meta:
        proxy = True
        verbose_name = "Sector wise Report"
        verbose_name_plural = "Sector wise Reports"


class CTPDistrictWiseReport(MasterSanctionForm):
    class Meta:
        proxy = True
        verbose_name = 'District Wise Report (CTP)'
        verbose_name_plural = 'District Wise Report (CTP)'


class FundReleaseDetails(models.Model):
    date_of_release = models.DateField('Date of Release', null=True)
    amount = models.CharField('Amount', max_length=20, null=True)
    instruction_report_by_SQM = models.FileField(upload_to='SQMreport/', null=True)
    masterSanctionForm = models.ForeignKey(MasterSanctionForm, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Fund Release Detail"
        verbose_name_plural = "pytd Release Details"


class ULBReleaseRequest(models.Model):
    scheme = models.ForeignKey(Scheme, on_delete=models.CASCADE, null=True)
    name_of_form = models.CharField("Name of form", max_length=50, null=True)
    form = models.FileField(upload_to='ReleaseRequest/', null=True)

    def __str__(self):
        return self.name_of_form

    class Meta:
        verbose_name = 'ULB Release Request'
        verbose_name_plural = 'ULB Release Requests'


class LatestReports(models.Model):
    Scheme = models.ForeignKey(Scheme, on_delete=models.CASCADE, null=True)
    name = models.CharField('Name', max_length=50, null=True)
    report = models.FileField(upload_to='reports/', null=True)

    def __str__(self):
        return self.name


def sector_make_choices():
    return [(str(c), str(c)) for c in MasterSanctionForm.objects.values_list('Sector', flat=True).distinct()]


def product_id_make_choices():
    return [(str(c), str(c)) for c in
            MasterSanctionForm.objects.values_list('Project_ID', flat=True).order_by('SNo').distinct()]


class ReleaseRequestModel(models.Model):
    Scheme = models.ForeignKey(Scheme, on_delete=models.CASCADE, null=True)
    AgencyType = models.ForeignKey(AgencyType, blank=True, on_delete=models.CASCADE, null=True, verbose_name='ULB Type')
    AgencyName = models.ForeignKey(AgencyName, blank=True, on_delete=models.CASCADE, null=True, verbose_name='ULB Name')
    Sector = models.CharField(max_length=100, choices=sector_make_choices(), blank=True, null=True)
    Project_ID = models.CharField(max_length=900, choices=product_id_make_choices(), blank=True, null=True)
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
        return '{} - {}'.format(str(self.ULBName), str(self.Project_ID))

    class Meta:
        verbose_name = 'Ledger: Release to ULBs'
        verbose_name_plural = 'Ledger: Release to ULBs'


# Special Road Programme Scheme

class SRPMasterSanctionForm(models.Model):
    SNo = models.IntegerField('S No.', null=True)
    AgencyName = models.ForeignKey(AgencyName, on_delete=models.CASCADE, verbose_name='ULB Name', null=True)
    AgencyType = models.ForeignKey(AgencyType, on_delete=models.CASCADE, verbose_name='ULB Type', null=True)
    Project_ID = models.CharField('Project ID', max_length=10, null=True)
    ProjectCost = models.DecimalField('Project Cost', max_digits=8, decimal_places=2, null=True)
    SchemeShare = models.DecimalField('Scheme Share', max_digits=8, decimal_places=2, null=True)
    R1_Date = models.DateField('Date of 1st Release', blank=True, null=True)
    R1_Amount = models.DecimalField('Amount', max_digits=8, decimal_places=2, blank=True, null=True)
    R2_Date = models.DateField('Date of 2nd Release', blank=True, null=True)
    R2_Amount = models.DecimalField('Amount', max_digits=8, decimal_places=2, blank=True, null=True)
    R_Total = models.DecimalField('Total Released', max_digits=8, decimal_places=2, blank=True, null=True)
    Balance = models.DecimalField('Balance', max_digits=8, decimal_places=2, blank=True, null=True)
    Dropped = models.DecimalField('Dropped Amount', max_digits=8, blank=True, decimal_places=2, null=True)
    BalanceEligible = models.DecimalField('Eligible for loan', max_digits=8, blank=True, decimal_places=2, null=True)

    def __str__(self):
        return str(self.Project_ID)

    class Meta:
        verbose_name = 'SRP Master Sanction Form'
        verbose_name_plural = 'SRP Master Sanction Form'


class ReceiptForm(models.Model):
    Scheme = models.ForeignKey(Scheme, on_delete=models.CASCADE, null=True)
    go_ref = models.CharField('GO ref.', max_length=30, null=True)
    go_date = models.DateField('GO Date', null=True)
    purpose = models.TextField('Purpose', null=True, help_text='Scheme/Management Fee')
    amount = models.DecimalField('Amount', max_digits=6, decimal_places=2, null=True)

    def __str__(self):
        return '{} - {} - {}'.format(self.Scheme, self.go_ref, self.go_ref, self.go_date)

    class Meta:
        verbose_name = 'Receipt Form'
        verbose_name_plural = 'Receipt Form'
