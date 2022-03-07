from weakref import proxy
from django.contrib.auth.models import User
from django.db import models
from mapbox_location_field.models import LocationField
from django.utils.safestring import mark_safe

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
        return self.scheme


# Master Sanction Form
class Location(models.Model):
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
                   })


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
    Latitude = models.DecimalField("Latitude", blank=True, decimal_places=4, max_digits=10,null=True)
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


def scheme_make_choices():
    return [(str(c), str(c)) for c in Scheme.objects.all()]


def sector_make_choices():
    return [(str(c), str(c)) for c in MasterSanctionForm.objects.values_list('Sector', flat=True).distinct()]


def product_id_make_choices():
    return [(str(c), str(c)) for c in
            MasterSanctionForm.objects.values_list('Project_ID', flat=True).order_by('SNo').distinct()]


def status_choices():
    return [('In Progress', 'In Progress'),
            ('Completed', 'Completed')]


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
    status = models.CharField(max_length=20, choices=status_choices(), blank=True, null=True)
    Expenditure = models.CharField("Expenditure (in lakhs)", max_length=50, blank=True, null=True)
    FundRelease = models.CharField("Fund Release (in lakhs)", max_length=50, blank=True, null=True,
                                   help_text="Agency has to send a hard copy of the release request along with "
                                             "photos,etc in the prescribed format")
    valueofworkdone = models.CharField("Value of Work done (in lakhs)", max_length=50, blank=True, null=True)
    upload1 = models.FileField("upload", upload_to="agencysanctionlocation/", null=True,
                               help_text="Please upload a photo of site with location matching with the google maps",
                               blank=True)
    upload2 = models.FileField("upload", upload_to="agencysanction/", blank=True, null=True)

    def save(self, **kwargs):
        self.location = "%s, %s" % (self.Longitude, self.Latitude)
        self.Sector = MasterSanctionForm.objects.values_list('Sector', flat=True).filter(Project_ID=self.Project_ID)
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


class MasterReport(MasterSanctionForm):
    class Meta:
        proxy = True
        verbose_name = "KNMT Physical & Financial Progress Report"
        verbose_name_plural = "KNMT Physical & Financial Progress Reports"


class Dashboard(MasterSanctionForm):
    class Meta:
        proxy = True
        verbose_name = "Dashboard"
        verbose_name_plural = "Dashboard"


class SectorMasterReport(MasterSanctionForm):
    class Meta:
        proxy = True
        verbose_name = "Sector wise Report"
        verbose_name_plural = "Sector wise Reports"


class DistrictWiseReport(MasterSanctionForm):
    class Meta:
        proxy = True
        verbose_name = "DMA District Wise Report"
        verbose_name_plural = "DMA District Wise Reports"


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


class FundReleaseDetails(models.Model):
    date_of_release = models.DateField('Date of Release', null=True)
    amount = models.CharField('Amount', max_length=20, null=True)
    instruction_report_by_SQM = models.FileField(upload_to='SQMreport/', null=True)
    masterSanctionForm = models.ForeignKey(MasterSanctionForm, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Fund Release Detail"
        verbose_name_plural = "Fund Release Details"


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