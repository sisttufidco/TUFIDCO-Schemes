from django.contrib.auth.models import User
from django.db import models
from django.utils.safestring import mark_safe
from TUFIDCOapp.models import Scheme, MasterSanctionForm, AgencyType, District
from mapbox_location_field.models import LocationField

# Create your models here.


class AgencyBankDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    beneficiary_name = models.CharField("Name of the ULB", max_length=90, null=True)
    bank_name = models.CharField("Name of the Bank", max_length=90, null=True)
    branch = models.CharField("Branch", max_length=90, null=True)
    account_number = models.CharField("Account Number", max_length=90, null=True)
    IFSC_code = models.CharField("IFSC Code", max_length=20, null=True)
    passbookupload = models.FileField("Passbook Front Page Photo", upload_to='passbook/', null=True
                                      , help_text='Please attach a clear scanned copy front page of the Bank passbook')

    @property
    def passbook_preview(self):
        if self.passbookupload:
            return mark_safe('<img src="{}" width="300" height="300" />'.format(self.passbookupload.url))
        return ""

    def __str__(self):
        return self.beneficiary_name

    class Meta:
        verbose_name = "ULB Bank Detail"
        verbose_name_plural = "ULB Bank Details"

class ULBPanCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    PANno = models.CharField("PAN Number", max_length=60, null=True)
    name = models.CharField("Name", max_length=60, null=True)
    panphoto = models.FileField("PAN Photo", upload_to='PAN/', null=True,
                                help_text="Please Upload a Clear Scanned Copy of PAN")

    @property
    def pan_preview(self):
        if self.panphoto:
            return mark_safe('<img src="{}" width="300" height="300" />'.format(self.panphoto.url))
        return ""

    def __str__(self):
        return self.user.first_name

    class Meta:
        verbose_name = "ULB PAN Detail"
        verbose_name_plural = "ULB PAN Details"

def scheme_make_choices():
    return [(str(c), str(c)) for c in Scheme.objects.all()]


def sector_make_choices():
    return [(str(c), str(c)) for c in MasterSanctionForm.objects.values_list('Sector', flat=True).distinct()]


def product_id_make_choices():
    return [(str(c), str(c)) for c in
            MasterSanctionForm.objects.values_list('Project_ID', flat=True).order_by('SNo').distinct()]


def status_choices():
    return [('In Progress', 'In Progress'),
            ('Completed', 'Completed'),
            ('Not Commenced', 'Not Commenced')]


class AgencyProgressModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    Scheme = models.CharField(max_length=30, choices=scheme_make_choices(), blank=True, null=True)
    Sector = models.CharField(max_length=100, choices=sector_make_choices(), blank=True, null=True)
    Project_ID = models.CharField(max_length=900, choices=product_id_make_choices(), blank=True, null=True)
    Latitude = models.CharField("Latitude", max_length=20, blank=True, null=True)
    Longitude = models.CharField("Longitude", max_length=20, blank=True, null=True)
    location = LocationField(
        map_attrs={"style": 'mapbox://styles/mapbox/satellite-v9',
                   "center": (80.2319139, 13.0376246),
                   "cursor_style": 'pointer',
                   "marker_color": "Blue",
                   "rotate": True,
                   "geocoder": True,
                   "fullscreen_button": True,
                   "navigation_buttons": True,
                   "track_location_button": True,
                   "readonly": True,
                   "zoom": 15,
                   }, blank=True, null=True)
    ProjectName = models.TextField("Project Name", blank=True, null=True)
    PhysicalProgress = models.TextField("Physical Progress", blank=True, null=True)
    status = models.CharField(max_length=20, choices=status_choices(), default='Not Commenced', blank=False, null=True)
    Expenditure = models.CharField("Expenditure (in lakhs)", max_length=50, blank=True, null=True)
    FundRelease = models.CharField("Fund Release (in lakhs)", max_length=50, blank=True, null=True,
                                   help_text="Agency has to send a hard copy of the release request along with "
                                             "photos,etc in the prescribed format")
    valueofworkdone = models.DecimalField("Value of Work done (in lakhs)", decimal_places=2, max_digits=12, blank=True,
                                          default=0.0, null=True)
    percentageofworkdone = models.DecimalField("Percentage of work done", decimal_places=2, max_digits=12, blank=True,
                                               default=0.0, null=True)
    upload1 = models.FileField("upload", upload_to="agencysanctionlocation/", null=True,
                               help_text="Please upload a photo of site with location matching with the google maps",
                               blank=True)
    District = models.CharField('District', max_length=50, blank=True, null=True)
    ApprovedProjectCost = models.DecimalField("Approved Project Cost", blank=True, decimal_places=2, max_digits=10,
                                              null=True)
    upload2 = models.FileField("upload", upload_to="agencysanction/", blank=True, null=True)

    def save(self, **kwargs):
        self.location = "%s, %s" % (self.Longitude, self.Latitude)
        self.Sector = MasterSanctionForm.objects.values_list('Sector', flat=True).filter(Project_ID=self.Project_ID)
        self.District = MasterSanctionForm.objects.values_list('District__District', flat=True).filter(
            Project_ID=self.Project_ID)
        self.ApprovedProjectCost = MasterSanctionForm.objects.values_list('ApprovedProjectCost', flat=True).filter(
            Project_ID=self.Project_ID)
        print(self.ApprovedProjectCost[0])
        if (self.valueofworkdone != None):
            self.percentageofworkdone = (
                round(float(self.valueofworkdone) / float(self.ApprovedProjectCost[0]) * 100, 2))
        else:
            self.percentageofworkdone = (0.00)
        super(AgencyProgressModel, self).save(**kwargs)

    def __str__(self):
        return '{} - {} - {}'.format(str(self.Scheme), str(self.user.first_name), str(self.Project_ID))

    class Meta:
        verbose_name = 'ULB Progress Detail'
        verbose_name_plural = 'ULB Progress Details'


class AgencySanctionModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    Scheme = models.CharField(max_length=30, choices=scheme_make_choices(), blank=True, null=True)
    Sector = models.CharField(max_length=100, choices=sector_make_choices(), blank=True, null=True)
    Project_ID = models.CharField(max_length=900, choices=product_id_make_choices(), blank=True, null=True)
    ProjectName = models.TextField("Project Name", blank=True, null=True)

    tsrefno = models.CharField("Technical Sanction Reference No.", max_length=30, blank=True, null=True)
    tsdate = models.DateField("Technical Sanction Date", blank=True, null=True)
    tawddate = models.DateField("Tender Awarded Date", blank=True, null=True)
    wdawddate = models.DateField("Work Order Awarded Date", blank=True, null=True)
    YN_CHOICES = (
        ('0', 'Yes'),
        ('0', 'No'),
    )
    ts_awarded = models.CharField("Technical Sanction Awarded", max_length=20, blank=True, choices=YN_CHOICES,
                                  null=True)
    tr_awarded = models.CharField("Tender Sanction Awarded", max_length=20, blank=True, choices=YN_CHOICES, null=True)
    wd_awarded = models.CharField("Work Order Awarded", max_length=20, blank=True, choices=YN_CHOICES, null=True)

    def save(self, **kwargs):
        self.Sector = MasterSanctionForm.objects.values_list('Sector', flat=True).filter(Project_ID=self.Project_ID)
        super(AgencySanctionModel, self).save(**kwargs)

    def __str__(self):
        return '{} - {} - {}'.format(str(self.Scheme), str(self.user.first_name), str(self.Project_ID))

    class Meta:
        verbose_name = "ULB Project Sanction Detail"
        verbose_name_plural = "ULB Project Sanction Details"


class ULBDetails(models.Model):
    ulbName = models.CharField('Name of the ULB', max_length=100, null=True, help_text="As Per the Record")
    ulbtype = models.ForeignKey(AgencyType, on_delete=models.CASCADE, null=True, verbose_name='ULB Type')
    administrative_district = models.ForeignKey(District, on_delete=models.CASCADE, null=True)
    regional_office_zone = models.CharField('Regional Office/Zone', max_length=100, null=True)
    office_phone_number = models.CharField('Office Phone Number', max_length=100, null=True)
    mail_id = models.EmailField('Email ID', max_length=100, null=True)
    alternative_mail = models.EmailField('Alternative Email ID', blank=True, max_length=100, null=True)
    officials = models.CharField('Officials', max_length=100, null=True)
    executive_commissionar_ph_no = models.CharField('Executive/Commissionar Phone No.', max_length=100, null=True)
    me_je = models.CharField('Master Engineer/Junior Engineer', max_length=100, null=True)

    def __str__(self):
        return self.ulbName

    class Meta:
        verbose_name = 'ULB Detail'
        verbose_name_plural = 'ULB Details'

class ULBProgressIncompleted(AgencyProgressModel):
    class Meta:
        proxy = True
        verbose_name = 'ULB Progress Incompleted'
        verbose_name_plural = 'ULB Progress Incompleted'


class ProjectProgressDetailsReport(AgencyProgressModel):
    class Meta:
        proxy = True
        verbose_name = 'Project Progress Details Report'
        verbose_name_plural = 'Project Progress Details Reports'

