import functools
from urllib import request
from django.contrib import admin
from django.contrib.admin import AdminSite
import json
from django.db.models import Count, Sum, Avg, Func
from import_export.admin import ImportExportModelAdmin
from mapbox_location_field.admin import MapAdmin
from .resources import *
from .forms import *
import pickle

admin.site.index_title = ""

# Register your models here.
admin.site.register(tufidco_info)


@admin.register(Officer)
class OfficerAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'Designation'
    ]

    ordering = [
        'id'
    ]


class PostImageAdmin(admin.StackedInline):
    model = postphotogallery_slider


class PostFormSlider(admin.StackedInline):
    model = postreformslider


class PostMainSlider(admin.StackedInline):
    model = postmainslider


class GalleryAdmin(admin.StackedInline):
    model = gallery_Images


@admin.register(body_images)
class BodyAdmin(admin.ModelAdmin):
    inlines = [
        PostImageAdmin,
        PostFormSlider,
        PostMainSlider
    ]

    class Meta:
        model = body_images


@admin.register(postphotogallery_slider)
class PostImageAdmin(admin.ModelAdmin):
    pass


@admin.register(postreformslider)
class PostFormSlider(admin.ModelAdmin):
    pass


@admin.register(postmainslider)
class PostMainSlider(admin.ModelAdmin):
    pass


@admin.register(gallery_Images)
class GalleryAdmin(admin.ModelAdmin):
    list_display = [
        'place',
        'Date'
    ]

    readonly_fields = (
        'image_preview',
    )

    ordering = [
        'id'
    ]

    def image_preview(self, obj):
        return obj.image_preview

    image_preview.short_description = 'Image Preview'
    image_preview.allow_tags = True


# Sanction Form
admin.site.register(Location, MapAdmin)

admin.site.register(About)


class SchemeAdmin(ImportExportModelAdmin, admin.AdminSite):
    model = Scheme

    list_display = [
        'Scheme'
    ]


admin.site.register(Scheme, SchemeAdmin)

admin.site.register(SchemeSanctionPdf)


class LocationAdmin(admin.StackedInline):
    model = Location


@admin.register(Scheme_Faq_Questions)
class SchemeFAQQuestion(admin.ModelAdmin):
    list_display = [
        'question',
        'name'
    ]

    ordering = [
        'question'
    ]


@admin.register(Scheme_Page)
class SchemePageAdmin(admin.ModelAdmin):
    pass


class AgencyTypeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    model = AgencyType

    list_display = [
        'AgencyType'
    ]

    ordering = [
        'id'
    ]


admin.site.register(AgencyType, AgencyTypeAdmin)


class AgencyNameAdmin(ImportExportModelAdmin):
    resource_class = AgencyNameResource

    list_display = [
        'AgencyName',
        'AgencyType'
    ]
    list_filter = ['AgencyType']
    ordering = [
        'AgencyName'
    ]

    search_fields = [
        'AgencyName'
    ]


admin.site.register(AgencyName, AgencyNameAdmin)


class DistrictAdmin(ImportExportModelAdmin):
    resource_class = DistrictResource

    list_display = [
        'District'
    ]

    ordering = [
        'District'
    ]

    search_fields = [
        'District'
    ]


admin.site.register(District, DistrictAdmin)


class RegionAdmin(ImportExportModelAdmin):
    resource_class = RegionResource

    list_display = [
        'Region'
    ]

    ordering = [
        'Region'
    ]

    search_fields = [
        'Region'
    ]


admin.site.register(Region, RegionAdmin)


class ReleaseDateInLine(admin.TabularInline):
    model = FundReleaseDetails
    extra = 1

    verbose_name = "Fund Release Detail"
    verbose_name_plural = "Fund Release Details"


class MasterSanctionFormAdmin(ImportExportModelAdmin, admin.AdminSite):
    change_form_template = 'admin/masterform.html'
    resource_class = MasterSanctionResource

    exclude = ['total']

    list_display = [
        'SNo',
        'AgencyName',
        'Sector',
        'ProjectName',
        'Project_ID',
        'Scheme',
        'ApprovedProjectCost',
        'SchemeShare',
        'ULBShare'
    ]

    list_filter = (
        'AgencyType',
        'Sector',
        'Scheme',
        'GoMeeting',
    )

    ordering = (
        'SNo',
    )

    search_fields = (
        'Project_ID',
        'Scheme__Scheme',
        'Sector',
        'GoMeeting',
        'ProjectName',
        'AgencyName__AgencyName',
        'District__District'
    )

    inlines = [ReleaseDateInLine]


admin.site.register(MasterSanctionForm, MasterSanctionFormAdmin)


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    change_list_template = 'admin/report.html'

    list_filter = (
        'AgencyType',
        'Scheme',
        'GoMeeting',
    )

    ordering = (
        'SNo',
    )

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        metrics = {
            'AgencyName': Count('AgencyName', distinct=True),
            'NoM': Count('SNo'),
            'ApprovedProjectCost': Sum('ApprovedProjectCost'),
            'SchemeShare': Sum('SchemeShare'),
            'ULBShare': Sum('ULBShare')
        }
        response.context_data['report_total'] = dict(
            qs.aggregate(**metrics)
        )

        response.context_data['report'] = list(qs.values('Sector').annotate(**metrics).order_by('Sector'))
        response.context_data['heading'] = list(
            qs.values('Scheme__Scheme', 'GoMeeting', 'Sector', 'AgencyType__AgencyType').order_by(
                'GoMeeting').distinct()
        )
        return response


@admin.register(SectorMasterReport)
class SectorReportAdmin(admin.ModelAdmin):
    change_list_template = 'admin/SectorMasterReport.html'

    list_filter = (
        'AgencyType',
        'Scheme',
        'Sector',
        'GoMeeting',
    )

    ordering = (
        'SNo',
    )

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        metrics = {
            'ProjectCost': Sum('ProjectCost'),
            'ProposedULBCost': Sum('ProposedCostByULB'),
            'ApprovedCost': Sum('ApprovedProjectCost'),
            'SchemeShare': Sum('SchemeShare'),
            'ULBShare': Sum('ULBShare')
        }

        response.context_data['report_total'] = dict(
            qs.aggregate(**metrics)
        )

        response.context_data['report'] = list(
            qs.values('District__District', 'AgencyName__AgencyName', 'ProjectName', 'Project_ID',
                      'ApprovedProjectCost', 'Sector', 'SchemeShare', 'ULBShare', 'Project_ID').order_by('GoMeeting',
                                                                                                         'Sector',
                                                                                                         'Project_ID'))
        response.context_data['heading'] = list(
            qs.values('Scheme__Scheme', 'Sector', 'AgencyType__AgencyType').order_by('Scheme__Scheme').distinct()
        )

        return response


"""
    Agency admin
"""


class AgencyBankDetailsAdmin(admin.ModelAdmin):
    change_form_template = 'admin/bankagencydetails.html'

    exclude = ['user']
    readonly_fields = ['passbook_preview']
    list_display = [
        'user',
        'beneficiary_name',
        'bank_name',
        'branch',
        'account_number',
        'IFSC_code'
    ]
    ordering = [
        'user__first_name',
    ]
    search_fields = [
        'user__first_name',
        'beneficiary_name',
        'bank_name',
        'branch',
        'account_number',
        'IFSC_code'
    ]

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context.update({
            'show_save': True,
            'show_save_and_add_another': False,
        })
        return super().render_change_form(request, context, add, change, form_url, obj)

    def get_queryset(self, request):
        qs = super(AgencyBankDetailsAdmin, self).get_queryset(request)
        if not request.user.groups.filter(name__in=["Admin", ]).exists():
            return qs.filter(user=request.user)
        return qs

    def has_add_permission(self, request, *args, **kwargs):
        return not AgencyBankDetails.objects.filter(user=request.user).exists() and not request.user.groups.filter(
            name__in=[
                "Admin", "CMD_DGM"]).exists()

    def passbook_preview(self, obj):
        return obj.passbook_preview

    passbook_preview.short_description = 'Passbook Front Page'
    passbook_preview.allow_tags = True


admin.site.register(AgencyBankDetails, AgencyBankDetailsAdmin)


@admin.register(AgencyProgressModel)
class AgencyProgressAdmin(admin.ModelAdmin):
    form = AgencyProgressForm
    fields = (('Scheme', 'Sector', 'Project_ID'), 'ProjectName', ('Latitude', 'Longitude'), 'location',
              'PhysicalProgress', 'status', 'upload1', 'Expenditure', 'FundRelease', 'valueofworkdone', 'upload2')

    list_filter = [
        'status',
        'Scheme',
        'Sector',
        'valueofworkdone',
        'percentageofworkdone'
    ]
    list_display = [
        'Project_ID',
        'Sector',
        'ProjectName',
        'user',
        'valueofworkdone',
        'status',
        'percentageofworkdone'
    ]

    search_fields = [
        'Scheme',
        'user__first_name',
        'ProjectName',
        'Project_ID',
        'Sector',
    ]

    ordering = [
        'Project_ID',
        'Sector',
        'user'
    ]

    def save_model(self, request, obj, form, change):
        if request.user.groups.filter(name__in=['Agency']).exists():
            obj.user = request.user
            obj.ProjectName = MasterSanctionForm.objects.values_list('ProjectName', flat=True).filter(
                Project_ID=form.cleaned_data['Project_ID'])
            obj.save()

    def get_queryset(self, request):
        qs = super(AgencyProgressAdmin, self).get_queryset(request)
        if not request.user.groups.filter(name__in=["Admin", ]).exists():
            return qs.filter(user=request.user)
        return qs

    def get_form(self, request, obj=None, **kwargs):
        Form = super().get_form(request, obj=None, **kwargs)
        return functools.partial(Form, request)


@admin.register(AgencySanctionModel)
class AgencySanctionAdmin(admin.ModelAdmin):
    form = AgencySanctionForm
    search_fields = [
        'Scheme',
        'user',
        'Project_ID',
        'ProjectName',
        'user__first_name',
        'Sector',
        'tsrefno'
    ]
    fields = (
        ('Scheme', 'Sector', 'Project_ID'), 'ProjectName', 'ts_awarded', 'tsrefno', 'tsdate', 'tr_awarded', 'tawddate',
        'wd_awarded', 'wdawddate')
    list_display = [
        'Project_ID',
        'Sector',
        'ProjectName',
        'user',
    ]
    ordering = [
        'Project_ID',
        'Sector',
        'user'
    ]
    list_filter = [
        'Scheme',
        'Sector',
        'ts_awarded',
        'tr_awarded',
        'wd_awarded',
    ]

    def save_model(self, request, obj, form, change):
        if request.user.groups.filter(name__in=['Agency']).exists():
            obj.user = request.user
            obj.ProjectName = MasterSanctionForm.objects.values_list('ProjectName', flat=True).filter(
                Project_ID=form.cleaned_data['Project_ID'])
            obj.save()

    def get_queryset(self, request):
        qs = super(AgencySanctionAdmin, self).get_queryset(request)
        if not request.user.groups.filter(name__in=["Admin", ]).exists():
            return qs.filter(user=request.user)
        return qs

    def get_form(self, request, obj=None, **kwargs):
        formset = super().get_form(request, obj, **kwargs)
        return functools.partial(formset, request)


class ULBPANDetailsAdmin(admin.ModelAdmin):
    change_form_template = 'admin/ULBpandetails.html'
    exclude = ['user']
    readonly_fields = ['pan_preview']
    list_display = [
        'user',
        'PANno',
        'name'
    ]
    search_fields = [
        'user__first_name',
        'PANno',
        'name',
    ]
    ordering = [
        'user__first_name',
    ]

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context.update({
            'show_save': True,
            'show_save_and_add_another': False,
        })
        return super().render_change_form(request, context, add, change, form_url, obj)

    def has_add_permission(self, request, *args, **kwargs):
        return not ULBPanCard.objects.filter(user=request.user).exists() and not request.user.groups.filter(name__in=[
            "Admin", "CMD_DGM"]).exists()

    def get_queryset(self, request):
        qs = super(ULBPANDetailsAdmin, self).get_queryset(request)
        if not request.user.groups.filter(name__in=["Admin", ]).exists():
            return qs.filter(user=request.user)
        return qs

    def pan_preview(self, obj):
        return obj.pan_preview

    pan_preview.short_description = 'Passbook Front Page'
    pan_preview.allow_tags = True


admin.site.register(ULBPanCard, ULBPANDetailsAdmin)


class FundReleaseDetailsAdmin(admin.StackedInline):
    model = FundReleaseDetails
    extra = 5


@admin.register(MasterReport)
class MasterReportAdmin(admin.ModelAdmin):
    change_list_template = 'admin/masterreport.html'

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response
        ''' 
            metrics = {
            'ApprovedProjectCost': Sum('ApprovedProjectCost'),
            'SchemeShare': Sum('SchemeShare'),
            'ULBShare': Sum('ULBShare'),
            'total': Sum('total')
        }
        response.context_data['report_total'] = dict(
            qs.aggregate(**metrics)
        )

        response.context_data['report'] = list(qs.values('Sector').annotate(**metrics).order_by('Sector'))
        '''
        BT_Road_SchemeShare = MasterSanctionForm.objects.filter(Scheme__Scheme="KNMT").filter(
            Sector="BT Road").aggregate(BT_Road_SchemeShare=Sum('SchemeShare'))
        BT_Road_ULBShare = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector='BT Road').aggregate(
            BT_Road_ULBShare=Sum('ULBShare'))
        BT_Road_Total = BT_Road_SchemeShare['BT_Road_SchemeShare'] + BT_Road_ULBShare['BT_Road_ULBShare']
        BT_Road_Approved = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector='BT Road').count()
        BT_Road_Completed = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector='BT Road').filter(
            status='Completed').count()
        BT_Road_inprogress = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector='BT Road').filter(
            status='In Progress').count()
        BT_Road_Taken = BT_Road_inprogress + BT_Road_Completed
        Bus_Stand_SchemeShare = MasterSanctionForm.objects.filter(Scheme__Scheme="KNMT").filter(
            Sector="Bus Stand").aggregate(Bus_Stand_SchemeShare=Sum('SchemeShare'))
        Bus_Stand_ULBShare = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector='Bus Stand').aggregate(Bus_Stand_ULBShare=Sum('ULBShare'))
        Bus_Stand_Total = Bus_Stand_SchemeShare['Bus_Stand_SchemeShare'] + Bus_Stand_ULBShare['Bus_Stand_ULBShare']
        Bus_Stand_Approved = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector='Bus Stand').count()
        Bus_Stand_Completed = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector='Bus Stand').filter(
            status='Completed').count()
        Bus_Stand_inprogress = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector='Bus Stand').filter(
            status='In Progress').count()
        Bus_Stand_Taken = Bus_Stand_inprogress + Bus_Stand_Completed
        CC_Road_SchemeShare = MasterSanctionForm.objects.filter(Scheme__Scheme="KNMT").filter(
            Sector="CC Road").aggregate(CC_Road_SchemeShare=Sum('SchemeShare'))
        CC_Road_ULBShare = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector='CC Road').aggregate(
            CC_Road_ULBShare=Sum('ULBShare'))
        CC_Road_Total = CC_Road_SchemeShare['CC_Road_SchemeShare'] + CC_Road_ULBShare['CC_Road_ULBShare']
        CC_Road_Approved = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector='CC Road').count()
        CC_Road_Completed = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector='CC Road').filter(
            status='Completed').count()
        CC_Road_inprogress = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector='CC Road').filter(
            status='In Progress').count()
        CC_Road_Taken = CC_Road_inprogress + CC_Road_Completed
        # Community Hall
        Community_Hall_SchemeShare = MasterSanctionForm.objects.filter(Scheme__Scheme="KNMT").filter(
            Sector="Community Hall").aggregate(Community_Hall_SchemeShare=Sum('SchemeShare'))
        Community_Hall_ULBShare = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector='Community Hall').aggregate(Community_Hall_ULBShare=Sum('ULBShare'))
        Community_Hall_Total = Community_Hall_SchemeShare['Community_Hall_SchemeShare'] + Community_Hall_ULBShare[
            'Community_Hall_ULBShare']
        Community_Hall_Approved = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector='Community Hall').count()
        Community_Hall_Completed = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            Sector='Community Hall').filter(status='Completed').count()
        Community_Hall_inprogress = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            Sector='Community Hall').filter(status='In Progress').count()
        Community_Hall_Taken = Community_Hall_inprogress + Community_Hall_Completed
        # Crematorium
        Crematorium_SchemeShare = MasterSanctionForm.objects.filter(Scheme__Scheme="KNMT").filter(
            Sector="Crematorium").aggregate(Crematorium_SchemeShare=Sum('SchemeShare'))
        Crematorium_ULBShare = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector='Crematorium').aggregate(Crematorium_ULBShare=Sum('ULBShare'))
        Crematorium_Total = Crematorium_SchemeShare['Crematorium_SchemeShare'] + Crematorium_ULBShare[
            'Crematorium_ULBShare']
        Crematorium_Approved = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector='Crematorium').count()
        Crematorium_Completed = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector='Crematorium').filter(
            status='Completed').count()
        Crematorium_inprogress = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector='Crematorium').filter(
            status='In Progress').count()
        Crematorium_Taken = Crematorium_inprogress + Crematorium_Completed
        #	Culvert
        Culvert_SchemeShare = MasterSanctionForm.objects.filter(Scheme__Scheme="KNMT").filter(
            Sector="Culvert").aggregate(Culvert_SchemeShare=Sum('SchemeShare'))
        Culvert_ULBShare = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector='Culvert').aggregate(
            Culvert_ULBShare=Sum('ULBShare'))
        Culvert_Total = Culvert_SchemeShare['Culvert_SchemeShare'] + Culvert_ULBShare['Culvert_ULBShare']
        Culvert_Approved = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector='Culvert').count()
        Culvert_Completed = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector='Culvert').filter(
            status='Completed').count()
        Culvert_inprogress = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector='Culvert').filter(
            status='In Progress').count()
        Culvert_Taken = Culvert_inprogress + Culvert_Completed
        # Knowledge Centre
        Knowledge_Centre_SchemeShare = MasterSanctionForm.objects.filter(Scheme__Scheme="KNMT").filter(
            Sector="Knowledge Centre").aggregate(Knowledge_Centre_SchemeShare=Sum('SchemeShare'))
        Knowledge_Centre_ULBShare = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector='Knowledge Centre').aggregate(Knowledge_Centre_ULBShare=Sum('ULBShare'))
        Knowledge_Centre_Total = Knowledge_Centre_SchemeShare['Knowledge_Centre_SchemeShare'] + \
                                 Knowledge_Centre_ULBShare['Knowledge_Centre_ULBShare']
        Knowledge_Centre_Approved = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector='Knowledge Centre').count()
        Knowledge_Centre_Completed = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            Sector='Knowledge Centre').filter(status='Completed').count()
        Knowledge_Centre_inprogress = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            Sector='Knowledge Centre').filter(status='In Progress').count()
        Knowledge_Centre_Taken = Knowledge_Centre_inprogress + Knowledge_Centre_Completed
        # Market
        Market_SchemeShare = MasterSanctionForm.objects.filter(Scheme__Scheme="KNMT").filter(Sector="Market").aggregate(
            Market_SchemeShare=Sum('SchemeShare'))
        Market_ULBShare = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector='Market').aggregate(
            Market_ULBShare=Sum('ULBShare'))
        Market_Total = Market_SchemeShare['Market_SchemeShare'] + Market_ULBShare['Market_ULBShare']
        Market_Approved = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector='Market').count()
        Market_Completed = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector='Market').filter(
            status='Completed').count()
        Market_inprogress = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector='Market').filter(
            status='In Progress').count()
        Market_Taken = Market_inprogress + Market_Completed
        # Metal Beam Crash Barriers
        M_B_C_B_SchemeShare = MasterSanctionForm.objects.filter(Scheme__Scheme="KNMT").filter(
            Sector="Metal Beam Crash Barriers").aggregate(M_B_C_B_SchemeShare=Sum('SchemeShare'))
        M_B_C_B_ULBShare = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector='Metal Beam Crash Barriers').aggregate(M_B_C_B_ULBShare=Sum('ULBShare'))
        M_B_C_B_Total = M_B_C_B_SchemeShare['M_B_C_B_SchemeShare'] + M_B_C_B_ULBShare['M_B_C_B_ULBShare']
        M_B_C_B_Approved = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector='Metal Beam Crash Barriers').count()
        M_B_C_B_Completed = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            Sector='Metal Beam Crash Barriers').filter(status='Completed').count()
        M_B_C_B_inprogress = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            Sector='Metal Beam Crash Barriers').filter(status='In Progress').count()
        M_B_C_B_Taken = M_B_C_B_inprogress + M_B_C_B_Completed

        # Parks
        Parks_SchemeShare = MasterSanctionForm.objects.filter(Scheme__Scheme="KNMT").filter(Sector="Parks").aggregate(
            Parks_SchemeShare=Sum('SchemeShare'))
        Parks_ULBShare = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector='Parks').aggregate(
            Parks_ULBShare=Sum('ULBShare'))
        Parks_Total = Parks_SchemeShare['Parks_SchemeShare'] + Parks_ULBShare['Parks_ULBShare']
        Parks_Approved = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector='Parks').count()
        Parks_Completed = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector='Parks').filter(
            status='Completed').count()
        Parks_inprogress = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector='Parks').filter(
            status='In Progress').count()
        Parks_Taken = Parks_inprogress + Parks_Completed

        # Paver Block
        Paver_Block_SchemeShare = MasterSanctionForm.objects.filter(Scheme__Scheme="KNMT").filter(
            Sector="Paver Block").aggregate(Paver_Block_SchemeShare=Sum('SchemeShare'))
        Paver_Block_ULBShare = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector='Paver Block').aggregate(Paver_Block_ULBShare=Sum('ULBShare'))
        Paver_Block_Total = Paver_Block_SchemeShare['Paver_Block_SchemeShare'] + Paver_Block_ULBShare[
            'Paver_Block_ULBShare']
        Paver_Block_Approved = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector='Paver Block').count()
        Paver_Block_Completed = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector='Paver Block').filter(
            status='Completed').count()
        Paver_Block_inprogress = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector='Paver Block').filter(
            status='In Progress').count()
        Paver_Block_Taken = Paver_Block_inprogress + Paver_Block_Completed

        # Retaining wall
        Retaining_wall_SchemeShare = MasterSanctionForm.objects.filter(Scheme__Scheme="KNMT").filter(
            Sector="Retaining wall").aggregate(Retaining_wall_SchemeShare=Sum('SchemeShare'))
        Retaining_wall_ULBShare = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector='Retaining wall').aggregate(Retaining_wall_ULBShare=Sum('ULBShare'))
        Retaining_wall_Total = Retaining_wall_SchemeShare['Retaining_wall_SchemeShare'] + Retaining_wall_ULBShare[
            'Retaining_wall_ULBShare']
        Retaining_wall_Approved = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector='Retaining wall').count()
        Retaining_wall_Completed = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            Sector='Retaining wall').filter(status='Completed').count()
        Retaining_wall_inprogress = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            Sector='Retaining wall').filter(status='In Progress').count()
        Retaining_wall_Taken = Retaining_wall_inprogress + Retaining_wall_Completed
        # Solid Waste Mgt. SWM
        SWM_SchemeShare = MasterSanctionForm.objects.filter(Scheme__Scheme="KNMT").filter(
            Sector="Solid Waste Mgt.").aggregate(SWM_SchemeShare=Sum('SchemeShare'))
        SWM_ULBShare = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector='Solid Waste Mgt.').aggregate(SWM_ULBShare=Sum('ULBShare'))
        SWM_Total = SWM_SchemeShare['SWM_SchemeShare'] + SWM_ULBShare['SWM_ULBShare']
        SWM_Approved = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector='Solid Waste Mgt.').count()
        SWM_Completed = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector='Solid Waste Mgt.').filter(
            status='Completed').count()
        SWM_inprogress = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector='Solid Waste Mgt.').filter(
            status='In Progress').count()
        SWM_Taken = SWM_inprogress + SWM_Completed
        # SWD
        SWD_SchemeShare = MasterSanctionForm.objects.filter(Scheme__Scheme="KNMT").filter(Sector="SWD").aggregate(
            SWD_SchemeShare=Sum('SchemeShare'))
        SWD_ULBShare = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector='SWD').aggregate(
            SWD_ULBShare=Sum('ULBShare'))
        SWD_Total = SWD_SchemeShare['SWD_SchemeShare'] + SWD_ULBShare['SWD_ULBShare']
        SWD_Approved = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector='SWD').count()
        SWD_Completed = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector='SWD').filter(
            status='Completed').count()
        SWD_inprogress = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector='SWD').filter(
            status='In Progress').count()
        SWD_Taken = SWD_inprogress + SWD_Completed

        # Water Bodies
        Water_Bodies_SchemeShare = MasterSanctionForm.objects.filter(Scheme__Scheme="KNMT").filter(
            Sector="Water Bodies").aggregate(Water_Bodies_SchemeShare=Sum('SchemeShare'))
        Water_Bodies_ULBShare = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector='Water Bodies').aggregate(Water_Bodies_ULBShare=Sum('ULBShare'))
        Water_Bodies_Total = Water_Bodies_SchemeShare['Water_Bodies_SchemeShare'] + Water_Bodies_ULBShare[
            'Water_Bodies_ULBShare']
        Water_Bodies_Approved = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector='Water Bodies').count()
        Water_Bodies_Completed = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector='Water Bodies').filter(
            status='Completed').count()
        Water_Bodies_inprogress = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            Sector='Water Bodies').filter(status='In Progress').count()
        Water_Bodies_Taken = Water_Bodies_inprogress + Water_Bodies_Completed

        SchemeShare = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').aggregate(SchemeShare=Sum('SchemeShare'))
        ULBShare = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').aggregate(ULBShare=Sum('ULBShare'))
        ProjectCost = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').aggregate(
            ProjectCost=Sum('ApprovedProjectCost'))
        work_approved_total = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').count()

        works_inprogress_total = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(status='In Progress').count()
        works_completed_total = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(status='Completed').count()
        works_taken_total = works_inprogress_total + works_completed_total

        extra_context = {
            'works_taken_total': works_taken_total,
            'works_inprogress_total': works_inprogress_total,
            'works_completed_total': works_completed_total,
            'work_approved_total': work_approved_total,
            'ProjectCost': ProjectCost,
            'ULBShare': ULBShare,
            'SchemeShare': SchemeShare,
            'BT_Road_SchemeShare': BT_Road_SchemeShare,
            'BT_Road_ULBShare': BT_Road_ULBShare,
            'BT_Road_Total': BT_Road_Total,
            'BT_Road_inprogress': BT_Road_inprogress,
            'BT_Road_Completed': BT_Road_Completed,
            'BT_Road_Approved': BT_Road_Approved,
            'BT_Road_Taken': BT_Road_Taken,
            'Bus_Stand_SchemeShare': Bus_Stand_SchemeShare,
            'Bus_Stand_ULBShare': Bus_Stand_ULBShare,
            'Bus_Stand_Total': Bus_Stand_Total,
            'Bus_Stand_inprogress': Bus_Stand_inprogress,
            'Bus_Stand_Completed': Bus_Stand_Completed,
            'Bus_Stand_Approved': Bus_Stand_Approved,
            'Bus_Stand_Taken': Bus_Stand_Taken,
            'CC_Road_SchemeShare': CC_Road_SchemeShare,
            'CC_Road_ULBShare': CC_Road_ULBShare,
            'CC_Road_Total': CC_Road_Total,
            'CC_Road_inprogress': CC_Road_inprogress,
            'CC_Road_Completed': CC_Road_Completed,
            'CC_Road_Approved': CC_Road_Approved,
            'CC_Road_Taken': CC_Road_Taken,
            'Community_Hall_SchemeShare': Community_Hall_SchemeShare,
            'Community_Hall_ULBShare': Community_Hall_ULBShare,
            'Community_Hall_Total': Community_Hall_Total,
            'Community_Hall_inprogress': Community_Hall_inprogress,
            'Community_Hall_Completed': Community_Hall_Completed,
            'Community_Hall_Approved': Community_Hall_Approved,
            'Community_Hall_Taken': Community_Hall_Taken,

            'Crematorium_SchemeShare': Crematorium_SchemeShare,
            'Crematorium_ULBShare': Crematorium_ULBShare,
            'Crematorium_Total': Crematorium_Total,
            'Crematorium_inprogress': Crematorium_inprogress,
            'Crematorium_Completed': Crematorium_Completed,
            'Crematorium_Approved': Crematorium_Approved,
            'Crematorium_Taken': Crematorium_Taken,

            'Culvert_SchemeShare': Culvert_SchemeShare,
            'Culvert_ULBShare': Culvert_ULBShare,
            'Culvert_Total': Culvert_Total,
            'Culvert_inprogress': Culvert_inprogress,
            'Culvert_Completed': Culvert_Completed,
            'Culvert_Approved': Culvert_Approved,
            'Culvert_Taken': Culvert_Taken,

            'Knowledge_Centre_SchemeShare': Knowledge_Centre_SchemeShare,
            'Knowledge_Centre_ULBShare': Knowledge_Centre_ULBShare,
            'Knowledge_Centre_Total': Knowledge_Centre_Total,
            'Knowledge_Centre_inprogress': Knowledge_Centre_inprogress,
            'Knowledge_Centre_Completed': Knowledge_Centre_Completed,
            'Knowledge_Centre_Approved': Knowledge_Centre_Approved,
            'Knowledge_Centre_Taken': Knowledge_Centre_Taken,

            'Market_SchemeShare': Market_SchemeShare,
            'Market_ULBShare': Market_ULBShare,
            'Market_Total': Market_Total,
            'Market_inprogress': Market_inprogress,
            'Market_Completed': Market_Completed,
            'Market_Approved': Market_Approved,
            'Market_Taken': Market_Taken,

            'M_B_C_B_SchemeShare': M_B_C_B_SchemeShare,
            'M_B_C_B_ULBShare': M_B_C_B_ULBShare,
            'M_B_C_B_Total': M_B_C_B_Total,
            'M_B_C_B_inprogress': M_B_C_B_inprogress,
            'M_B_C_B_Completed': M_B_C_B_Completed,
            'M_B_C_B_Approved': M_B_C_B_Approved,
            'M_B_C_B_Taken': M_B_C_B_Taken,

            'Parks_SchemeShare': Parks_SchemeShare,
            'Parks_ULBShare': Parks_ULBShare,
            'Parks_Total': Parks_Total,
            'Parks_inprogress': Parks_inprogress,
            'Parks_Completed': Parks_Completed,
            'Parks_Approved': Parks_Approved,
            'Parks_Taken': Parks_Taken,

            'Paver_Block_SchemeShare': Paver_Block_SchemeShare,
            'Paver_Block_ULBShare': Paver_Block_ULBShare,
            'Paver_Block_Total': Paver_Block_Total,
            'Paver_Block_inprogress': Paver_Block_inprogress,
            'Paver_Block_Completed': Paver_Block_Completed,
            'Paver_Block_Approved': Paver_Block_Approved,
            'Paver_Block_Taken': Paver_Block_Taken,

            'Retaining_wall_SchemeShare': Retaining_wall_SchemeShare,
            'Retaining_wall_ULBShare': Retaining_wall_ULBShare,
            'Retaining_wall_Total': Retaining_wall_Total,
            'Retaining_wall_inprogress': Retaining_wall_inprogress,
            'Retaining_wall_Completed': Retaining_wall_Completed,
            'Retaining_wall_Approved': Retaining_wall_Approved,
            'Retaining_wall_Taken': Retaining_wall_Taken,

            'SWM_SchemeShare': SWM_SchemeShare,
            'SWM_ULBShare': SWM_ULBShare,
            'SWM_Total': SWM_Total,
            'SWM_inprogress': SWM_inprogress,
            'SWM_Completed': SWM_Completed,
            'SWM_Approved': SWM_Approved,
            'SWM_Taken': SWM_Taken,

            'SWD_SchemeShare': SWD_SchemeShare,
            'SWD_ULBShare': SWD_ULBShare,
            'SWD_Total': SWD_Total,
            'SWD_inprogress': SWD_inprogress,
            'SWD_Completed': SWD_Completed,
            'SWD_Approved': SWD_Approved,
            'SWD_Taken': SWD_Taken,

            'Water_Bodies_SchemeShare': Water_Bodies_SchemeShare,
            'Water_Bodies_ULBShare': Water_Bodies_ULBShare,
            'Water_Bodies_Total': Water_Bodies_Total,
            'Water_Bodies_inprogress': Water_Bodies_inprogress,
            'Water_Bodies_Completed': Water_Bodies_Completed,
            'Water_Bodies_Approved': Water_Bodies_Approved,
            'Water_Bodies_Taken': Water_Bodies_Taken,

        }
        response.context_data.update(extra_context)
        return response


@admin.register(LatestReports)
class LatestReportAdmin(admin.ModelAdmin):
    pass


@admin.register(CTPDistrictWiseReport)
class CTPDistrictWiseReportAdmin(admin.ModelAdmin):
    change_list_template = "admin/CTPDistrictWiseReport.html"

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response
        extra_context = {

        }
        metrics = {
            'Project_ID': Count('Project_ID'),
            'ApprovedCost': Sum('ApprovedProjectCost'),
        }

        response.context_data['report_total'] = dict(
            qs.aggregate(**metrics)
        )

        ariyalur_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Ariyalur'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        ariyalur_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Ariyalur'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        ariyalur_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Ariyalur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        ariyalur_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Ariyalur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        ariyalur_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Ariyalur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        ariyalur_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Ariyalur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        ariyalur_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Ariyalur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        ariyalur_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Ariyalur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        ariyalur_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Ariyalur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        ariyalur_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Ariyalur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        ariyalur_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Ariyalur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        ariyalur_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Ariyalur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        ariyalur_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Ariyalur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        ariyalur_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Ariyalur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        ariyalur_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Ariyalur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        ariyalur_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Ariyalur').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        ariyalur_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Ariyalur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        ariyalur_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Ariyalur').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        ariyalur_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Ariyalur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        ariyalur_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Ariyalur').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        ariyalur_total_no = MasterSanctionForm.objects.filter(District__District='Ariyalur').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        ariyalur_total_cost = MasterSanctionForm.objects.filter(District__District='Ariyalur').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Chengalpattu_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Chengalpattu'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Chengalpattu_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Chengalpattu'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Chengalpattu_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Chengalpattu'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Chengalpattu_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Chengalpattu'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Chengalpattu_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Chengalpattu'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Chengalpattu_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Chengalpattu'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Chengalpattu_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Chengalpattu'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Chengalpattu_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Chengalpattu'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Chengalpattu_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Chengalpattu'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Chengalpattu_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Chengalpattu'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Chengalpattu_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Chengalpattu'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Chengalpattu_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Chengalpattu'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Chengalpattu_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Chengalpattu'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Chengalpattu_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Chengalpattu'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Chengalpattu_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Chengalpattu'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Chengalpattu_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Chengalpattu').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Chengalpattu_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Chengalpattu'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Chengalpattu_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Chengalpattu').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Chengalpattu_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Chengalpattu'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Chengalpattu_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Chengalpattu').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Chengalpattu_total_no = MasterSanctionForm.objects.filter(District__District='Chengalpattu').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Chengalpattu_total_cost = MasterSanctionForm.objects.filter(District__District='Chengalpattu').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Coimbatore_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Coimbatore'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Coimbatore_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Coimbatore'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Coimbatore_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Coimbatore'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Coimbatore_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Coimbatore'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Coimbatore_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Coimbatore'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Coimbatore_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Coimbatore'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Coimbatore_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Coimbatore'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Coimbatore_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Coimbatore'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Coimbatore_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Coimbatore'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Coimbatore_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Coimbatore'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Coimbatore_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Coimbatore'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Coimbatore_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Coimbatore'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Coimbatore_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Coimbatore'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Coimbatore_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Coimbatore'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Coimbatore_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Coimbatore'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Coimbatore_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Coimbatore').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Coimbatore_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Coimbatore'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Coimbatore_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Coimbatore').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Coimbatore_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Coimbatore'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Coimbatore_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Coimbatore').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Coimbatore_total_no = MasterSanctionForm.objects.filter(District__District='Coimbatore').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Coimbatore_total_cost = MasterSanctionForm.objects.filter(District__District='Coimbatore').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Cuddalore_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Cuddalore'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Cuddalore_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Cuddalore'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Cuddalore_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Cuddalore'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Cuddalore_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Cuddalore'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Cuddalore_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Cuddalore'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Cuddalore_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Cuddalore'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Cuddalore_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Cuddalore'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Cuddalore_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Cuddalore'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Cuddalore_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Cuddalore'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Cuddalore_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Cuddalore'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Cuddalore_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Cuddalore'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Cuddalore_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Cuddalore'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Cuddalore_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Cuddalore'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Cuddalore_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Cuddalore'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Cuddalore_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Cuddalore'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Cuddalore_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Cuddalore').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Cuddalore_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Cuddalore'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Cuddalore_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Cuddalore').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Cuddalore_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Cuddalore'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Cuddalore_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Cuddalore').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Cuddalore_total_no = MasterSanctionForm.objects.filter(District__District='Cuddalore').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Cuddalore_total_cost = MasterSanctionForm.objects.filter(District__District='Cuddalore').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Dharmapuri_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Dharmapuri'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Dharmapuri_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Dharmapuri'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Dharmapuri_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Dharmapuri'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Dharmapuri_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Dharmapuri'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Dharmapuri_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Dharmapuri'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Dharmapuri_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Dharmapuri'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Dharmapuri_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Dharmapuri'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Dharmapuri_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Dharmapuri'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Dharmapuri_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Dharmapuri'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Dharmapuri_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Dharmapuri'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Dharmapuri_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Dharmapuri'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Dharmapuri_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Dharmapuri'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Dharmapuri_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Dharmapuri'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Dharmapuri_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Dharmapuri'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Dharmapuri_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Dharmapuri'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Dharmapuri_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Dharmapuri').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Dharmapuri_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Dharmapuri'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Dharmapuri_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Dharmapuri').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Dharmapuri_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Dharmapuri'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Dharmapuri_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Dharmapuri').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Dharmapuri_total_no = MasterSanctionForm.objects.filter(District__District='Dharmapuri').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Dharmapuri_total_cost = MasterSanctionForm.objects.filter(District__District='Dharmapuri').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Dindigul_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Dindigul'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Dindigul_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Dindigul'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Dindigul_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Dindigul'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Dindigul_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Dindigul'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Dindigul_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Dindigul'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Dindigul_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Dindigul'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Dindigul_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Dindigul'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Dindigul_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Dindigul'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Dindigul_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Dindigul'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Dindigul_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Dindigul'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Dindigul_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Dindigul'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Dindigul_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Dindigul'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Dindigul_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Dindigul'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Dindigul_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Dindigul'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Dindigul_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Dindigul'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Dindigul_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Dindigul').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Dindigul_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Dindigul'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Dindigul_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Dindigul').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Dindigul_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Dindigul'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Dindigul_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Dindigul').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Dindigul_total_no = MasterSanctionForm.objects.filter(District__District='Dindigul').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Dindigul_total_cost = MasterSanctionForm.objects.filter(District__District='Dindigul').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Erode_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Erode'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Erode_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Erode'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Erode_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Erode'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Erode_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Erode'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Erode_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Erode'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Erode_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Erode'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Erode_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Erode'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Erode_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Erode'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Erode_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Erode'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Erode_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Erode'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Erode_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Erode'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Erode_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Erode'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Erode_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Erode'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Erode_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Erode'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Erode_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Erode'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Erode_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Erode').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Erode_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Erode'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Erode_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Erode').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Erode_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Erode'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Erode_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Erode').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Erode_total_no = MasterSanctionForm.objects.filter(District__District='Erode').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Erode_total_cost = MasterSanctionForm.objects.filter(District__District='Erode').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Kallakurichi_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Kallakurichi'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Kallakurichi_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Kallakurichi'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Kallakurichi_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Kallakurichi'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Kallakurichi_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Kallakurichi'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Kallakurichi_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Kallakurichi'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Kallakurichi_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Kallakurichi'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Kallakurichi_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Kallakurichi'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Kallakurichi_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Kallakurichi'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Kallakurichi_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Kallakurichi'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Kallakurichi_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Kallakurichi'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Kallakurichi_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Kallakurichi'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Kallakurichi_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Kallakurichi'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Kallakurichi_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Kallakurichi'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Kallakurichi_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Kallakurichi'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Kallakurichi_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Kallakurichi'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Kallakurichi_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Kallakurichi').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Kallakurichi_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Kallakurichi'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Kallakurichi_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Kallakurichi').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Kallakurichi_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Kallakurichi'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Kallakurichi_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Kallakurichi').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Kallakurichi_total_no = MasterSanctionForm.objects.filter(District__District='Kallakurichi').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Kallakurichi_total_cost = MasterSanctionForm.objects.filter(District__District='Kallakurichi').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Kancheepuram_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Kancheepuram'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Kancheepuram_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Kancheepuram'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Kancheepuram_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Kancheepuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Kancheepuram_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Kancheepuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Kancheepuram_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Kancheepuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Kancheepuram_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Kancheepuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Kancheepuram_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Kancheepuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Kancheepuram_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Kancheepuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Kancheepuram_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Kancheepuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Kancheepuram_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Kancheepuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Kancheepuram_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Kancheepuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Kancheepuram_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Kancheepuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Kancheepuram_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Kancheepuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Kancheepuram_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Kancheepuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Kancheepuram_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Kancheepuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Kancheepuram_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Kancheepuram').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Kancheepuram_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Kancheepuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Kancheepuram_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Kancheepuram').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Kancheepuram_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Kancheepuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Kancheepuram_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Kancheepuram').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Kancheepuram_total_no = MasterSanctionForm.objects.filter(District__District='Kancheepuram').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Kancheepuram_total_cost = MasterSanctionForm.objects.filter(District__District='Kancheepuram').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Kanyakumari_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Kanyakumari'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Kanyakumari_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Kanyakumari'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Kanyakumari_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Kanyakumari'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Kanyakumari_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Kanyakumari'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Kanyakumari_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Kanyakumari'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Kanyakumari_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Kanyakumari'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Kanyakumari_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Kanyakumari'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Kanyakumari_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Kanyakumari'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Kanyakumari_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Kanyakumari'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Kanyakumari_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Kanyakumari'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Kanyakumari_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Kanyakumari'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Kanyakumari_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Kanyakumari'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Kanyakumari_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Kanyakumari'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Kanyakumari_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Kanyakumari'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Kanyakumari_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Kanyakumari'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Kanyakumari_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Kanyakumari').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Kanyakumari_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Kanyakumari'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Kanyakumari_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Kanyakumari').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Kanyakumari_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Kanyakumari'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Kanyakumari_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Kanyakumari').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Kanyakumari_total_no = MasterSanctionForm.objects.filter(District__District='Kanyakumari').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Kanyakumari_total_cost = MasterSanctionForm.objects.filter(District__District='Kanyakumari').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Karur_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Karur'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Karur_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Karur'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Karur_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Karur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Karur_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Karur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Karur_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Karur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Karur_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Karur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Karur_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Karur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Karur_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Karur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Karur_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Karur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Karur_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Karur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Karur_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Karur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Karur_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Karur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Karur_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Karur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Karur_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Karur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Karur_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Karur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Karur_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Karur').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Karur_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Karur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Karur_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Karur').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Karur_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Karur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Karur_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Karur').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Karur_total_no = MasterSanctionForm.objects.filter(District__District='Karur').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Karur_total_cost = MasterSanctionForm.objects.filter(District__District='Karur').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Krishnagiri_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Krishnagiri'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Krishnagiri_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Krishnagiri'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Krishnagiri_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Krishnagiri'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Krishnagiri_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Krishnagiri'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Krishnagiri_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Krishnagiri'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Krishnagiri_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Krishnagiri'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Krishnagiri_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Krishnagiri'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Krishnagiri_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Krishnagiri'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Krishnagiri_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Krishnagiri'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Krishnagiri_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Krishnagiri'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Krishnagiri_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Krishnagiri'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Krishnagiri_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Krishnagiri'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Krishnagiri_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Krishnagiri'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Krishnagiri_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Krishnagiri'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Krishnagiri_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Krishnagiri'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Krishnagiri_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Krishnagiri').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Krishnagiri_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Krishnagiri'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Krishnagiri_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Krishnagiri').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Krishnagiri_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Krishnagiri'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Krishnagiri_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Krishnagiri').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Krishnagiri_total_no = MasterSanctionForm.objects.filter(District__District='Krishnagiri').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Krishnagiri_total_cost = MasterSanctionForm.objects.filter(District__District='Krishnagiri').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Madurai_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Madurai'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Madurai_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Madurai'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Madurai_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Madurai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Madurai_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Madurai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Madurai_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Madurai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Madurai_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Madurai'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Madurai_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Madurai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Madurai_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Madurai'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Madurai_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Madurai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Madurai_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Madurai'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Madurai_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Madurai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Madurai_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Madurai'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Madurai_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Madurai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Madurai_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Madurai'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Madurai_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Madurai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Madurai_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Madurai').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Madurai_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Madurai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Madurai_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Madurai').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Madurai_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Madurai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Madurai_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Madurai').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Madurai_total_no = MasterSanctionForm.objects.filter(District__District='Madurai').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Madurai_total_cost = MasterSanctionForm.objects.filter(District__District='Madurai').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Mayiladuthurai_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Mayiladuthurai'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Mayiladuthurai_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Mayiladuthurai'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Mayiladuthurai_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Mayiladuthurai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Mayiladuthurai_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Mayiladuthurai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Mayiladuthurai_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Mayiladuthurai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Mayiladuthurai_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Mayiladuthurai'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Mayiladuthurai_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Mayiladuthurai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Mayiladuthurai_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Mayiladuthurai'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Mayiladuthurai_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Mayiladuthurai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Mayiladuthurai_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Mayiladuthurai'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Mayiladuthurai_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Mayiladuthurai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Mayiladuthurai_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Mayiladuthurai'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Mayiladuthurai_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Mayiladuthurai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Mayiladuthurai_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Mayiladuthurai'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Mayiladuthurai_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Mayiladuthurai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Mayiladuthurai_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Mayiladuthurai').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Mayiladuthurai_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Mayiladuthurai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Mayiladuthurai_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Mayiladuthurai').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Mayiladuthurai_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Mayiladuthurai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Mayiladuthurai_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Mayiladuthurai').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Mayiladuthurai_total_no = MasterSanctionForm.objects.filter(District__District='Mayiladuthurai').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Mayiladuthurai_total_cost = MasterSanctionForm.objects.filter(District__District='Mayiladuthurai').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Nagapattinam_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Nagapattinam'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Nagapattinam_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Nagapattinam'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Nagapattinam_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Nagapattinam'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Nagapattinam_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Nagapattinam'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Nagapattinam_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Nagapattinam'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Nagapattinam_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Nagapattinam'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Nagapattinam_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Nagapattinam'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Nagapattinam_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Nagapattinam'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Nagapattinam_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Nagapattinam'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Nagapattinam_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Nagapattinam'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Nagapattinam_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Nagapattinam'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Nagapattinam_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Nagapattinam'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Nagapattinam_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Nagapattinam'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Nagapattinam_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Nagapattinam'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Nagapattinam_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Nagapattinam'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Nagapattinam_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Nagapattinam').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Nagapattinam_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Nagapattinam'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Nagapattinam_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Nagapattinam').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Nagapattinam_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Nagapattinam'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Nagapattinam_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Nagapattinam').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Nagapattinam_total_no = MasterSanctionForm.objects.filter(District__District='Nagapattinam').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Nagapattinam_total_cost = MasterSanctionForm.objects.filter(District__District='Nagapattinam').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Namakkal_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Namakkal'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Namakkal_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Namakkal'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Namakkal_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Namakkal'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Namakkal_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Namakkal'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Namakkal_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Namakkal'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Namakkal_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Namakkal'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Namakkal_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Namakkal'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Namakkal_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Namakkal'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Namakkal_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Namakkal'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Namakkal_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Namakkal'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Namakkal_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Namakkal'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Namakkal_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Namakkal'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Namakkal_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Namakkal'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Namakkal_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Namakkal'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Namakkal_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Namakkal'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Namakkal_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Namakkal').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Namakkal_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Namakkal'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Namakkal_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Namakkal').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Namakkal_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Namakkal'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Namakkal_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Namakkal').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Namakkal_total_no = MasterSanctionForm.objects.filter(District__District='Namakkal').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Namakkal_total_cost = MasterSanctionForm.objects.filter(District__District='Namakkal').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Nilgiris_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Nilgiris'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Nilgiris_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Nilgiris'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Nilgiris_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Nilgiris'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Nilgiris_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Nilgiris'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Nilgiris_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Nilgiris'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Nilgiris_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Nilgiris'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Nilgiris_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Nilgiris'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Nilgiris_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Nilgiris'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Nilgiris_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Nilgiris'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Nilgiris_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Nilgiris'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Nilgiris_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Nilgiris'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Nilgiris_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Nilgiris'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Nilgiris_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Nilgiris'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Nilgiris_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Nilgiris'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Nilgiris_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Nilgiris'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Nilgiris_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Nilgiris').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Nilgiris_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Nilgiris'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Nilgiris_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Nilgiris').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Nilgiris_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Nilgiris'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Nilgiris_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Nilgiris').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Nilgiris_total_no = MasterSanctionForm.objects.filter(District__District='Nilgiris').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Nilgiris_total_cost = MasterSanctionForm.objects.filter(District__District='Nilgiris').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Perambalur_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Perambalur'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Perambalur_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Perambalur'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Perambalur_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Perambalur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Perambalur_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Perambalur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Perambalur_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Perambalur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Perambalur_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Perambalur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Perambalur_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Perambalur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Perambalur_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Perambalur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Perambalur_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Perambalur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Perambalur_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Perambalur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Perambalur_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Perambalur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Perambalur_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Perambalur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Perambalur_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Perambalur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Perambalur_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Perambalur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Perambalur_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Perambalur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Perambalur_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Perambalur').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Perambalur_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Perambalur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Perambalur_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Perambalur').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Perambalur_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Perambalur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Perambalur_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Perambalur').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Perambalur_total_no = MasterSanctionForm.objects.filter(District__District='Perambalur').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Perambalur_total_cost = MasterSanctionForm.objects.filter(District__District='Perambalur').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Pudukottai_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Pudukottai'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Pudukottai_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Pudukottai'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Pudukottai_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Pudukottai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Pudukottai_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Pudukottai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Pudukottai_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Pudukottai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Pudukottai_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Pudukottai'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Pudukottai_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Pudukottai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Pudukottai_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Pudukottai'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Pudukottai_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Pudukottai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Pudukottai_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Pudukottai'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Pudukottai_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Pudukottai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Pudukottai_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Pudukottai'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Pudukottai_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Pudukottai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Pudukottai_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Pudukottai'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Pudukottai_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Pudukottai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Pudukottai_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Pudukottai').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Pudukottai_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Pudukottai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Pudukottai_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Pudukottai').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Pudukottai_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Pudukottai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Pudukottai_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Pudukottai').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Pudukottai_total_no = MasterSanctionForm.objects.filter(District__District='Pudukottai').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Pudukottai_total_cost = MasterSanctionForm.objects.filter(District__District='Pudukottai').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        response.context_data['KNMT_Sector'] = list(qs.values('Sector').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').annotate(**metrics).order_by('Sector'))
        Ramanathapuram_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Ramanathapuram'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Ramanathapuram_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Ramanathapuram'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Ramanathapuram_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Ramanathapuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Ramanathapuram_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Ramanathapuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Ramanathapuram_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Ramanathapuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Ramanathapuram_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Ramanathapuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Ramanathapuram_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Ramanathapuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Ramanathapuram_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Ramanathapuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Ramanathapuram_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Ramanathapuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Ramanathapuram_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Ramanathapuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Ramanathapuram_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Ramanathapuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Ramanathapuram_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Ramanathapuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Ramanathapuram_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Ramanathapuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Ramanathapuram_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Ramanathapuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Ramanathapuram_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Ramanathapuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Ramanathapuram_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Ramanathapuram').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Ramanathapuram_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Ramanathapuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Ramanathapuram_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Ramanathapuram').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Ramanathapuram_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Ramanathapuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Ramanathapuram_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Ramanathapuram').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Ramanathapuram_total_no = MasterSanctionForm.objects.filter(District__District='Ramanathapuram').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Ramanathapuram_total_cost = MasterSanctionForm.objects.filter(District__District='Ramanathapuram').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Ranipet_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Ranipet'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Ranipet_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Ranipet'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Ranipet_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Ranipet'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Ranipet_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Ranipet'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Ranipet_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Ranipet'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Ranipet_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Ranipet'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Ranipet_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Ranipet'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Ranipet_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Ranipet'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Ranipet_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Ranipet'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Ranipet_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Ranipet'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Ranipet_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Ranipet'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Ranipet_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Ranipet'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Ranipet_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Ranipet'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Ranipet_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Ranipet'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Ranipet_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Ranipet'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Ranipet_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Ranipet').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Ranipet_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Ranipet'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Ranipet_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Ranipet').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Ranipet_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Ranipet'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Ranipet_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Ranipet').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Ranipet_total_no = MasterSanctionForm.objects.filter(District__District='Ranipet').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Ranipet_total_cost = MasterSanctionForm.objects.filter(District__District='Ranipet').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Salem_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Salem'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Salem_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Salem'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Salem_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Salem'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Salem_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Salem'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Salem_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Salem'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Salem_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Salem'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Salem_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Salem'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Salem_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Salem'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Salem_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Salem'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Salem_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Salem'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Salem_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Salem'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Salem_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Salem'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Salem_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Salem'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Salem_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Salem'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Salem_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Salem'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Salem_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Salem').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Salem_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Salem'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Salem_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Salem').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Salem_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Salem'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Salem_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Salem').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Salem_total_no = MasterSanctionForm.objects.filter(District__District='Salem').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Salem_total_cost = MasterSanctionForm.objects.filter(District__District='Salem').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Sivagangai_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Sivagangai'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Sivagangai_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Sivagangai'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Sivagangai_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Sivagangai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Sivagangai_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Sivagangai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Sivagangai_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Sivagangai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Sivagangai_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Sivagangai'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Sivagangai_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Sivagangai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Sivagangai_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Sivagangai'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Sivagangai_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Sivagangai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Sivagangai_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Sivagangai'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Sivagangai_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Sivagangai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Sivagangai_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Sivagangai'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Sivagangai_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Sivagangai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Sivagangai_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Sivagangai'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Sivagangai_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Sivagangai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Sivagangai_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Sivagangai').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Sivagangai_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Sivagangai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Sivagangai_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Sivagangai').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Sivagangai_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Sivagangai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Sivagangai_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Sivagangai').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Sivagangai_total_no = MasterSanctionForm.objects.filter(District__District='Sivagangai').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Sivagangai_total_cost = MasterSanctionForm.objects.filter(District__District='Sivagangai').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tenkasi_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Tenkasi'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Tenkasi_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Tenkasi'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Tenkasi_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Tenkasi'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Tenkasi_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Tenkasi'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Tenkasi_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Tenkasi'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Tenkasi_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Tenkasi'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tenkasi_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Tenkasi'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Tenkasi_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Tenkasi'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tenkasi_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Tenkasi'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Tenkasi_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Tenkasi'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tenkasi_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Tenkasi'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Tenkasi_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Tenkasi'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tenkasi_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Tenkasi'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Tenkasi_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Tenkasi'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tenkasi_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Tenkasi'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Tenkasi_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Tenkasi').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tenkasi_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Tenkasi'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Tenkasi_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Tenkasi').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tenkasi_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Tenkasi'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Tenkasi_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Tenkasi').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Tenkasi_total_no = MasterSanctionForm.objects.filter(District__District='Tenkasi').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Tenkasi_total_cost = MasterSanctionForm.objects.filter(District__District='Tenkasi').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thanjavur_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Thanjavur'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Thanjavur_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Thanjavur'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Thanjavur_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Thanjavur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Thanjavur_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Thanjavur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Thanjavur_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Thanjavur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Thanjavur_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Thanjavur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thanjavur_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Thanjavur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Thanjavur_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Thanjavur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thanjavur_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Thanjavur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Thanjavur_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Thanjavur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thanjavur_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Thanjavur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Thanjavur_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Thanjavur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thanjavur_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Thanjavur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Thanjavur_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Thanjavur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thanjavur_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Thanjavur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Thanjavur_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Thanjavur').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thanjavur_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Thanjavur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Thanjavur_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Thanjavur').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thanjavur_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Thanjavur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Thanjavur_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Thanjavur').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Thanjavur_total_no = MasterSanctionForm.objects.filter(District__District='Thanjavur').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Thanjavur_total_cost = MasterSanctionForm.objects.filter(District__District='Thanjavur').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Theni_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Theni'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Theni_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Theni'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Theni_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Theni'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Theni_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Theni'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Theni_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Theni'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Theni_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Theni'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Theni_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Theni'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Theni_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Theni'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Theni_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Theni'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Theni_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Theni'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Theni_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Theni'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Theni_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Theni'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Theni_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Theni'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Theni_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Theni'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Theni_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Theni'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Theni_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Theni').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Theni_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Theni'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Theni_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Theni').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Theni_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Theni'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Theni_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Theni').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Theni_total_no = MasterSanctionForm.objects.filter(District__District='Theni').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Theni_total_cost = MasterSanctionForm.objects.filter(District__District='Theni').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thiruvallur_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Thiruvallur'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Thiruvallur_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Thiruvallur'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Thiruvallur_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Thiruvallur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Thiruvallur_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Thiruvallur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Thiruvallur_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Thiruvallur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Thiruvallur_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Thiruvallur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thiruvallur_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Thiruvallur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Thiruvallur_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Thiruvallur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thiruvallur_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Thiruvallur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Thiruvallur_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Thiruvallur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thiruvallur_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Thiruvallur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Thiruvallur_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Thiruvallur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thiruvallur_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Thiruvallur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Thiruvallur_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Thiruvallur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thiruvallur_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Thiruvallur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Thiruvallur_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Thiruvallur').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thiruvallur_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Thiruvallur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Thiruvallur_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Thiruvallur').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thiruvallur_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Thiruvallur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Thiruvallur_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Thiruvallur').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Thiruvallur_total_no = MasterSanctionForm.objects.filter(District__District='Thiruvallur').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Thiruvallur_total_cost = MasterSanctionForm.objects.filter(District__District='Thiruvallur').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thiruvarur_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Thiruvarur'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Thiruvarur_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Thiruvarur'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Thiruvarur_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Thiruvarur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Thiruvarur_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Thiruvarur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Thiruvarur_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Thiruvarur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Thiruvarur_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Thiruvarur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thiruvarur_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Thiruvarur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Thiruvarur_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Thiruvarur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thiruvarur_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Thiruvarur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Thiruvarur_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Thiruvarur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thiruvarur_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Thiruvarur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Thiruvarur_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Thiruvarur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thiruvarur_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Thiruvarur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Thiruvarur_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Thiruvarur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thiruvarur_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Thiruvarur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Thiruvarur_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Thiruvarur').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thiruvarur_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Thiruvarur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Thiruvarur_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Thiruvarur').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thiruvarur_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Thiruvarur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Thiruvarur_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Thiruvarur').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Thiruvarur_total_no = MasterSanctionForm.objects.filter(District__District='Thiruvarur').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Thiruvarur_total_cost = MasterSanctionForm.objects.filter(District__District='Thiruvarur').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thoothukudi_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Thoothukudi'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Thoothukudi_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Thoothukudi'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Thoothukudi_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Thoothukudi'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Thoothukudi_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Thoothukudi'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Thoothukudi_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Thoothukudi'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Thoothukudi_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Thoothukudi'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thoothukudi_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Thoothukudi'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Thoothukudi_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Thoothukudi'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thoothukudi_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Thoothukudi'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Thoothukudi_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Thoothukudi'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thoothukudi_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Thoothukudi'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Thoothukudi_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Thoothukudi'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thoothukudi_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Thoothukudi'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Thoothukudi_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Thoothukudi'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thoothukudi_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Thoothukudi'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Thoothukudi_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Thoothukudi').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thoothukudi_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Thoothukudi'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Thoothukudi_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Thoothukudi').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thoothukudi_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Thoothukudi'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Thoothukudi_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Thoothukudi').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Thoothukudi_total_no = MasterSanctionForm.objects.filter(District__District='Thoothukudi').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Thoothukudi_total_cost = MasterSanctionForm.objects.filter(District__District='Thoothukudi').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tiruchirappalli_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Tiruchirappalli'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Tiruchirappalli_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Tiruchirappalli'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Tiruchirappalli_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Tiruchirappalli'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Tiruchirappalli_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Tiruchirappalli'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Tiruchirappalli_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Tiruchirappalli'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Tiruchirappalli_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Tiruchirappalli'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tiruchirappalli_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Tiruchirappalli'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Tiruchirappalli_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Tiruchirappalli'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tiruchirappalli_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Tiruchirappalli'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Tiruchirappalli_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Tiruchirappalli'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tiruchirappalli_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Tiruchirappalli'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Tiruchirappalli_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Tiruchirappalli'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tiruchirappalli_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Tiruchirappalli'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Tiruchirappalli_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Tiruchirappalli'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tiruchirappalli_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Tiruchirappalli'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Tiruchirappalli_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Tiruchirappalli').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tiruchirappalli_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Tiruchirappalli'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Tiruchirappalli_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Tiruchirappalli').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tiruchirappalli_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Tiruchirappalli'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Tiruchirappalli_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Tiruchirappalli').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Tiruchirappalli_total_no = MasterSanctionForm.objects.filter(District__District='Tiruchirappalli').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Tiruchirappalli_total_cost = MasterSanctionForm.objects.filter(District__District='Tiruchirappalli').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tirunelveli_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Tirunelveli'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Tirunelveli_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Tirunelveli'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Tirunelveli_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Tirunelveli'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Tirunelveli_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Tirunelveli'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Tirunelveli_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Tirunelveli'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Tirunelveli_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Tirunelveli'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tirunelveli_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Tirunelveli'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Tirunelveli_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Tirunelveli'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tirunelveli_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Tirunelveli'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Tirunelveli_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Tirunelveli'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tirunelveli_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Tirunelveli'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Tirunelveli_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Tirunelveli'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tirunelveli_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Tirunelveli'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Tirunelveli_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Tirunelveli'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tirunelveli_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Tirunelveli'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Tirunelveli_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Tirunelveli').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tirunelveli_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Tirunelveli'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Tirunelveli_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Tirunelveli').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tirunelveli_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Tirunelveli'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Tirunelveli_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Tirunelveli').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Tirunelveli_total_no = MasterSanctionForm.objects.filter(District__District='Tirunelveli').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Tirunelveli_total_cost = MasterSanctionForm.objects.filter(District__District='Tirunelveli').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tirupathur_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Tirupathur'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Tirupathur_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Tirupathur'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Tirupathur_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Tirupathur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Tirupathur_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Tirupathur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Tirupathur_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Tirupathur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Tirupathur_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Tirupathur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tirupathur_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Tirupathur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Tirupathur_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Tirupathur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tirupathur_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Tirupathur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Tirupathur_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Tirupathur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tirupathur_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Tirupathur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Tirupathur_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Tirupathur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tirupathur_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Tirupathur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Tirupathur_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Tirupathur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tirupathur_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Tirupathur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Tirupathur_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Tirupathur').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tirupathur_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Tirupathur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Tirupathur_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Tirupathur').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tirupathur_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Tirupathur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Tirupathur_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Tirupathur').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Tirupathur_total_no = MasterSanctionForm.objects.filter(District__District='Tirupathur').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Tirupathur_total_cost = MasterSanctionForm.objects.filter(District__District='Tirupathur').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tiruppur_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Tiruppur'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Tiruppur_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Tiruppur'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Tiruppur_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Tiruppur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Tiruppur_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Tiruppur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Tiruppur_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Tiruppur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Tiruppur_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Tiruppur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tiruppur_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Tiruppur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Tiruppur_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Tiruppur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tiruppur_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Tiruppur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Tiruppur_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Tiruppur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tiruppur_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Tiruppur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Tiruppur_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Tiruppur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tiruppur_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Tiruppur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Tiruppur_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Tiruppur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tiruppur_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Tiruppur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Tiruppur_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Tiruppur').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tiruppur_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Tiruppur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Tiruppur_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Tiruppur').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tiruppur_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Tiruppur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Tiruppur_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Tiruppur').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Tiruppur_total_no = MasterSanctionForm.objects.filter(District__District='Tiruppur').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Tiruppur_total_cost = MasterSanctionForm.objects.filter(District__District='Tiruppur').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tiruvannamalai_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Tiruvannamalai'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Tiruvannamalai_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Tiruvannamalai'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Tiruvannamalai_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Tiruvannamalai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Tiruvannamalai_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Tiruvannamalai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Tiruvannamalai_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Tiruvannamalai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Tiruvannamalai_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Tiruvannamalai'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tiruvannamalai_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Tiruvannamalai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Tiruvannamalai_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Tiruvannamalai'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tiruvannamalai_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Tiruvannamalai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Tiruvannamalai_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Tiruvannamalai'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tiruvannamalai_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Tiruvannamalai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Tiruvannamalai_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Tiruvannamalai'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tiruvannamalai_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Tiruvannamalai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Tiruvannamalai_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Tiruvannamalai'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tiruvannamalai_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Tiruvannamalai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Tiruvannamalai_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Tiruvannamalai').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tiruvannamalai_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Tiruvannamalai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Tiruvannamalai_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Tiruvannamalai').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tiruvannamalai_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Tiruvannamalai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Tiruvannamalai_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Tiruvannamalai').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Tiruvannamalai_total_no = MasterSanctionForm.objects.filter(District__District='Tiruvannamalai').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Tiruvannamalai_total_cost = MasterSanctionForm.objects.filter(District__District='Tiruvannamalai').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Vellore_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Vellore'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Vellore_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Vellore'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Vellore_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Vellore'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Vellore_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Vellore'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Vellore_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Vellore'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Vellore_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Vellore'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Vellore_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Vellore'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Vellore_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Vellore'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Vellore_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Vellore'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Vellore_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Vellore'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Vellore_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Vellore'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Vellore_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Vellore'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Vellore_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Vellore'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Vellore_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Vellore'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Vellore_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Vellore'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Vellore_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Vellore').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Vellore_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Vellore'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Vellore_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Vellore').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Vellore_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Vellore'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Vellore_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Vellore').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Vellore_total_no = MasterSanctionForm.objects.filter(District__District='Vellore').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Vellore_total_cost = MasterSanctionForm.objects.filter(District__District='Vellore').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Villupuram_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Villupuram'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Villupuram_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Villupuram'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Villupuram_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Villupuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Villupuram_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Villupuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Villupuram_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Villupuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Villupuram_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Villupuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Villupuram_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Villupuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Villupuram_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Villupuram').filter(
            District__District='Virudhunagar'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Villupuram_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Villupuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Villupuram_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Villupuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Villupuram_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Villupuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Villupuram_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Villupuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Villupuram_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Villupuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Villupuram_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Villupuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Villupuram_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Villupuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Villupuram_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Villupuram').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Villupuram_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Villupuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Villupuram_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Villupuram').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Villupuram_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Villupuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Villupuram_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Villupuram').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Villupuram_total_no = MasterSanctionForm.objects.filter(District__District='Villupuram').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Villupuram_total_cost = MasterSanctionForm.objects.filter(District__District='Villupuram').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Virudhunagar_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Virudhunagar'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Virudhunagar_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Virudhunagar'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Virudhunagar_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Virudhunagar'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Virudhunagar_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Virudhunagar'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Virudhunagar_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Virudhunagar'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Virudhunagar_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Virudhunagar'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Virudhunagar_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Virudhunagar'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Virudhunagar_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Virudhunagar'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Virudhunagar_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Virudhunagar'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Virudhunagar_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Virudhunagar'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Virudhunagar_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Virudhunagar'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Virudhunagar_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Virudhunagar'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Virudhunagar_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Virudhunagar'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Virudhunagar_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Virudhunagar'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Virudhunagar_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Virudhunagar'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Virudhunagar_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Virudhunagar').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Virudhunagar_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Virudhunagar'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Virudhunagar_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Virudhunagar').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Virudhunagar_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Virudhunagar'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Virudhunagar_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Virudhunagar').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Virudhunagar_total_no = MasterSanctionForm.objects.filter(District__District='Virudhunagar').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Virudhunagar_total_cost = MasterSanctionForm.objects.filter(District__District='Virudhunagar').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        DMA_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        DMA_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        DMA_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        DMA_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        DMA_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        DMA_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        DMA_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        DMA_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Villupuram').filter(
            District__District='Virudhunagar'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        DMA_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        DMA_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        DMA_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        DMA_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        DMA_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        DMA_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        DMA_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        DMA_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        DMA_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        DMA_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        DMA_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        DMA_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        DMA_total_no = MasterSanctionForm.objects.filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        DMA_total_cost = MasterSanctionForm.objects.filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        extra_context = {
            'DMA_BT_RoadDMA_No': DMA_BT_RoadDMA_No,
            'DMA_BT_RoadDMA_Cost': DMA_BT_RoadDMA_Cost,
            'DMA_CC_RoadDMA_No': DMA_CC_RoadDMA_No,
            'DMA_CC_RoadDMA_Cost': DMA_CC_RoadDMA_Cost,
            'DMA_CrematoriumDMA_Cost': DMA_CrematoriumDMA_Cost,
            'DMA_CrematoriumDMA_No': DMA_CrematoriumDMA_No,
            'DMA_CulvertDMA_Cost': DMA_CulvertDMA_Cost,
            'DMA_CulvertDMA_No': DMA_CulvertDMA_No,
            'DMA_KnowledgeDMA_Centre_No': DMA_KnowledgeDMA_Centre_No,
            'DMA_KnowledgeDMA_Centre_Cost': DMA_KnowledgeDMA_Centre_Cost,
            'DMA_MarketDMA_No': DMA_MarketDMA_No,
            'DMA_MarketDMA_Cost': DMA_MarketDMA_Cost,
            'DMA_ParksDMA_No': DMA_ParksDMA_No,
            'DMA_ParksDMA_Cost': DMA_ParksDMA_Cost,
            'DMA_PaverBlockDMA_No': DMA_PaverBlockDMA_No,
            'DMA_PaverBlockDMA_Cost': DMA_PaverBlockDMA_Cost,
            'DMA_SWDDMA_No': DMA_SWDDMA_No,
            'DMA_SWDDMA_Cost': DMA_SWDDMA_Cost,
            'DMA_WBDMA_No': DMA_WBDMA_No,
            'DMA_WBDMA_Cost': DMA_WBDMA_Cost,
            'DMA_total_no': DMA_total_no,
            'DMA_total_cost': DMA_total_cost,
            'Virudhunagar_BT_RoadDMA_No': Virudhunagar_BT_RoadDMA_No,
            'Virudhunagar_BT_RoadDMA_Cost': Virudhunagar_BT_RoadDMA_Cost,
            'Virudhunagar_CC_RoadDMA_No': Virudhunagar_CC_RoadDMA_No,
            'Virudhunagar_CC_RoadDMA_Cost': Virudhunagar_CC_RoadDMA_Cost,
            'Virudhunagar_CrematoriumDMA_Cost': Virudhunagar_CrematoriumDMA_Cost,
            'Virudhunagar_CrematoriumDMA_No': Virudhunagar_CrematoriumDMA_No,
            'Virudhunagar_CulvertDMA_Cost': Virudhunagar_CulvertDMA_Cost,
            'Virudhunagar_CulvertDMA_No': Virudhunagar_CulvertDMA_No,
            'Virudhunagar_KnowledgeDMA_Centre_No': Virudhunagar_KnowledgeDMA_Centre_No,
            'Virudhunagar_KnowledgeDMA_Centre_Cost': Virudhunagar_KnowledgeDMA_Centre_Cost,
            'Virudhunagar_MarketDMA_No': Virudhunagar_MarketDMA_No,
            'Virudhunagar_MarketDMA_Cost': Virudhunagar_MarketDMA_Cost,
            'Virudhunagar_ParksDMA_No': Virudhunagar_ParksDMA_No,
            'Virudhunagar_ParksDMA_Cost': Virudhunagar_ParksDMA_Cost,
            'Virudhunagar_PaverBlockDMA_No': Virudhunagar_PaverBlockDMA_No,
            'Virudhunagar_PaverBlockDMA_Cost': Virudhunagar_PaverBlockDMA_Cost,
            'Virudhunagar_SWDDMA_No': Virudhunagar_SWDDMA_No,
            'Virudhunagar_SWDDMA_Cost': Virudhunagar_SWDDMA_Cost,
            'Virudhunagar_WBDMA_No': Virudhunagar_WBDMA_No,
            'Virudhunagar_WBDMA_Cost': Virudhunagar_WBDMA_Cost,
            'Virudhunagar_total_no': Virudhunagar_total_no,
            'Virudhunagar_total_cost': Virudhunagar_total_cost,

            'Villupuram_BT_RoadDMA_No': Villupuram_BT_RoadDMA_No,
            'Villupuram_BT_RoadDMA_Cost': Villupuram_BT_RoadDMA_Cost,
            'Villupuram_CC_RoadDMA_No': Villupuram_CC_RoadDMA_No,
            'Villupuram_CC_RoadDMA_Cost': Villupuram_CC_RoadDMA_Cost,
            'Villupuram_CrematoriumDMA_Cost': Villupuram_CrematoriumDMA_Cost,
            'Villupuram_CrematoriumDMA_No': Villupuram_CrematoriumDMA_No,
            'Villupuram_CulvertDMA_Cost': Villupuram_CulvertDMA_Cost,
            'Villupuram_CulvertDMA_No': Villupuram_CulvertDMA_No,
            'Villupuram_KnowledgeDMA_Centre_No': Villupuram_KnowledgeDMA_Centre_No,
            'Villupuram_KnowledgeDMA_Centre_Cost': Villupuram_KnowledgeDMA_Centre_Cost,
            'Villupuram_MarketDMA_No': Villupuram_MarketDMA_No,
            'Villupuram_MarketDMA_Cost': Villupuram_MarketDMA_Cost,
            'Villupuram_ParksDMA_No': Villupuram_ParksDMA_No,
            'Villupuram_ParksDMA_Cost': Villupuram_ParksDMA_Cost,
            'Villupuram_PaverBlockDMA_No': Villupuram_PaverBlockDMA_No,
            'Villupuram_PaverBlockDMA_Cost': Villupuram_PaverBlockDMA_Cost,
            'Villupuram_SWDDMA_No': Villupuram_SWDDMA_No,
            'Villupuram_SWDDMA_Cost': Villupuram_SWDDMA_Cost,
            'Villupuram_WBDMA_No': Villupuram_WBDMA_No,
            'Villupuram_WBDMA_Cost': Villupuram_WBDMA_Cost,
            'Villupuram_total_no': Villupuram_total_no,
            'Villupuram_total_cost': Villupuram_total_cost,

            'Vellore_BT_RoadDMA_No': Vellore_BT_RoadDMA_No,
            'Vellore_BT_RoadDMA_Cost': Vellore_BT_RoadDMA_Cost,
            'Vellore_CC_RoadDMA_No': Vellore_CC_RoadDMA_No,
            'Vellore_CC_RoadDMA_Cost': Vellore_CC_RoadDMA_Cost,
            'Vellore_CrematoriumDMA_Cost': Vellore_CrematoriumDMA_Cost,
            'Vellore_CrematoriumDMA_No': Vellore_CrematoriumDMA_No,
            'Vellore_CulvertDMA_Cost': Vellore_CulvertDMA_Cost,
            'Vellore_CulvertDMA_No': Vellore_CulvertDMA_No,
            'Vellore_KnowledgeDMA_Centre_No': Vellore_KnowledgeDMA_Centre_No,
            'Vellore_KnowledgeDMA_Centre_Cost': Vellore_KnowledgeDMA_Centre_Cost,
            'Vellore_MarketDMA_No': Vellore_MarketDMA_No,
            'Vellore_MarketDMA_Cost': Vellore_MarketDMA_Cost,
            'Vellore_ParksDMA_No': Vellore_ParksDMA_No,
            'Vellore_ParksDMA_Cost': Vellore_ParksDMA_Cost,
            'Vellore_PaverBlockDMA_No': Vellore_PaverBlockDMA_No,
            'Vellore_PaverBlockDMA_Cost': Vellore_PaverBlockDMA_Cost,
            'Vellore_SWDDMA_No': Vellore_SWDDMA_No,
            'Vellore_SWDDMA_Cost': Vellore_SWDDMA_Cost,
            'Vellore_WBDMA_No': Vellore_WBDMA_No,
            'Vellore_WBDMA_Cost': Vellore_WBDMA_Cost,
            'Vellore_total_no': Vellore_total_no,
            'Vellore_total_cost': Vellore_total_cost,
            'Tiruvannamalai_BT_RoadDMA_No': Tiruvannamalai_BT_RoadDMA_No,
            'Tiruvannamalai_BT_RoadDMA_Cost': Tiruvannamalai_BT_RoadDMA_Cost,
            'Tiruvannamalai_CC_RoadDMA_No': Tiruvannamalai_CC_RoadDMA_No,
            'Tiruvannamalai_CC_RoadDMA_Cost': Tiruvannamalai_CC_RoadDMA_Cost,
            'Tiruvannamalai_CrematoriumDMA_Cost': Tiruvannamalai_CrematoriumDMA_Cost,
            'Tiruvannamalai_CrematoriumDMA_No': Tiruvannamalai_CrematoriumDMA_No,
            'Tiruvannamalai_CulvertDMA_Cost': Tiruvannamalai_CulvertDMA_Cost,
            'Tiruvannamalai_CulvertDMA_No': Tiruvannamalai_CulvertDMA_No,
            'Tiruvannamalai_KnowledgeDMA_Centre_No': Tiruvannamalai_KnowledgeDMA_Centre_No,
            'Tiruvannamalai_KnowledgeDMA_Centre_Cost': Tiruvannamalai_KnowledgeDMA_Centre_Cost,
            'Tiruvannamalai_MarketDMA_No': Tiruvannamalai_MarketDMA_No,
            'Tiruvannamalai_MarketDMA_Cost': Tiruvannamalai_MarketDMA_Cost,
            'Tiruvannamalai_ParksDMA_No': Tiruvannamalai_ParksDMA_No,
            'Tiruvannamalai_ParksDMA_Cost': Tiruvannamalai_ParksDMA_Cost,
            'Tiruvannamalai_PaverBlockDMA_No': Tiruvannamalai_PaverBlockDMA_No,
            'Tiruvannamalai_PaverBlockDMA_Cost': Tiruvannamalai_PaverBlockDMA_Cost,
            'Tiruvannamalai_SWDDMA_No': Tiruvannamalai_SWDDMA_No,
            'Tiruvannamalai_SWDDMA_Cost': Tiruvannamalai_SWDDMA_Cost,
            'Tiruvannamalai_WBDMA_No': Tiruvannamalai_WBDMA_No,
            'Tiruvannamalai_WBDMA_Cost': Tiruvannamalai_WBDMA_Cost,
            'Tiruvannamalai_total_no': Tiruvannamalai_total_no,
            'Tiruvannamalai_total_cost': Tiruvannamalai_total_cost,
            'Tiruppur_BT_RoadDMA_No': Tiruppur_BT_RoadDMA_No,
            'Tiruppur_BT_RoadDMA_Cost': Tiruppur_BT_RoadDMA_Cost,
            'Tiruppur_CC_RoadDMA_No': Tiruppur_CC_RoadDMA_No,
            'Tiruppur_CC_RoadDMA_Cost': Tiruppur_CC_RoadDMA_Cost,
            'Tiruppur_CrematoriumDMA_Cost': Tiruppur_CrematoriumDMA_Cost,
            'Tiruppur_CrematoriumDMA_No': Tiruppur_CrematoriumDMA_No,
            'Tiruppur_CulvertDMA_Cost': Tiruppur_CulvertDMA_Cost,
            'Tiruppur_CulvertDMA_No': Tiruppur_CulvertDMA_No,
            'Tiruppur_KnowledgeDMA_Centre_No': Tiruppur_KnowledgeDMA_Centre_No,
            'Tiruppur_KnowledgeDMA_Centre_Cost': Tiruppur_KnowledgeDMA_Centre_Cost,
            'Tiruppur_MarketDMA_No': Tiruppur_MarketDMA_No,
            'Tiruppur_MarketDMA_Cost': Tiruppur_MarketDMA_Cost,
            'Tiruppur_ParksDMA_No': Tiruppur_ParksDMA_No,
            'Tiruppur_ParksDMA_Cost': Tiruppur_ParksDMA_Cost,
            'Tiruppur_PaverBlockDMA_No': Tiruppur_PaverBlockDMA_No,
            'Tiruppur_PaverBlockDMA_Cost': Tiruppur_PaverBlockDMA_Cost,
            'Tiruppur_SWDDMA_No': Tiruppur_SWDDMA_No,
            'Tiruppur_SWDDMA_Cost': Tiruppur_SWDDMA_Cost,
            'Tiruppur_WBDMA_No': Tiruppur_WBDMA_No,
            'Tiruppur_WBDMA_Cost': Tiruppur_WBDMA_Cost,
            'Tiruppur_total_no': Tiruppur_total_no,
            'Tiruppur_total_cost': Tiruppur_total_cost,
            'Tirupathur_BT_RoadDMA_No': Tirupathur_BT_RoadDMA_No,
            'Tirupathur_BT_RoadDMA_Cost': Tirupathur_BT_RoadDMA_Cost,
            'Tirupathur_CC_RoadDMA_No': Tirupathur_CC_RoadDMA_No,
            'Tirupathur_CC_RoadDMA_Cost': Tirupathur_CC_RoadDMA_Cost,
            'Tirupathur_CrematoriumDMA_Cost': Tirupathur_CrematoriumDMA_Cost,
            'Tirupathur_CrematoriumDMA_No': Tirupathur_CrematoriumDMA_No,
            'Tirupathur_CulvertDMA_Cost': Tirupathur_CulvertDMA_Cost,
            'Tirupathur_CulvertDMA_No': Tirupathur_CulvertDMA_No,
            'Tirupathur_KnowledgeDMA_Centre_No': Tirupathur_KnowledgeDMA_Centre_No,
            'Tirupathur_KnowledgeDMA_Centre_Cost': Tirupathur_KnowledgeDMA_Centre_Cost,
            'Tirupathur_MarketDMA_No': Tirupathur_MarketDMA_No,
            'Tirupathur_MarketDMA_Cost': Tirupathur_MarketDMA_Cost,
            'Tirupathur_ParksDMA_No': Tirupathur_ParksDMA_No,
            'Tirupathur_ParksDMA_Cost': Tirupathur_ParksDMA_Cost,
            'Tirupathur_PaverBlockDMA_No': Tirupathur_PaverBlockDMA_No,
            'Tirupathur_PaverBlockDMA_Cost': Tirupathur_PaverBlockDMA_Cost,
            'Tirupathur_SWDDMA_No': Tirupathur_SWDDMA_No,
            'Tirupathur_SWDDMA_Cost': Tirupathur_SWDDMA_Cost,
            'Tirupathur_WBDMA_No': Tirupathur_WBDMA_No,
            'Tirupathur_WBDMA_Cost': Tirupathur_WBDMA_Cost,
            'Tirupathur_total_no': Tirupathur_total_no,
            'Tirupathur_total_cost': Tirupathur_total_cost,
            'Tirunelveli_BT_RoadDMA_No': Tirunelveli_BT_RoadDMA_No,
            'Tirunelveli_BT_RoadDMA_Cost': Tirunelveli_BT_RoadDMA_Cost,
            'Tirunelveli_CC_RoadDMA_No': Tirunelveli_CC_RoadDMA_No,
            'Tirunelveli_CC_RoadDMA_Cost': Tirunelveli_CC_RoadDMA_Cost,
            'Tirunelveli_CrematoriumDMA_Cost': Tirunelveli_CrematoriumDMA_Cost,
            'Tirunelveli_CrematoriumDMA_No': Tirunelveli_CrematoriumDMA_No,
            'Tirunelveli_CulvertDMA_Cost': Tirunelveli_CulvertDMA_Cost,
            'Tirunelveli_CulvertDMA_No': Tirunelveli_CulvertDMA_No,
            'Tirunelveli_KnowledgeDMA_Centre_No': Tirunelveli_KnowledgeDMA_Centre_No,
            'Tirunelveli_KnowledgeDMA_Centre_Cost': Tirunelveli_KnowledgeDMA_Centre_Cost,
            'Tirunelveli_MarketDMA_No': Tirunelveli_MarketDMA_No,
            'Tirunelveli_MarketDMA_Cost': Tirunelveli_MarketDMA_Cost,
            'Tirunelveli_ParksDMA_No': Tirunelveli_ParksDMA_No,
            'Tirunelveli_ParksDMA_Cost': Tirunelveli_ParksDMA_Cost,
            'Tirunelveli_PaverBlockDMA_No': Tirunelveli_PaverBlockDMA_No,
            'Tirunelveli_PaverBlockDMA_Cost': Tirunelveli_PaverBlockDMA_Cost,
            'Tirunelveli_SWDDMA_No': Tirunelveli_SWDDMA_No,
            'Tirunelveli_SWDDMA_Cost': Tirunelveli_SWDDMA_Cost,
            'Tirunelveli_WBDMA_No': Tirunelveli_WBDMA_No,
            'Tirunelveli_WBDMA_Cost': Tirunelveli_WBDMA_Cost,
            'Tirunelveli_total_no': Tirunelveli_total_no,
            'Tirunelveli_total_cost': Tirunelveli_total_cost,
            'Tiruchirappalli_BT_RoadDMA_No': Tiruchirappalli_BT_RoadDMA_No,
            'Tiruchirappalli_BT_RoadDMA_Cost': Tiruchirappalli_BT_RoadDMA_Cost,
            'Tiruchirappalli_CC_RoadDMA_No': Tiruchirappalli_CC_RoadDMA_No,
            'Tiruchirappalli_CC_RoadDMA_Cost': Tiruchirappalli_CC_RoadDMA_Cost,
            'Tiruchirappalli_CrematoriumDMA_Cost': Tiruchirappalli_CrematoriumDMA_Cost,
            'Tiruchirappalli_CrematoriumDMA_No': Tiruchirappalli_CrematoriumDMA_No,
            'Tiruchirappalli_CulvertDMA_Cost': Tiruchirappalli_CulvertDMA_Cost,
            'Tiruchirappalli_CulvertDMA_No': Tiruchirappalli_CulvertDMA_No,
            'Tiruchirappalli_KnowledgeDMA_Centre_No': Tiruchirappalli_KnowledgeDMA_Centre_No,
            'Tiruchirappalli_KnowledgeDMA_Centre_Cost': Tiruchirappalli_KnowledgeDMA_Centre_Cost,
            'Tiruchirappalli_MarketDMA_No': Tiruchirappalli_MarketDMA_No,
            'Tiruchirappalli_MarketDMA_Cost': Tiruchirappalli_MarketDMA_Cost,
            'Tiruchirappalli_ParksDMA_No': Tiruchirappalli_ParksDMA_No,
            'Tiruchirappalli_ParksDMA_Cost': Tiruchirappalli_ParksDMA_Cost,
            'Tiruchirappalli_PaverBlockDMA_No': Tiruchirappalli_PaverBlockDMA_No,
            'Tiruchirappalli_PaverBlockDMA_Cost': Tiruchirappalli_PaverBlockDMA_Cost,
            'Tiruchirappalli_SWDDMA_No': Tiruchirappalli_SWDDMA_No,
            'Tiruchirappalli_SWDDMA_Cost': Tiruchirappalli_SWDDMA_Cost,
            'Tiruchirappalli_WBDMA_No': Tiruchirappalli_WBDMA_No,
            'Tiruchirappalli_WBDMA_Cost': Tiruchirappalli_WBDMA_Cost,
            'Tiruchirappalli_total_no': Tiruchirappalli_total_no,
            'Tiruchirappalli_total_cost': Tiruchirappalli_total_cost,
            'Thoothukudi_BT_RoadDMA_No': Thoothukudi_BT_RoadDMA_No,
            'Thoothukudi_BT_RoadDMA_Cost': Thoothukudi_BT_RoadDMA_Cost,
            'Thoothukudi_CC_RoadDMA_No': Thoothukudi_CC_RoadDMA_No,
            'Thoothukudi_CC_RoadDMA_Cost': Thoothukudi_CC_RoadDMA_Cost,
            'Thoothukudi_CrematoriumDMA_Cost': Thoothukudi_CrematoriumDMA_Cost,
            'Thoothukudi_CrematoriumDMA_No': Thoothukudi_CrematoriumDMA_No,
            'Thoothukudi_CulvertDMA_Cost': Thoothukudi_CulvertDMA_Cost,
            'Thoothukudi_CulvertDMA_No': Thoothukudi_CulvertDMA_No,
            'Thoothukudi_KnowledgeDMA_Centre_No': Thoothukudi_KnowledgeDMA_Centre_No,
            'Thoothukudi_KnowledgeDMA_Centre_Cost': Thoothukudi_KnowledgeDMA_Centre_Cost,
            'Thoothukudi_MarketDMA_No': Thoothukudi_MarketDMA_No,
            'Thoothukudi_MarketDMA_Cost': Thoothukudi_MarketDMA_Cost,
            'Thoothukudi_ParksDMA_No': Thoothukudi_ParksDMA_No,
            'Thoothukudi_ParksDMA_Cost': Thoothukudi_ParksDMA_Cost,
            'Thoothukudi_PaverBlockDMA_No': Thoothukudi_PaverBlockDMA_No,
            'Thoothukudi_PaverBlockDMA_Cost': Thoothukudi_PaverBlockDMA_Cost,
            'Thoothukudi_SWDDMA_No': Thoothukudi_SWDDMA_No,
            'Thoothukudi_SWDDMA_Cost': Thoothukudi_SWDDMA_Cost,
            'Thoothukudi_WBDMA_No': Thoothukudi_WBDMA_No,
            'Thoothukudi_WBDMA_Cost': Thoothukudi_WBDMA_Cost,
            'Thoothukudi_total_no': Thoothukudi_total_no,
            'Thoothukudi_total_cost': Thoothukudi_total_cost,
            'Thiruvarur_BT_RoadDMA_No': Thiruvarur_BT_RoadDMA_No,
            'Thiruvarur_BT_RoadDMA_Cost': Thiruvarur_BT_RoadDMA_Cost,
            'Thiruvarur_CC_RoadDMA_No': Thiruvarur_CC_RoadDMA_No,
            'Thiruvarur_CC_RoadDMA_Cost': Thiruvarur_CC_RoadDMA_Cost,
            'Thiruvarur_CrematoriumDMA_Cost': Thiruvarur_CrematoriumDMA_Cost,
            'Thiruvarur_CrematoriumDMA_No': Thiruvarur_CrematoriumDMA_No,
            'Thiruvarur_CulvertDMA_Cost': Thiruvarur_CulvertDMA_Cost,
            'Thiruvarur_CulvertDMA_No': Thiruvarur_CulvertDMA_No,
            'Thiruvarur_KnowledgeDMA_Centre_No': Thiruvarur_KnowledgeDMA_Centre_No,
            'Thiruvarur_KnowledgeDMA_Centre_Cost': Thiruvarur_KnowledgeDMA_Centre_Cost,
            'Thiruvarur_MarketDMA_No': Thiruvarur_MarketDMA_No,
            'Thiruvarur_MarketDMA_Cost': Thiruvarur_MarketDMA_Cost,
            'Thiruvarur_ParksDMA_No': Thiruvarur_ParksDMA_No,
            'Thiruvarur_ParksDMA_Cost': Thiruvarur_ParksDMA_Cost,
            'Thiruvarur_PaverBlockDMA_No': Thiruvarur_PaverBlockDMA_No,
            'Thiruvarur_PaverBlockDMA_Cost': Thiruvarur_PaverBlockDMA_Cost,
            'Thiruvarur_SWDDMA_No': Thiruvarur_SWDDMA_No,
            'Thiruvarur_SWDDMA_Cost': Thiruvarur_SWDDMA_Cost,
            'Thiruvarur_WBDMA_No': Thiruvarur_WBDMA_No,
            'Thiruvarur_WBDMA_Cost': Thiruvarur_WBDMA_Cost,
            'Thiruvarur_total_no': Thiruvarur_total_no,
            'Thiruvarur_total_cost': Thiruvarur_total_cost,
            'Thiruvallur_BT_RoadDMA_No': Thiruvallur_BT_RoadDMA_No,
            'Thiruvallur_BT_RoadDMA_Cost': Thiruvallur_BT_RoadDMA_Cost,
            'Thiruvallur_CC_RoadDMA_No': Thiruvallur_CC_RoadDMA_No,
            'Thiruvallur_CC_RoadDMA_Cost': Thiruvallur_CC_RoadDMA_Cost,
            'Thiruvallur_CrematoriumDMA_Cost': Thiruvallur_CrematoriumDMA_Cost,
            'Thiruvallur_CrematoriumDMA_No': Thiruvallur_CrematoriumDMA_No,
            'Thiruvallur_CulvertDMA_Cost': Thiruvallur_CulvertDMA_Cost,
            'Thiruvallur_CulvertDMA_No': Thiruvallur_CulvertDMA_No,
            'Thiruvallur_KnowledgeDMA_Centre_No': Thiruvallur_KnowledgeDMA_Centre_No,
            'Thiruvallur_KnowledgeDMA_Centre_Cost': Thiruvallur_KnowledgeDMA_Centre_Cost,
            'Thiruvallur_MarketDMA_No': Thiruvallur_MarketDMA_No,
            'Thiruvallur_MarketDMA_Cost': Thiruvallur_MarketDMA_Cost,
            'Thiruvallur_ParksDMA_No': Thiruvallur_ParksDMA_No,
            'Thiruvallur_ParksDMA_Cost': Thiruvallur_ParksDMA_Cost,
            'Thiruvallur_PaverBlockDMA_No': Thiruvallur_PaverBlockDMA_No,
            'Thiruvallur_PaverBlockDMA_Cost': Thiruvallur_PaverBlockDMA_Cost,
            'Thiruvallur_SWDDMA_No': Thiruvallur_SWDDMA_No,
            'Thiruvallur_SWDDMA_Cost': Thiruvallur_SWDDMA_Cost,
            'Thiruvallur_WBDMA_No': Thiruvallur_WBDMA_No,
            'Thiruvallur_WBDMA_Cost': Thiruvallur_WBDMA_Cost,
            'Thiruvallur_total_no': Thiruvallur_total_no,
            'Thiruvallur_total_cost': Thiruvallur_total_cost,
            'Theni_BT_RoadDMA_No': Theni_BT_RoadDMA_No,
            'Theni_BT_RoadDMA_Cost': Theni_BT_RoadDMA_Cost,
            'Theni_CC_RoadDMA_No': Theni_CC_RoadDMA_No,
            'Theni_CC_RoadDMA_Cost': Theni_CC_RoadDMA_Cost,
            'Theni_CrematoriumDMA_Cost': Theni_CrematoriumDMA_Cost,
            'Theni_CrematoriumDMA_No': Theni_CrematoriumDMA_No,
            'Theni_CulvertDMA_Cost': Theni_CulvertDMA_Cost,
            'Theni_CulvertDMA_No': Theni_CulvertDMA_No,
            'Theni_KnowledgeDMA_Centre_No': Theni_KnowledgeDMA_Centre_No,
            'Theni_KnowledgeDMA_Centre_Cost': Theni_KnowledgeDMA_Centre_Cost,
            'Theni_MarketDMA_No': Theni_MarketDMA_No,
            'Theni_MarketDMA_Cost': Theni_MarketDMA_Cost,
            'Theni_ParksDMA_No': Theni_ParksDMA_No,
            'Theni_ParksDMA_Cost': Theni_ParksDMA_Cost,
            'Theni_PaverBlockDMA_No': Theni_PaverBlockDMA_No,
            'Theni_PaverBlockDMA_Cost': Theni_PaverBlockDMA_Cost,
            'Theni_SWDDMA_No': Theni_SWDDMA_No,
            'Theni_SWDDMA_Cost': Theni_SWDDMA_Cost,
            'Theni_WBDMA_No': Theni_WBDMA_No,
            'Theni_WBDMA_Cost': Theni_WBDMA_Cost,
            'Theni_total_no': Theni_total_no,
            'Theni_total_cost': Theni_total_cost,
            'Thanjavur_BT_RoadDMA_No': Thanjavur_BT_RoadDMA_No,
            'Thanjavur_BT_RoadDMA_Cost': Thanjavur_BT_RoadDMA_Cost,
            'Thanjavur_CC_RoadDMA_No': Thanjavur_CC_RoadDMA_No,
            'Thanjavur_CC_RoadDMA_Cost': Thanjavur_CC_RoadDMA_Cost,
            'Thanjavur_CrematoriumDMA_Cost': Thanjavur_CrematoriumDMA_Cost,
            'Thanjavur_CrematoriumDMA_No': Thanjavur_CrematoriumDMA_No,
            'Thanjavur_CulvertDMA_Cost': Thanjavur_CulvertDMA_Cost,
            'Thanjavur_CulvertDMA_No': Thanjavur_CulvertDMA_No,
            'Thanjavur_KnowledgeDMA_Centre_No': Thanjavur_KnowledgeDMA_Centre_No,
            'Thanjavur_KnowledgeDMA_Centre_Cost': Thanjavur_KnowledgeDMA_Centre_Cost,
            'Thanjavur_MarketDMA_No': Thanjavur_MarketDMA_No,
            'Thanjavur_MarketDMA_Cost': Thanjavur_MarketDMA_Cost,
            'Thanjavur_ParksDMA_No': Thanjavur_ParksDMA_No,
            'Thanjavur_ParksDMA_Cost': Thanjavur_ParksDMA_Cost,
            'Thanjavur_PaverBlockDMA_No': Thanjavur_PaverBlockDMA_No,
            'Thanjavur_PaverBlockDMA_Cost': Thanjavur_PaverBlockDMA_Cost,
            'Thanjavur_SWDDMA_No': Thanjavur_SWDDMA_No,
            'Thanjavur_SWDDMA_Cost': Thanjavur_SWDDMA_Cost,
            'Thanjavur_WBDMA_No': Thanjavur_WBDMA_No,
            'Thanjavur_WBDMA_Cost': Thanjavur_WBDMA_Cost,
            'Thanjavur_total_no': Thanjavur_total_no,
            'Thanjavur_total_cost': Thanjavur_total_cost,

            'Tenkasi_BT_RoadDMA_No': Tenkasi_BT_RoadDMA_No,
            'Tenkasi_BT_RoadDMA_Cost': Tenkasi_BT_RoadDMA_Cost,
            'Tenkasi_CC_RoadDMA_No': Tenkasi_CC_RoadDMA_No,
            'Tenkasi_CC_RoadDMA_Cost': Tenkasi_CC_RoadDMA_Cost,
            'Tenkasi_CrematoriumDMA_Cost': Tenkasi_CrematoriumDMA_Cost,
            'Tenkasi_CrematoriumDMA_No': Tenkasi_CrematoriumDMA_No,
            'Tenkasi_CulvertDMA_Cost': Tenkasi_CulvertDMA_Cost,
            'Tenkasi_CulvertDMA_No': Tenkasi_CulvertDMA_No,
            'Tenkasi_KnowledgeDMA_Centre_No': Tenkasi_KnowledgeDMA_Centre_No,
            'Tenkasi_KnowledgeDMA_Centre_Cost': Tenkasi_KnowledgeDMA_Centre_Cost,
            'Tenkasi_MarketDMA_No': Tenkasi_MarketDMA_No,
            'Tenkasi_MarketDMA_Cost': Tenkasi_MarketDMA_Cost,
            'Tenkasi_ParksDMA_No': Tenkasi_ParksDMA_No,
            'Tenkasi_ParksDMA_Cost': Tenkasi_ParksDMA_Cost,
            'Tenkasi_PaverBlockDMA_No': Tenkasi_PaverBlockDMA_No,
            'Tenkasi_PaverBlockDMA_Cost': Tenkasi_PaverBlockDMA_Cost,
            'Tenkasi_SWDDMA_No': Tenkasi_SWDDMA_No,
            'Tenkasi_SWDDMA_Cost': Tenkasi_SWDDMA_Cost,
            'Tenkasi_WBDMA_No': Tenkasi_WBDMA_No,
            'Tenkasi_WBDMA_Cost': Tenkasi_WBDMA_Cost,
            'Tenkasi_total_no': Tenkasi_total_no,
            'Tenkasi_total_cost': Tenkasi_total_cost,
            'Sivagangai_BT_RoadDMA_No': Sivagangai_BT_RoadDMA_No,
            'Sivagangai_BT_RoadDMA_Cost': Sivagangai_BT_RoadDMA_Cost,
            'Sivagangai_CC_RoadDMA_No': Sivagangai_CC_RoadDMA_No,
            'Sivagangai_CC_RoadDMA_Cost': Sivagangai_CC_RoadDMA_Cost,
            'Sivagangai_CrematoriumDMA_Cost': Sivagangai_CrematoriumDMA_Cost,
            'Sivagangai_CrematoriumDMA_No': Sivagangai_CrematoriumDMA_No,
            'Sivagangai_CulvertDMA_Cost': Sivagangai_CulvertDMA_Cost,
            'Sivagangai_CulvertDMA_No': Sivagangai_CulvertDMA_No,
            'Sivagangai_KnowledgeDMA_Centre_No': Sivagangai_KnowledgeDMA_Centre_No,
            'Sivagangai_KnowledgeDMA_Centre_Cost': Sivagangai_KnowledgeDMA_Centre_Cost,
            'Sivagangai_MarketDMA_No': Sivagangai_MarketDMA_No,
            'Sivagangai_MarketDMA_Cost': Sivagangai_MarketDMA_Cost,
            'Sivagangai_ParksDMA_No': Sivagangai_ParksDMA_No,
            'Sivagangai_ParksDMA_Cost': Sivagangai_ParksDMA_Cost,
            'Sivagangai_PaverBlockDMA_No': Sivagangai_PaverBlockDMA_No,
            'Sivagangai_PaverBlockDMA_Cost': Sivagangai_PaverBlockDMA_Cost,
            'Sivagangai_SWDDMA_No': Sivagangai_SWDDMA_No,
            'Sivagangai_SWDDMA_Cost': Sivagangai_SWDDMA_Cost,
            'Sivagangai_WBDMA_No': Sivagangai_WBDMA_No,
            'Sivagangai_WBDMA_Cost': Sivagangai_WBDMA_Cost,
            'Sivagangai_total_no': Sivagangai_total_no,
            'Sivagangai_total_cost': Sivagangai_total_cost,
            'Salem_BT_RoadDMA_No': Salem_BT_RoadDMA_No,
            'Salem_BT_RoadDMA_Cost': Salem_BT_RoadDMA_Cost,
            'Salem_CC_RoadDMA_No': Salem_CC_RoadDMA_No,
            'Salem_CC_RoadDMA_Cost': Salem_CC_RoadDMA_Cost,
            'Salem_CrematoriumDMA_Cost': Salem_CrematoriumDMA_Cost,
            'Salem_CrematoriumDMA_No': Salem_CrematoriumDMA_No,
            'Salem_CulvertDMA_Cost': Salem_CulvertDMA_Cost,
            'Salem_CulvertDMA_No': Salem_CulvertDMA_No,
            'Salem_KnowledgeDMA_Centre_No': Salem_KnowledgeDMA_Centre_No,
            'Salem_KnowledgeDMA_Centre_Cost': Salem_KnowledgeDMA_Centre_Cost,
            'Salem_MarketDMA_No': Salem_MarketDMA_No,
            'Salem_MarketDMA_Cost': Salem_MarketDMA_Cost,
            'Salem_ParksDMA_No': Salem_ParksDMA_No,
            'Salem_ParksDMA_Cost': Salem_ParksDMA_Cost,
            'Salem_PaverBlockDMA_No': Salem_PaverBlockDMA_No,
            'Salem_PaverBlockDMA_Cost': Salem_PaverBlockDMA_Cost,
            'Salem_SWDDMA_No': Salem_SWDDMA_No,
            'Salem_SWDDMA_Cost': Salem_SWDDMA_Cost,
            'Salem_WBDMA_No': Salem_WBDMA_No,
            'Salem_WBDMA_Cost': Salem_WBDMA_Cost,
            'Salem_total_no': Salem_total_no,
            'Salem_total_cost': Salem_total_cost,
            'Ranipet_BT_RoadDMA_No': Ranipet_BT_RoadDMA_No,
            'Ranipet_BT_RoadDMA_Cost': Ranipet_BT_RoadDMA_Cost,
            'Ranipet_CC_RoadDMA_No': Ranipet_CC_RoadDMA_No,
            'Ranipet_CC_RoadDMA_Cost': Ranipet_CC_RoadDMA_Cost,
            'Ranipet_CrematoriumDMA_Cost': Ranipet_CrematoriumDMA_Cost,
            'Ranipet_CrematoriumDMA_No': Ranipet_CrematoriumDMA_No,
            'Ranipet_CulvertDMA_Cost': Ranipet_CulvertDMA_Cost,
            'Ranipet_CulvertDMA_No': Ranipet_CulvertDMA_No,
            'Ranipet_KnowledgeDMA_Centre_No': Ranipet_KnowledgeDMA_Centre_No,
            'Ranipet_KnowledgeDMA_Centre_Cost': Ranipet_KnowledgeDMA_Centre_Cost,
            'Ranipet_MarketDMA_No': Ranipet_MarketDMA_No,
            'Ranipet_MarketDMA_Cost': Ranipet_MarketDMA_Cost,
            'Ranipet_ParksDMA_No': Ranipet_ParksDMA_No,
            'Ranipet_ParksDMA_Cost': Ranipet_ParksDMA_Cost,
            'Ranipet_PaverBlockDMA_No': Ranipet_PaverBlockDMA_No,
            'Ranipet_PaverBlockDMA_Cost': Ranipet_PaverBlockDMA_Cost,
            'Ranipet_SWDDMA_No': Ranipet_SWDDMA_No,
            'Ranipet_SWDDMA_Cost': Ranipet_SWDDMA_Cost,
            'Ranipet_WBDMA_No': Ranipet_WBDMA_No,
            'Ranipet_WBDMA_Cost': Ranipet_WBDMA_Cost,
            'Ranipet_total_no': Ranipet_total_no,
            'Ranipet_total_cost': Ranipet_total_cost,
            'Ramanathapuram_BT_RoadDMA_No': Ramanathapuram_BT_RoadDMA_No,
            'Ramanathapuram_BT_RoadDMA_Cost': Ramanathapuram_BT_RoadDMA_Cost,
            'Ramanathapuram_CC_RoadDMA_No': Ramanathapuram_CC_RoadDMA_No,
            'Ramanathapuram_CC_RoadDMA_Cost': Ramanathapuram_CC_RoadDMA_Cost,
            'Ramanathapuram_CrematoriumDMA_Cost': Ramanathapuram_CrematoriumDMA_Cost,
            'Ramanathapuram_CrematoriumDMA_No': Ramanathapuram_CrematoriumDMA_No,
            'Ramanathapuram_CulvertDMA_Cost': Ramanathapuram_CulvertDMA_Cost,
            'Ramanathapuram_CulvertDMA_No': Ramanathapuram_CulvertDMA_No,
            'Ramanathapuram_KnowledgeDMA_Centre_No': Ramanathapuram_KnowledgeDMA_Centre_No,
            'Ramanathapuram_KnowledgeDMA_Centre_Cost': Ramanathapuram_KnowledgeDMA_Centre_Cost,
            'Ramanathapuram_MarketDMA_No': Ramanathapuram_MarketDMA_No,
            'Ramanathapuram_MarketDMA_Cost': Ramanathapuram_MarketDMA_Cost,
            'Ramanathapuram_ParksDMA_No': Ramanathapuram_ParksDMA_No,
            'Ramanathapuram_ParksDMA_Cost': Ramanathapuram_ParksDMA_Cost,
            'Ramanathapuram_PaverBlockDMA_No': Ramanathapuram_PaverBlockDMA_No,
            'Ramanathapuram_PaverBlockDMA_Cost': Ramanathapuram_PaverBlockDMA_Cost,
            'Ramanathapuram_SWDDMA_No': Ramanathapuram_SWDDMA_No,
            'Ramanathapuram_SWDDMA_Cost': Ramanathapuram_SWDDMA_Cost,
            'Ramanathapuram_WBDMA_No': Ramanathapuram_WBDMA_No,
            'Ramanathapuram_WBDMA_Cost': Ramanathapuram_WBDMA_Cost,
            'Ramanathapuram_total_no': Ramanathapuram_total_no,
            'Ramanathapuram_total_cost': Ramanathapuram_total_cost,
            'Pudukottai_BT_RoadDMA_No': Pudukottai_BT_RoadDMA_No,
            'Pudukottai_BT_RoadDMA_Cost': Pudukottai_BT_RoadDMA_Cost,
            'Pudukottai_CC_RoadDMA_No': Pudukottai_CC_RoadDMA_No,
            'Pudukottai_CC_RoadDMA_Cost': Pudukottai_CC_RoadDMA_Cost,
            'Pudukottai_CrematoriumDMA_Cost': Pudukottai_CrematoriumDMA_Cost,
            'Pudukottai_CrematoriumDMA_No': Pudukottai_CrematoriumDMA_No,
            'Pudukottai_CulvertDMA_Cost': Pudukottai_CulvertDMA_Cost,
            'Pudukottai_CulvertDMA_No': Pudukottai_CulvertDMA_No,
            'Pudukottai_KnowledgeDMA_Centre_No': Pudukottai_KnowledgeDMA_Centre_No,
            'Pudukottai_KnowledgeDMA_Centre_Cost': Pudukottai_KnowledgeDMA_Centre_Cost,
            'Pudukottai_MarketDMA_No': Pudukottai_MarketDMA_No,
            'Pudukottai_MarketDMA_Cost': Pudukottai_MarketDMA_Cost,
            'Pudukottai_ParksDMA_No': Pudukottai_ParksDMA_No,
            'Pudukottai_ParksDMA_Cost': Pudukottai_ParksDMA_Cost,
            'Pudukottai_PaverBlockDMA_No': Pudukottai_PaverBlockDMA_No,
            'Pudukottai_PaverBlockDMA_Cost': Pudukottai_PaverBlockDMA_Cost,
            'Pudukottai_SWDDMA_No': Pudukottai_SWDDMA_No,
            'Pudukottai_SWDDMA_Cost': Pudukottai_SWDDMA_Cost,
            'Pudukottai_WBDMA_No': Pudukottai_WBDMA_No,
            'Pudukottai_WBDMA_Cost': Pudukottai_WBDMA_Cost,
            'Pudukottai_total_no': Pudukottai_total_no,
            'Pudukottai_total_cost': Pudukottai_total_cost,
            'Perambalur_BT_RoadDMA_No': Perambalur_BT_RoadDMA_No,
            'Perambalur_BT_RoadDMA_Cost': Perambalur_BT_RoadDMA_Cost,
            'Perambalur_CC_RoadDMA_No': Perambalur_CC_RoadDMA_No,
            'Perambalur_CC_RoadDMA_Cost': Perambalur_CC_RoadDMA_Cost,
            'Perambalur_CrematoriumDMA_Cost': Perambalur_CrematoriumDMA_Cost,
            'Perambalur_CrematoriumDMA_No': Perambalur_CrematoriumDMA_No,
            'Perambalur_CulvertDMA_Cost': Perambalur_CulvertDMA_Cost,
            'Perambalur_CulvertDMA_No': Perambalur_CulvertDMA_No,
            'Perambalur_KnowledgeDMA_Centre_No': Perambalur_KnowledgeDMA_Centre_No,
            'Perambalur_KnowledgeDMA_Centre_Cost': Perambalur_KnowledgeDMA_Centre_Cost,
            'Perambalur_MarketDMA_No': Perambalur_MarketDMA_No,
            'Perambalur_MarketDMA_Cost': Perambalur_MarketDMA_Cost,
            'Perambalur_ParksDMA_No': Perambalur_ParksDMA_No,
            'Perambalur_ParksDMA_Cost': Perambalur_ParksDMA_Cost,
            'Perambalur_PaverBlockDMA_No': Perambalur_PaverBlockDMA_No,
            'Perambalur_PaverBlockDMA_Cost': Perambalur_PaverBlockDMA_Cost,
            'Perambalur_SWDDMA_No': Perambalur_SWDDMA_No,
            'Perambalur_SWDDMA_Cost': Perambalur_SWDDMA_Cost,
            'Perambalur_WBDMA_No': Perambalur_WBDMA_No,
            'Perambalur_WBDMA_Cost': Perambalur_WBDMA_Cost,
            'Perambalur_total_no': Perambalur_total_no,
            'Perambalur_total_cost': Perambalur_total_cost,
            'ariyalur_BT_RoadDMA_No': ariyalur_BT_RoadDMA_No,
            'ariyalur_BT_RoadDMA_Cost': ariyalur_BT_RoadDMA_Cost,
            'ariyalur_CC_RoadDMA_No': ariyalur_CC_RoadDMA_No,
            'ariyalur_CC_RoadDMA_Cost': ariyalur_CC_RoadDMA_Cost,
            'ariyalur_CrematoriumDMA_Cost': ariyalur_CrematoriumDMA_Cost,
            'ariyalur_CrematoriumDMA_No': ariyalur_CrematoriumDMA_No,
            'ariyalur_CulvertDMA_Cost': ariyalur_CulvertDMA_Cost,
            'ariyalur_CulvertDMA_No': ariyalur_CulvertDMA_No,
            'ariyalur_KnowledgeDMA_Centre_No': ariyalur_KnowledgeDMA_Centre_No,
            'ariyalur_KnowledgeDMA_Centre_Cost': ariyalur_KnowledgeDMA_Centre_Cost,
            'ariyalur_MarketDMA_No': ariyalur_MarketDMA_No,
            'ariyalur_MarketDMA_Cost': ariyalur_MarketDMA_Cost,
            'ariyalur_ParksDMA_No': ariyalur_ParksDMA_No,
            'ariyalur_ParksDMA_Cost': ariyalur_ParksDMA_Cost,
            'ariyalur_PaverBlockDMA_No': ariyalur_PaverBlockDMA_No,
            'ariyalur_PaverBlockDMA_Cost': ariyalur_PaverBlockDMA_Cost,
            'ariyalur_SWDDMA_No': ariyalur_SWDDMA_No,
            'ariyalur_SWDDMA_Cost': ariyalur_SWDDMA_Cost,
            'ariyalur_WBDMA_No': ariyalur_WBDMA_No,
            'ariyalur_WBDMA_Cost': ariyalur_WBDMA_Cost,
            'ariyalur_total_no': ariyalur_total_no,
            'ariyalur_total_cost': ariyalur_total_cost,
            'Chengalpattu_BT_RoadDMA_No': Chengalpattu_BT_RoadDMA_No,
            'Chengalpattu_BT_RoadDMA_Cost': Chengalpattu_BT_RoadDMA_Cost,
            'Chengalpattu_CC_RoadDMA_No': Chengalpattu_CC_RoadDMA_No,
            'Chengalpattu_CC_RoadDMA_Cost': Chengalpattu_CC_RoadDMA_Cost,
            'Chengalpattu_CrematoriumDMA_Cost': Chengalpattu_CrematoriumDMA_Cost,
            'Chengalpattu_CrematoriumDMA_No': Chengalpattu_CrematoriumDMA_No,
            'Chengalpattu_CulvertDMA_Cost': Chengalpattu_CulvertDMA_Cost,
            'Chengalpattu_CulvertDMA_No': Chengalpattu_CulvertDMA_No,
            'Chengalpattu_KnowledgeDMA_Centre_No': Chengalpattu_KnowledgeDMA_Centre_No,
            'Chengalpattu_KnowledgeDMA_Centre_Cost': Chengalpattu_KnowledgeDMA_Centre_Cost,
            'Chengalpattu_MarketDMA_No': Chengalpattu_MarketDMA_No,
            'Chengalpattu_MarketDMA_Cost': Chengalpattu_MarketDMA_Cost,
            'Chengalpattu_ParksDMA_No': Chengalpattu_ParksDMA_No,
            'Chengalpattu_ParksDMA_Cost': Chengalpattu_ParksDMA_Cost,
            'Chengalpattu_PaverBlockDMA_No': Chengalpattu_PaverBlockDMA_No,
            'Chengalpattu_PaverBlockDMA_Cost': Chengalpattu_PaverBlockDMA_Cost,
            'Chengalpattu_SWDDMA_No': Chengalpattu_SWDDMA_No,
            'Chengalpattu_SWDDMA_Cost': Chengalpattu_SWDDMA_Cost,
            'Chengalpattu_WBDMA_No': Chengalpattu_WBDMA_No,
            'Chengalpattu_WBDMA_Cost': Chengalpattu_WBDMA_Cost,
            'Chengalpattu_total_no': Chengalpattu_total_no,
            'Chengalpattu_total_cost': Chengalpattu_total_cost,
            'Coimbatore_BT_RoadDMA_No': Coimbatore_BT_RoadDMA_No,
            'Coimbatore_BT_RoadDMA_Cost': Coimbatore_BT_RoadDMA_Cost,
            'Coimbatore_CC_RoadDMA_No': Coimbatore_CC_RoadDMA_No,
            'Coimbatore_CC_RoadDMA_Cost': Coimbatore_CC_RoadDMA_Cost,
            'Coimbatore_CrematoriumDMA_Cost': Coimbatore_CrematoriumDMA_Cost,
            'Coimbatore_CrematoriumDMA_No': Coimbatore_CrematoriumDMA_No,
            'Coimbatore_CulvertDMA_Cost': Coimbatore_CulvertDMA_Cost,
            'Coimbatore_CulvertDMA_No': Coimbatore_CulvertDMA_No,
            'Coimbatore_KnowledgeDMA_Centre_No': Coimbatore_KnowledgeDMA_Centre_No,
            'Coimbatore_KnowledgeDMA_Centre_Cost': Coimbatore_KnowledgeDMA_Centre_Cost,
            'Coimbatore_MarketDMA_No': Coimbatore_MarketDMA_No,
            'Coimbatore_MarketDMA_Cost': Coimbatore_MarketDMA_Cost,
            'Coimbatore_ParksDMA_No': Coimbatore_ParksDMA_No,
            'Coimbatore_ParksDMA_Cost': Coimbatore_ParksDMA_Cost,
            'Coimbatore_PaverBlockDMA_No': Coimbatore_PaverBlockDMA_No,
            'Coimbatore_PaverBlockDMA_Cost': Coimbatore_PaverBlockDMA_Cost,
            'Coimbatore_SWDDMA_No': Coimbatore_SWDDMA_No,
            'Coimbatore_SWDDMA_Cost': Coimbatore_SWDDMA_Cost,
            'Coimbatore_WBDMA_No': Coimbatore_WBDMA_No,
            'Coimbatore_WBDMA_Cost': Coimbatore_WBDMA_Cost,
            'Coimbatore_total_no': Coimbatore_total_no,
            'Coimbatore_total_cost': Coimbatore_total_cost,

            'Cuddalore_BT_RoadDMA_No': Cuddalore_BT_RoadDMA_No,
            'Cuddalore_BT_RoadDMA_Cost': Cuddalore_BT_RoadDMA_Cost,
            'Cuddalore_CC_RoadDMA_No': Cuddalore_CC_RoadDMA_No,
            'Cuddalore_CC_RoadDMA_Cost': Cuddalore_CC_RoadDMA_Cost,
            'Cuddalore_CrematoriumDMA_Cost': Cuddalore_CrematoriumDMA_Cost,
            'Cuddalore_CrematoriumDMA_No': Cuddalore_CrematoriumDMA_No,
            'Cuddalore_CulvertDMA_Cost': Cuddalore_CulvertDMA_Cost,
            'Cuddalore_CulvertDMA_No': Cuddalore_CulvertDMA_No,
            'Cuddalore_KnowledgeDMA_Centre_No': Cuddalore_KnowledgeDMA_Centre_No,
            'Cuddalore_KnowledgeDMA_Centre_Cost': Cuddalore_KnowledgeDMA_Centre_Cost,
            'Cuddalore_MarketDMA_No': Cuddalore_MarketDMA_No,
            'Cuddalore_MarketDMA_Cost': Cuddalore_MarketDMA_Cost,
            'Cuddalore_ParksDMA_No': Cuddalore_ParksDMA_No,
            'Cuddalore_ParksDMA_Cost': Cuddalore_ParksDMA_Cost,
            'Cuddalore_PaverBlockDMA_No': Cuddalore_PaverBlockDMA_No,
            'Cuddalore_PaverBlockDMA_Cost': Cuddalore_PaverBlockDMA_Cost,
            'Cuddalore_SWDDMA_No': Cuddalore_SWDDMA_No,
            'Cuddalore_SWDDMA_Cost': Cuddalore_SWDDMA_Cost,
            'Cuddalore_WBDMA_No': Cuddalore_WBDMA_No,
            'Cuddalore_WBDMA_Cost': Cuddalore_WBDMA_Cost,
            'Cuddalore_total_no': Cuddalore_total_no,
            'Cuddalore_total_cost': Cuddalore_total_cost,

            'Dharmapuri_BT_RoadDMA_No': Dharmapuri_BT_RoadDMA_No,
            'Dharmapuri_BT_RoadDMA_Cost': Dharmapuri_BT_RoadDMA_Cost,
            'Dharmapuri_CC_RoadDMA_No': Dharmapuri_CC_RoadDMA_No,
            'Dharmapuri_CC_RoadDMA_Cost': Dharmapuri_CC_RoadDMA_Cost,
            'Dharmapuri_CrematoriumDMA_Cost': Dharmapuri_CrematoriumDMA_Cost,
            'Dharmapuri_CrematoriumDMA_No': Dharmapuri_CrematoriumDMA_No,
            'Dharmapuri_CulvertDMA_Cost': Dharmapuri_CulvertDMA_Cost,
            'Dharmapuri_CulvertDMA_No': Dharmapuri_CulvertDMA_No,
            'Dharmapuri_KnowledgeDMA_Centre_No': Dharmapuri_KnowledgeDMA_Centre_No,
            'Dharmapuri_KnowledgeDMA_Centre_Cost': Dharmapuri_KnowledgeDMA_Centre_Cost,
            'Dharmapuri_MarketDMA_No': Dharmapuri_MarketDMA_No,
            'Dharmapuri_MarketDMA_Cost': Dharmapuri_MarketDMA_Cost,
            'Dharmapuri_ParksDMA_No': Dharmapuri_ParksDMA_No,
            'Dharmapuri_ParksDMA_Cost': Dharmapuri_ParksDMA_Cost,
            'Dharmapuri_PaverBlockDMA_No': Dharmapuri_PaverBlockDMA_No,
            'Dharmapuri_PaverBlockDMA_Cost': Dharmapuri_PaverBlockDMA_Cost,
            'Dharmapuri_SWDDMA_No': Dharmapuri_SWDDMA_No,
            'Dharmapuri_SWDDMA_Cost': Dharmapuri_SWDDMA_Cost,
            'Dharmapuri_WBDMA_No': Dharmapuri_WBDMA_No,
            'Dharmapuri_WBDMA_Cost': Dharmapuri_WBDMA_Cost,
            'Dharmapuri_total_no': Dharmapuri_total_no,
            'Dharmapuri_total_cost': Dharmapuri_total_cost,

            'Dindigul_BT_RoadDMA_No': Dindigul_BT_RoadDMA_No,
            'Dindigul_BT_RoadDMA_Cost': Dindigul_BT_RoadDMA_Cost,
            'Dindigul_CC_RoadDMA_No': Dindigul_CC_RoadDMA_No,
            'Dindigul_CC_RoadDMA_Cost': Dindigul_CC_RoadDMA_Cost,
            'Dindigul_CrematoriumDMA_Cost': Dindigul_CrematoriumDMA_Cost,
            'Dindigul_CrematoriumDMA_No': Dindigul_CrematoriumDMA_No,
            'Dindigul_CulvertDMA_Cost': Dindigul_CulvertDMA_Cost,
            'Dindigul_CulvertDMA_No': Dindigul_CulvertDMA_No,
            'Dindigul_KnowledgeDMA_Centre_No': Dindigul_KnowledgeDMA_Centre_No,
            'Dindigul_KnowledgeDMA_Centre_Cost': Dindigul_KnowledgeDMA_Centre_Cost,
            'Dindigul_MarketDMA_No': Dindigul_MarketDMA_No,
            'Dindigul_MarketDMA_Cost': Dindigul_MarketDMA_Cost,
            'Dindigul_ParksDMA_No': Dindigul_ParksDMA_No,
            'Dindigul_ParksDMA_Cost': Dindigul_ParksDMA_Cost,
            'Dindigul_PaverBlockDMA_No': Dindigul_PaverBlockDMA_No,
            'Dindigul_PaverBlockDMA_Cost': Dindigul_PaverBlockDMA_Cost,
            'Dindigul_SWDDMA_No': Dindigul_SWDDMA_No,
            'Dindigul_SWDDMA_Cost': Dindigul_SWDDMA_Cost,
            'Dindigul_WBDMA_No': Dindigul_WBDMA_No,
            'Dindigul_WBDMA_Cost': Dindigul_WBDMA_Cost,
            'Dindigul_total_no': Dindigul_total_no,
            'Dindigul_total_cost': Dindigul_total_cost,

            'Erode_BT_RoadDMA_No': Erode_BT_RoadDMA_No,
            'Erode_BT_RoadDMA_Cost': Erode_BT_RoadDMA_Cost,
            'Erode_CC_RoadDMA_No': Erode_CC_RoadDMA_No,
            'Erode_CC_RoadDMA_Cost': Erode_CC_RoadDMA_Cost,
            'Erode_CrematoriumDMA_Cost': Erode_CrematoriumDMA_Cost,
            'Erode_CrematoriumDMA_No': Erode_CrematoriumDMA_No,
            'Erode_CulvertDMA_Cost': Erode_CulvertDMA_Cost,
            'Erode_CulvertDMA_No': Erode_CulvertDMA_No,
            'Erode_KnowledgeDMA_Centre_No': Erode_KnowledgeDMA_Centre_No,
            'Erode_KnowledgeDMA_Centre_Cost': Erode_KnowledgeDMA_Centre_Cost,
            'Erode_MarketDMA_No': Erode_MarketDMA_No,
            'Erode_MarketDMA_Cost': Erode_MarketDMA_Cost,
            'Erode_ParksDMA_No': Erode_ParksDMA_No,
            'Erode_ParksDMA_Cost': Erode_ParksDMA_Cost,
            'Erode_PaverBlockDMA_No': Erode_PaverBlockDMA_No,
            'Erode_PaverBlockDMA_Cost': Erode_PaverBlockDMA_Cost,
            'Erode_SWDDMA_No': Erode_SWDDMA_No,
            'Erode_SWDDMA_Cost': Erode_SWDDMA_Cost,
            'Erode_WBDMA_No': Erode_WBDMA_No,
            'Erode_WBDMA_Cost': Erode_WBDMA_Cost,
            'Erode_total_no': Erode_total_no,
            'Erode_total_cost': Erode_total_cost,

            'Kallakurichi_BT_RoadDMA_No': Kallakurichi_BT_RoadDMA_No,
            'Kallakurichi_BT_RoadDMA_Cost': Kallakurichi_BT_RoadDMA_Cost,
            'Kallakurichi_CC_RoadDMA_No': Kallakurichi_CC_RoadDMA_No,
            'Kallakurichi_CC_RoadDMA_Cost': Kallakurichi_CC_RoadDMA_Cost,
            'Kallakurichi_CrematoriumDMA_Cost': Kallakurichi_CrematoriumDMA_Cost,
            'Kallakurichi_CrematoriumDMA_No': Kallakurichi_CrematoriumDMA_No,
            'Kallakurichi_CulvertDMA_Cost': Kallakurichi_CulvertDMA_Cost,
            'Kallakurichi_CulvertDMA_No': Kallakurichi_CulvertDMA_No,
            'Kallakurichi_KnowledgeDMA_Centre_No': Kallakurichi_KnowledgeDMA_Centre_No,
            'Kallakurichi_KnowledgeDMA_Centre_Cost': Kallakurichi_KnowledgeDMA_Centre_Cost,
            'Kallakurichi_MarketDMA_No': Kallakurichi_MarketDMA_No,
            'Kallakurichi_MarketDMA_Cost': Kallakurichi_MarketDMA_Cost,
            'Kallakurichi_ParksDMA_No': Kallakurichi_ParksDMA_No,
            'Kallakurichi_ParksDMA_Cost': Kallakurichi_ParksDMA_Cost,
            'Kallakurichi_PaverBlockDMA_No': Kallakurichi_PaverBlockDMA_No,
            'Kallakurichi_PaverBlockDMA_Cost': Kallakurichi_PaverBlockDMA_Cost,
            'Kallakurichi_SWDDMA_No': Kallakurichi_SWDDMA_No,
            'Kallakurichi_SWDDMA_Cost': Kallakurichi_SWDDMA_Cost,
            'Kallakurichi_WBDMA_No': Kallakurichi_WBDMA_No,
            'Kallakurichi_WBDMA_Cost': Kallakurichi_WBDMA_Cost,
            'Kallakurichi_total_no': Kallakurichi_total_no,
            'Kallakurichi_total_cost': Kallakurichi_total_cost,
            'Kancheepuram_BT_RoadDMA_No': Kancheepuram_BT_RoadDMA_No,
            'Kancheepuram_BT_RoadDMA_Cost': Kancheepuram_BT_RoadDMA_Cost,
            'Kancheepuram_CC_RoadDMA_No': Kancheepuram_CC_RoadDMA_No,
            'Kancheepuram_CC_RoadDMA_Cost': Kancheepuram_CC_RoadDMA_Cost,
            'Kancheepuram_CrematoriumDMA_Cost': Kancheepuram_CrematoriumDMA_Cost,
            'Kancheepuram_CrematoriumDMA_No': Kancheepuram_CrematoriumDMA_No,
            'Kancheepuram_CulvertDMA_Cost': Kancheepuram_CulvertDMA_Cost,
            'Kancheepuram_CulvertDMA_No': Kancheepuram_CulvertDMA_No,
            'Kancheepuram_KnowledgeDMA_Centre_No': Kancheepuram_KnowledgeDMA_Centre_No,
            'Kancheepuram_KnowledgeDMA_Centre_Cost': Kancheepuram_KnowledgeDMA_Centre_Cost,
            'Kancheepuram_MarketDMA_No': Kancheepuram_MarketDMA_No,
            'Kancheepuram_MarketDMA_Cost': Kancheepuram_MarketDMA_Cost,
            'Kancheepuram_ParksDMA_No': Kancheepuram_ParksDMA_No,
            'Kancheepuram_ParksDMA_Cost': Kancheepuram_ParksDMA_Cost,
            'Kancheepuram_PaverBlockDMA_No': Kancheepuram_PaverBlockDMA_No,
            'Kancheepuram_PaverBlockDMA_Cost': Kancheepuram_PaverBlockDMA_Cost,
            'Kancheepuram_SWDDMA_No': Kancheepuram_SWDDMA_No,
            'Kancheepuram_SWDDMA_Cost': Kancheepuram_SWDDMA_Cost,
            'Kancheepuram_WBDMA_No': Kancheepuram_WBDMA_No,
            'Kancheepuram_WBDMA_Cost': Kancheepuram_WBDMA_Cost,
            'Kancheepuram_total_no': Kancheepuram_total_no,
            'Kancheepuram_total_cost': Kancheepuram_total_cost,

            'Kanyakumari_BT_RoadDMA_No': Kanyakumari_BT_RoadDMA_No,
            'Kanyakumari_BT_RoadDMA_Cost': Kanyakumari_BT_RoadDMA_Cost,
            'Kanyakumari_CC_RoadDMA_No': Kanyakumari_CC_RoadDMA_No,
            'Kanyakumari_CC_RoadDMA_Cost': Kanyakumari_CC_RoadDMA_Cost,
            'Kanyakumari_CrematoriumDMA_Cost': Kanyakumari_CrematoriumDMA_Cost,
            'Kanyakumari_CrematoriumDMA_No': Kanyakumari_CrematoriumDMA_No,
            'Kanyakumari_CulvertDMA_Cost': Kanyakumari_CulvertDMA_Cost,
            'Kanyakumari_CulvertDMA_No': Kanyakumari_CulvertDMA_No,
            'Kanyakumari_KnowledgeDMA_Centre_No': Kanyakumari_KnowledgeDMA_Centre_No,
            'Kanyakumari_KnowledgeDMA_Centre_Cost': Kanyakumari_KnowledgeDMA_Centre_Cost,
            'Kanyakumari_MarketDMA_No': Kanyakumari_MarketDMA_No,
            'Kanyakumari_MarketDMA_Cost': Kanyakumari_MarketDMA_Cost,
            'Kanyakumari_ParksDMA_No': Kanyakumari_ParksDMA_No,
            'Kanyakumari_ParksDMA_Cost': Kanyakumari_ParksDMA_Cost,
            'Kanyakumari_PaverBlockDMA_No': Kanyakumari_PaverBlockDMA_No,
            'Kanyakumari_PaverBlockDMA_Cost': Kanyakumari_PaverBlockDMA_Cost,
            'Kanyakumari_SWDDMA_No': Kanyakumari_SWDDMA_No,
            'Kanyakumari_SWDDMA_Cost': Kanyakumari_SWDDMA_Cost,
            'Kanyakumari_WBDMA_No': Kanyakumari_WBDMA_No,
            'Kanyakumari_WBDMA_Cost': Kanyakumari_WBDMA_Cost,
            'Kanyakumari_total_no': Kanyakumari_total_no,
            'Kanyakumari_total_cost': Kanyakumari_total_cost,
            'Karur_BT_RoadDMA_No': Karur_BT_RoadDMA_No,
            'Karur_BT_RoadDMA_Cost': Karur_BT_RoadDMA_Cost,
            'Karur_CC_RoadDMA_No': Karur_CC_RoadDMA_No,
            'Karur_CC_RoadDMA_Cost': Karur_CC_RoadDMA_Cost,
            'Karur_CrematoriumDMA_Cost': Karur_CrematoriumDMA_Cost,
            'Karur_CrematoriumDMA_No': Karur_CrematoriumDMA_No,
            'Karur_CulvertDMA_Cost': Karur_CulvertDMA_Cost,
            'Karur_CulvertDMA_No': Karur_CulvertDMA_No,
            'Karur_KnowledgeDMA_Centre_No': Karur_KnowledgeDMA_Centre_No,
            'Karur_KnowledgeDMA_Centre_Cost': Karur_KnowledgeDMA_Centre_Cost,
            'Karur_MarketDMA_No': Karur_MarketDMA_No,
            'Karur_MarketDMA_Cost': Karur_MarketDMA_Cost,
            'Karur_ParksDMA_No': Karur_ParksDMA_No,
            'Karur_ParksDMA_Cost': Karur_ParksDMA_Cost,
            'Karur_PaverBlockDMA_No': Karur_PaverBlockDMA_No,
            'Karur_PaverBlockDMA_Cost': Karur_PaverBlockDMA_Cost,
            'Karur_SWDDMA_No': Karur_SWDDMA_No,
            'Karur_SWDDMA_Cost': Karur_SWDDMA_Cost,
            'Karur_WBDMA_No': Karur_WBDMA_No,
            'Karur_WBDMA_Cost': Karur_WBDMA_Cost,
            'Karur_total_no': Karur_total_no,
            'Karur_total_cost': Karur_total_cost,

            'Krishnagiri_BT_RoadDMA_No': Krishnagiri_BT_RoadDMA_No,
            'Krishnagiri_BT_RoadDMA_Cost': Krishnagiri_BT_RoadDMA_Cost,
            'Krishnagiri_CC_RoadDMA_No': Krishnagiri_CC_RoadDMA_No,
            'Krishnagiri_CC_RoadDMA_Cost': Krishnagiri_CC_RoadDMA_Cost,
            'Krishnagiri_CrematoriumDMA_Cost': Krishnagiri_CrematoriumDMA_Cost,
            'Krishnagiri_CrematoriumDMA_No': Krishnagiri_CrematoriumDMA_No,
            'Krishnagiri_CulvertDMA_Cost': Krishnagiri_CulvertDMA_Cost,
            'Krishnagiri_CulvertDMA_No': Krishnagiri_CulvertDMA_No,
            'Krishnagiri_KnowledgeDMA_Centre_No': Krishnagiri_KnowledgeDMA_Centre_No,
            'Krishnagiri_KnowledgeDMA_Centre_Cost': Krishnagiri_KnowledgeDMA_Centre_Cost,
            'Krishnagiri_MarketDMA_No': Krishnagiri_MarketDMA_No,
            'Krishnagiri_MarketDMA_Cost': Krishnagiri_MarketDMA_Cost,
            'Krishnagiri_ParksDMA_No': Krishnagiri_ParksDMA_No,
            'Krishnagiri_ParksDMA_Cost': Krishnagiri_ParksDMA_Cost,
            'Krishnagiri_PaverBlockDMA_No': Krishnagiri_PaverBlockDMA_No,
            'Krishnagiri_PaverBlockDMA_Cost': Krishnagiri_PaverBlockDMA_Cost,
            'Krishnagiri_SWDDMA_No': Krishnagiri_SWDDMA_No,
            'Krishnagiri_SWDDMA_Cost': Krishnagiri_SWDDMA_Cost,
            'Krishnagiri_WBDMA_No': Krishnagiri_WBDMA_No,
            'Krishnagiri_WBDMA_Cost': Krishnagiri_WBDMA_Cost,
            'Krishnagiri_total_no': Krishnagiri_total_no,
            'Krishnagiri_total_cost': Krishnagiri_total_cost,
            'Madurai_BT_RoadDMA_No': Madurai_BT_RoadDMA_No,
            'Madurai_BT_RoadDMA_Cost': Madurai_BT_RoadDMA_Cost,
            'Madurai_CC_RoadDMA_No': Madurai_CC_RoadDMA_No,
            'Madurai_CC_RoadDMA_Cost': Madurai_CC_RoadDMA_Cost,
            'Madurai_CrematoriumDMA_Cost': Madurai_CrematoriumDMA_Cost,
            'Madurai_CrematoriumDMA_No': Madurai_CrematoriumDMA_No,
            'Madurai_CulvertDMA_Cost': Madurai_CulvertDMA_Cost,
            'Madurai_CulvertDMA_No': Madurai_CulvertDMA_No,
            'Madurai_KnowledgeDMA_Centre_No': Madurai_KnowledgeDMA_Centre_No,
            'Madurai_KnowledgeDMA_Centre_Cost': Madurai_KnowledgeDMA_Centre_Cost,
            'Madurai_MarketDMA_No': Madurai_MarketDMA_No,
            'Madurai_MarketDMA_Cost': Madurai_MarketDMA_Cost,
            'Madurai_ParksDMA_No': Madurai_ParksDMA_No,
            'Madurai_ParksDMA_Cost': Madurai_ParksDMA_Cost,
            'Madurai_PaverBlockDMA_No': Madurai_PaverBlockDMA_No,
            'Madurai_PaverBlockDMA_Cost': Madurai_PaverBlockDMA_Cost,
            'Madurai_SWDDMA_No': Madurai_SWDDMA_No,
            'Madurai_SWDDMA_Cost': Madurai_SWDDMA_Cost,
            'Madurai_WBDMA_No': Madurai_WBDMA_No,
            'Madurai_WBDMA_Cost': Madurai_WBDMA_Cost,
            'Madurai_total_no': Madurai_total_no,
            'Madurai_total_cost': Madurai_total_cost,
            'Mayiladuthurai_BT_RoadDMA_No': Mayiladuthurai_BT_RoadDMA_No,
            'Mayiladuthurai_BT_RoadDMA_Cost': Mayiladuthurai_BT_RoadDMA_Cost,
            'Mayiladuthurai_CC_RoadDMA_No': Mayiladuthurai_CC_RoadDMA_No,
            'Mayiladuthurai_CC_RoadDMA_Cost': Mayiladuthurai_CC_RoadDMA_Cost,
            'Mayiladuthurai_CrematoriumDMA_Cost': Mayiladuthurai_CrematoriumDMA_Cost,
            'Mayiladuthurai_CrematoriumDMA_No': Mayiladuthurai_CrematoriumDMA_No,
            'Mayiladuthurai_CulvertDMA_Cost': Mayiladuthurai_CulvertDMA_Cost,
            'Mayiladuthurai_CulvertDMA_No': Mayiladuthurai_CulvertDMA_No,
            'Mayiladuthurai_KnowledgeDMA_Centre_No': Mayiladuthurai_KnowledgeDMA_Centre_No,
            'Mayiladuthurai_KnowledgeDMA_Centre_Cost': Mayiladuthurai_KnowledgeDMA_Centre_Cost,
            'Mayiladuthurai_MarketDMA_No': Mayiladuthurai_MarketDMA_No,
            'Mayiladuthurai_MarketDMA_Cost': Mayiladuthurai_MarketDMA_Cost,
            'Mayiladuthurai_ParksDMA_No': Mayiladuthurai_ParksDMA_No,
            'Mayiladuthurai_ParksDMA_Cost': Mayiladuthurai_ParksDMA_Cost,
            'Mayiladuthurai_PaverBlockDMA_No': Mayiladuthurai_PaverBlockDMA_No,
            'Mayiladuthurai_PaverBlockDMA_Cost': Mayiladuthurai_PaverBlockDMA_Cost,
            'Mayiladuthurai_SWDDMA_No': Mayiladuthurai_SWDDMA_No,
            'Mayiladuthurai_SWDDMA_Cost': Mayiladuthurai_SWDDMA_Cost,
            'Mayiladuthurai_WBDMA_No': Mayiladuthurai_WBDMA_No,
            'Mayiladuthurai_WBDMA_Cost': Mayiladuthurai_WBDMA_Cost,
            'Mayiladuthurai_total_no': Mayiladuthurai_total_no,
            'Mayiladuthurai_total_cost': Mayiladuthurai_total_cost,
            'Nagapattinam_BT_RoadDMA_No': Nagapattinam_BT_RoadDMA_No,
            'Nagapattinam_BT_RoadDMA_Cost': Nagapattinam_BT_RoadDMA_Cost,
            'Nagapattinam_CC_RoadDMA_No': Nagapattinam_CC_RoadDMA_No,
            'Nagapattinam_CC_RoadDMA_Cost': Nagapattinam_CC_RoadDMA_Cost,
            'Nagapattinam_CrematoriumDMA_Cost': Nagapattinam_CrematoriumDMA_Cost,
            'Nagapattinam_CrematoriumDMA_No': Nagapattinam_CrematoriumDMA_No,
            'Nagapattinam_CulvertDMA_Cost': Nagapattinam_CulvertDMA_Cost,
            'Nagapattinam_CulvertDMA_No': Nagapattinam_CulvertDMA_No,
            'Nagapattinam_KnowledgeDMA_Centre_No': Nagapattinam_KnowledgeDMA_Centre_No,
            'Nagapattinam_KnowledgeDMA_Centre_Cost': Nagapattinam_KnowledgeDMA_Centre_Cost,
            'Nagapattinam_MarketDMA_No': Nagapattinam_MarketDMA_No,
            'Nagapattinam_MarketDMA_Cost': Nagapattinam_MarketDMA_Cost,
            'Nagapattinam_ParksDMA_No': Nagapattinam_ParksDMA_No,
            'Nagapattinam_ParksDMA_Cost': Nagapattinam_ParksDMA_Cost,
            'Nagapattinam_PaverBlockDMA_No': Nagapattinam_PaverBlockDMA_No,
            'Nagapattinam_PaverBlockDMA_Cost': Nagapattinam_PaverBlockDMA_Cost,
            'Nagapattinam_SWDDMA_No': Nagapattinam_SWDDMA_No,
            'Nagapattinam_SWDDMA_Cost': Nagapattinam_SWDDMA_Cost,
            'Nagapattinam_WBDMA_No': Nagapattinam_WBDMA_No,
            'Nagapattinam_WBDMA_Cost': Nagapattinam_WBDMA_Cost,
            'Nagapattinam_total_no': Nagapattinam_total_no,
            'Nagapattinam_total_cost': Nagapattinam_total_cost,
            'Namakkal_BT_RoadDMA_No': Namakkal_BT_RoadDMA_No,
            'Namakkal_BT_RoadDMA_Cost': Namakkal_BT_RoadDMA_Cost,
            'Namakkal_CC_RoadDMA_No': Namakkal_CC_RoadDMA_No,
            'Namakkal_CC_RoadDMA_Cost': Namakkal_CC_RoadDMA_Cost,
            'Namakkal_CrematoriumDMA_Cost': Namakkal_CrematoriumDMA_Cost,
            'Namakkal_CrematoriumDMA_No': Namakkal_CrematoriumDMA_No,
            'Namakkal_CulvertDMA_Cost': Namakkal_CulvertDMA_Cost,
            'Namakkal_CulvertDMA_No': Namakkal_CulvertDMA_No,
            'Namakkal_KnowledgeDMA_Centre_No': Namakkal_KnowledgeDMA_Centre_No,
            'Namakkal_KnowledgeDMA_Centre_Cost': Namakkal_KnowledgeDMA_Centre_Cost,
            'Namakkal_MarketDMA_No': Namakkal_MarketDMA_No,
            'Namakkal_MarketDMA_Cost': Namakkal_MarketDMA_Cost,
            'Namakkal_ParksDMA_No': Namakkal_ParksDMA_No,
            'Namakkal_ParksDMA_Cost': Namakkal_ParksDMA_Cost,
            'Namakkal_PaverBlockDMA_No': Namakkal_PaverBlockDMA_No,
            'Namakkal_PaverBlockDMA_Cost': Namakkal_PaverBlockDMA_Cost,
            'Namakkal_SWDDMA_No': Namakkal_SWDDMA_No,
            'Namakkal_SWDDMA_Cost': Namakkal_SWDDMA_Cost,
            'Namakkal_WBDMA_No': Namakkal_WBDMA_No,
            'Namakkal_WBDMA_Cost': Namakkal_WBDMA_Cost,
            'Namakkal_total_no': Namakkal_total_no,
            'Namakkal_total_cost': Namakkal_total_cost,
            'Nilgiris_BT_RoadDMA_No': Nilgiris_BT_RoadDMA_No,
            'Nilgiris_BT_RoadDMA_Cost': Nilgiris_BT_RoadDMA_Cost,
            'Nilgiris_CC_RoadDMA_No': Nilgiris_CC_RoadDMA_No,
            'Nilgiris_CC_RoadDMA_Cost': Nilgiris_CC_RoadDMA_Cost,
            'Nilgiris_CrematoriumDMA_Cost': Nilgiris_CrematoriumDMA_Cost,
            'Nilgiris_CrematoriumDMA_No': Nilgiris_CrematoriumDMA_No,
            'Nilgiris_CulvertDMA_Cost': Nilgiris_CulvertDMA_Cost,
            'Nilgiris_CulvertDMA_No': Nilgiris_CulvertDMA_No,
            'Nilgiris_KnowledgeDMA_Centre_No': Nilgiris_KnowledgeDMA_Centre_No,
            'Nilgiris_KnowledgeDMA_Centre_Cost': Nilgiris_KnowledgeDMA_Centre_Cost,
            'Nilgiris_MarketDMA_No': Nilgiris_MarketDMA_No,
            'Nilgiris_MarketDMA_Cost': Nilgiris_MarketDMA_Cost,
            'Nilgiris_ParksDMA_No': Nilgiris_ParksDMA_No,
            'Nilgiris_ParksDMA_Cost': Nilgiris_ParksDMA_Cost,
            'Nilgiris_PaverBlockDMA_No': Nilgiris_PaverBlockDMA_No,
            'Nilgiris_PaverBlockDMA_Cost': Nilgiris_PaverBlockDMA_Cost,
            'Nilgiris_SWDDMA_No': Nilgiris_SWDDMA_No,
            'Nilgiris_SWDDMA_Cost': Nilgiris_SWDDMA_Cost,
            'Nilgiris_WBDMA_No': Nilgiris_WBDMA_No,
            'Nilgiris_WBDMA_Cost': Nilgiris_WBDMA_Cost,
            'Nilgiris_total_no': Nilgiris_total_no,
            'Nilgiris_total_cost': Nilgiris_total_cost,
        }

        response.context_data.update(extra_context)
        return response

class Round(Func):
    function = "ROUND"
    template = "%(function)s(%(expressions)s::numeric, 2)"
@admin.register(DistrictWiseReport)
class DistrictWiseReportAdmin(admin.ModelAdmin):
    change_list_template = "admin/districtwisereport.html"

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        metrics = {
            'Project_ID': Count('Project_ID'),
            'ApprovedCost': Sum('ApprovedProjectCost'),
        }

        response.context_data['report_total'] = dict(
            qs.aggregate(**metrics)
        )
        ariyalur_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Ariyalur'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        ariyalur_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Ariyalur'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        ariyalur_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Ariyalur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        ariyalur_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Ariyalur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        ariyalur_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Ariyalur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        ariyalur_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Ariyalur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        ariyalur_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Ariyalur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        ariyalur_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Ariyalur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        ariyalur_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Ariyalur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        ariyalur_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Ariyalur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        ariyalur_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Ariyalur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        ariyalur_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Ariyalur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        ariyalur_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Ariyalur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        ariyalur_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Ariyalur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        ariyalur_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Ariyalur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        ariyalur_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Ariyalur').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        ariyalur_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Ariyalur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        ariyalur_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Ariyalur').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        ariyalur_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Ariyalur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        ariyalur_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Ariyalur').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        ariyalur_total_no = MasterSanctionForm.objects.filter(District__District='Ariyalur').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        ariyalur_total_cost = MasterSanctionForm.objects.filter(District__District='Ariyalur').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Chengalpattu_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Chengalpattu'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Chengalpattu_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Chengalpattu'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Chengalpattu_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Chengalpattu'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Chengalpattu_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Chengalpattu'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Chengalpattu_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Chengalpattu'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Chengalpattu_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Chengalpattu'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Chengalpattu_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Chengalpattu'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Chengalpattu_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Chengalpattu'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Chengalpattu_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Chengalpattu'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Chengalpattu_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Chengalpattu'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Chengalpattu_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Chengalpattu'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Chengalpattu_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Chengalpattu'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Chengalpattu_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Chengalpattu'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Chengalpattu_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Chengalpattu'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Chengalpattu_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Chengalpattu'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Chengalpattu_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Chengalpattu').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Chengalpattu_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Chengalpattu'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Chengalpattu_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Chengalpattu').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Chengalpattu_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Chengalpattu'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Chengalpattu_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Chengalpattu').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Chengalpattu_total_no = MasterSanctionForm.objects.filter(District__District='Chengalpattu').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Chengalpattu_total_cost = MasterSanctionForm.objects.filter(District__District='Chengalpattu').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Coimbatore_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Coimbatore'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Coimbatore_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Coimbatore'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Coimbatore_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Coimbatore'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Coimbatore_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Coimbatore'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Coimbatore_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Coimbatore'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Coimbatore_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Coimbatore'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Coimbatore_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Coimbatore'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Coimbatore_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Coimbatore'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Coimbatore_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Coimbatore'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Coimbatore_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Coimbatore'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Coimbatore_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Coimbatore'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Coimbatore_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Coimbatore'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Coimbatore_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Coimbatore'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Coimbatore_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Coimbatore'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Coimbatore_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Coimbatore'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Coimbatore_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Coimbatore').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Coimbatore_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Coimbatore'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Coimbatore_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Coimbatore').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Coimbatore_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Coimbatore'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Coimbatore_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Coimbatore').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Coimbatore_total_no = MasterSanctionForm.objects.filter(District__District='Coimbatore').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Coimbatore_total_cost = MasterSanctionForm.objects.filter(District__District='Coimbatore').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Cuddalore_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Cuddalore'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Cuddalore_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Cuddalore'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Cuddalore_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Cuddalore'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Cuddalore_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Cuddalore'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Cuddalore_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Cuddalore'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Cuddalore_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Cuddalore'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Cuddalore_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Cuddalore'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Cuddalore_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Cuddalore'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Cuddalore_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Cuddalore'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Cuddalore_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Cuddalore'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Cuddalore_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Cuddalore'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Cuddalore_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Cuddalore'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Cuddalore_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Cuddalore'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Cuddalore_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Cuddalore'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Cuddalore_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Cuddalore'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Cuddalore_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Cuddalore').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Cuddalore_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Cuddalore'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Cuddalore_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Cuddalore').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Cuddalore_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Cuddalore'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Cuddalore_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Cuddalore').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Cuddalore_total_no = MasterSanctionForm.objects.filter(District__District='Cuddalore').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Cuddalore_total_cost = MasterSanctionForm.objects.filter(District__District='Cuddalore').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Dharmapuri_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Dharmapuri'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Dharmapuri_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Dharmapuri'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Dharmapuri_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Dharmapuri'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Dharmapuri_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Dharmapuri'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Dharmapuri_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Dharmapuri'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Dharmapuri_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Dharmapuri'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Dharmapuri_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Dharmapuri'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Dharmapuri_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Dharmapuri'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Dharmapuri_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Dharmapuri'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Dharmapuri_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Dharmapuri'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Dharmapuri_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Dharmapuri'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Dharmapuri_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Dharmapuri'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Dharmapuri_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Dharmapuri'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Dharmapuri_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Dharmapuri'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Dharmapuri_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Dharmapuri'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Dharmapuri_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Dharmapuri').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Dharmapuri_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Dharmapuri'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Dharmapuri_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Dharmapuri').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Dharmapuri_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Dharmapuri'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Dharmapuri_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Dharmapuri').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Dharmapuri_total_no = MasterSanctionForm.objects.filter(District__District='Dharmapuri').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Dharmapuri_total_cost = MasterSanctionForm.objects.filter(District__District='Dharmapuri').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Dindigul_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Dindigul'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Dindigul_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Dindigul'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Dindigul_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Dindigul'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Dindigul_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Dindigul'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Dindigul_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Dindigul'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Dindigul_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Dindigul'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Dindigul_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Dindigul'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Dindigul_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Dindigul'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Dindigul_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Dindigul'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Dindigul_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Dindigul'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Dindigul_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Dindigul'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Dindigul_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Dindigul'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Dindigul_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Dindigul'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Dindigul_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Dindigul'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Dindigul_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Dindigul'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Dindigul_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Dindigul').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Dindigul_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Dindigul'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Dindigul_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Dindigul').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Dindigul_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Dindigul'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Dindigul_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Dindigul').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Dindigul_total_no = MasterSanctionForm.objects.filter(District__District='Dindigul').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Dindigul_total_cost = MasterSanctionForm.objects.filter(District__District='Dindigul').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Erode_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Erode'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Erode_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Erode'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Erode_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Erode'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Erode_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Erode'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Erode_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Erode'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Erode_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Erode'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Erode_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Erode'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Erode_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Erode'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Erode_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Erode'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Erode_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Erode'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Erode_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Erode'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Erode_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Erode'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Erode_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Erode'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Erode_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Erode'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Erode_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Erode'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Erode_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Erode').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Erode_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Erode'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Erode_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Erode').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Erode_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Erode'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Erode_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Erode').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Erode_total_no = MasterSanctionForm.objects.filter(District__District='Erode').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Erode_total_cost = MasterSanctionForm.objects.filter(District__District='Erode').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Kallakurichi_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Kallakurichi'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Kallakurichi_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Kallakurichi'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Kallakurichi_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Kallakurichi'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Kallakurichi_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Kallakurichi'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Kallakurichi_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Kallakurichi'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Kallakurichi_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Kallakurichi'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Kallakurichi_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Kallakurichi'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Kallakurichi_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Kallakurichi'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Kallakurichi_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Kallakurichi'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Kallakurichi_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Kallakurichi'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Kallakurichi_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Kallakurichi'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Kallakurichi_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Kallakurichi'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Kallakurichi_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Kallakurichi'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Kallakurichi_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Kallakurichi'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Kallakurichi_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Kallakurichi'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Kallakurichi_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Kallakurichi').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Kallakurichi_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Kallakurichi'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Kallakurichi_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Kallakurichi').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Kallakurichi_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Kallakurichi'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Kallakurichi_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Kallakurichi').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Kallakurichi_total_no = MasterSanctionForm.objects.filter(District__District='Kallakurichi').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Kallakurichi_total_cost = MasterSanctionForm.objects.filter(District__District='Kallakurichi').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Kancheepuram_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Kancheepuram'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Kancheepuram_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Kancheepuram'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Kancheepuram_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Kancheepuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Kancheepuram_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Kancheepuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Kancheepuram_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Kancheepuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Kancheepuram_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Kancheepuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Kancheepuram_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Kancheepuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Kancheepuram_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Kancheepuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Kancheepuram_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Kancheepuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Kancheepuram_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Kancheepuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Kancheepuram_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Kancheepuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Kancheepuram_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Kancheepuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Kancheepuram_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Kancheepuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Kancheepuram_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Kancheepuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Kancheepuram_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Kancheepuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Kancheepuram_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Kancheepuram').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Kancheepuram_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Kancheepuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Kancheepuram_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Kancheepuram').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Kancheepuram_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Kancheepuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Kancheepuram_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Kancheepuram').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Kancheepuram_total_no = MasterSanctionForm.objects.filter(District__District='Kancheepuram').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Kancheepuram_total_cost = MasterSanctionForm.objects.filter(District__District='Kancheepuram').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Kanyakumari_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Kanyakumari'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Kanyakumari_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Kanyakumari'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Kanyakumari_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Kanyakumari'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Kanyakumari_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Kanyakumari'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Kanyakumari_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Kanyakumari'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Kanyakumari_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Kanyakumari'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Kanyakumari_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Kanyakumari'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Kanyakumari_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Kanyakumari'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Kanyakumari_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Kanyakumari'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Kanyakumari_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Kanyakumari'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Kanyakumari_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Kanyakumari'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Kanyakumari_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Kanyakumari'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Kanyakumari_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Kanyakumari'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Kanyakumari_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Kanyakumari'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Kanyakumari_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Kanyakumari'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Kanyakumari_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Kanyakumari').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Kanyakumari_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Kanyakumari'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Kanyakumari_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Kanyakumari').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Kanyakumari_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Kanyakumari'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Kanyakumari_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Kanyakumari').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Kanyakumari_total_no = MasterSanctionForm.objects.filter(District__District='Kanyakumari').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Kanyakumari_total_cost = MasterSanctionForm.objects.filter(District__District='Kanyakumari').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Karur_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Karur'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Karur_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Karur'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Karur_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Karur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Karur_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Karur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Karur_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Karur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Karur_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Karur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Karur_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Karur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Karur_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Karur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Karur_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Karur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Karur_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Karur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Karur_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Karur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Karur_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Karur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Karur_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Karur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Karur_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Karur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Karur_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Karur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Karur_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Karur').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Karur_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Karur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Karur_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Karur').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Karur_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Karur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Karur_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Karur').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Karur_total_no = MasterSanctionForm.objects.filter(District__District='Karur').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Karur_total_cost = MasterSanctionForm.objects.filter(District__District='Karur').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Krishnagiri_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Krishnagiri'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Krishnagiri_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Krishnagiri'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Krishnagiri_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Krishnagiri'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Krishnagiri_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Krishnagiri'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Krishnagiri_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Krishnagiri'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Krishnagiri_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Krishnagiri'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Krishnagiri_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Krishnagiri'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Krishnagiri_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Krishnagiri'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Krishnagiri_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Krishnagiri'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Krishnagiri_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Krishnagiri'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Krishnagiri_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Krishnagiri'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Krishnagiri_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Krishnagiri'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Krishnagiri_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Krishnagiri'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Krishnagiri_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Krishnagiri'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Krishnagiri_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Krishnagiri'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Krishnagiri_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Krishnagiri').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Krishnagiri_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Krishnagiri'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Krishnagiri_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Krishnagiri').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Krishnagiri_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Krishnagiri'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Krishnagiri_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Krishnagiri').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Krishnagiri_total_no = MasterSanctionForm.objects.filter(District__District='Krishnagiri').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Krishnagiri_total_cost = MasterSanctionForm.objects.filter(District__District='Krishnagiri').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Madurai_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Madurai'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Madurai_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Madurai'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Madurai_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Madurai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Madurai_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Madurai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Madurai_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Madurai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Madurai_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Madurai'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Madurai_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Madurai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Madurai_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Madurai'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Madurai_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Madurai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Madurai_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Madurai'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Madurai_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Madurai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Madurai_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Madurai'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Madurai_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Madurai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Madurai_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Madurai'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Madurai_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Madurai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Madurai_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Madurai').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Madurai_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Madurai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Madurai_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Madurai').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Madurai_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Madurai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Madurai_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Madurai').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Madurai_total_no = MasterSanctionForm.objects.filter(District__District='Madurai').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Madurai_total_cost = MasterSanctionForm.objects.filter(District__District='Madurai').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Mayiladuthurai_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Mayiladuthurai'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Mayiladuthurai_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Mayiladuthurai'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Mayiladuthurai_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Mayiladuthurai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Mayiladuthurai_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Mayiladuthurai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Mayiladuthurai_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Mayiladuthurai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Mayiladuthurai_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Mayiladuthurai'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Mayiladuthurai_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Mayiladuthurai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Mayiladuthurai_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Mayiladuthurai'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Mayiladuthurai_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Mayiladuthurai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Mayiladuthurai_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Mayiladuthurai'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Mayiladuthurai_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Mayiladuthurai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Mayiladuthurai_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Mayiladuthurai'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Mayiladuthurai_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Mayiladuthurai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Mayiladuthurai_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Mayiladuthurai'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Mayiladuthurai_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Mayiladuthurai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Mayiladuthurai_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Mayiladuthurai').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Mayiladuthurai_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Mayiladuthurai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Mayiladuthurai_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Mayiladuthurai').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Mayiladuthurai_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Mayiladuthurai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Mayiladuthurai_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Mayiladuthurai').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Mayiladuthurai_total_no = MasterSanctionForm.objects.filter(District__District='Mayiladuthurai').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Mayiladuthurai_total_cost = MasterSanctionForm.objects.filter(District__District='Mayiladuthurai').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Nagapattinam_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Nagapattinam'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Nagapattinam_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Nagapattinam'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Nagapattinam_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Nagapattinam'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Nagapattinam_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Nagapattinam'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Nagapattinam_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Nagapattinam'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Nagapattinam_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Nagapattinam'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Nagapattinam_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Nagapattinam'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Nagapattinam_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Nagapattinam'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Nagapattinam_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Nagapattinam'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Nagapattinam_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Nagapattinam'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Nagapattinam_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Nagapattinam'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Nagapattinam_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Nagapattinam'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Nagapattinam_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Nagapattinam'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Nagapattinam_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Nagapattinam'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Nagapattinam_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Nagapattinam'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Nagapattinam_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Nagapattinam').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Nagapattinam_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Nagapattinam'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Nagapattinam_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Nagapattinam').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Nagapattinam_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Nagapattinam'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Nagapattinam_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Nagapattinam').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Nagapattinam_total_no = MasterSanctionForm.objects.filter(District__District='Nagapattinam').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Nagapattinam_total_cost = MasterSanctionForm.objects.filter(District__District='Nagapattinam').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Namakkal_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Namakkal'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Namakkal_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Namakkal'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Namakkal_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Namakkal'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Namakkal_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Namakkal'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Namakkal_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Namakkal'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Namakkal_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Namakkal'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Namakkal_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Namakkal'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Namakkal_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Namakkal'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Namakkal_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Namakkal'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Namakkal_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Namakkal'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Namakkal_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Namakkal'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Namakkal_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Namakkal'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Namakkal_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Namakkal'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Namakkal_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Namakkal'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Namakkal_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Namakkal'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Namakkal_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Namakkal').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Namakkal_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Namakkal'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Namakkal_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Namakkal').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Namakkal_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Namakkal'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Namakkal_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Namakkal').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Namakkal_total_no = MasterSanctionForm.objects.filter(District__District='Namakkal').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Namakkal_total_cost = MasterSanctionForm.objects.filter(District__District='Namakkal').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Nilgiris_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Nilgiris'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Nilgiris_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Nilgiris'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Nilgiris_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Nilgiris'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Nilgiris_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Nilgiris'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Nilgiris_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Nilgiris'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Nilgiris_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Nilgiris'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Nilgiris_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Nilgiris'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Nilgiris_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Nilgiris'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Nilgiris_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Nilgiris'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Nilgiris_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Nilgiris'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Nilgiris_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Nilgiris'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Nilgiris_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Nilgiris'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Nilgiris_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Nilgiris'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Nilgiris_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Nilgiris'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Nilgiris_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Nilgiris'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Nilgiris_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Nilgiris').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Nilgiris_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Nilgiris'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Nilgiris_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Nilgiris').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Nilgiris_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Nilgiris'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Nilgiris_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Nilgiris').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Nilgiris_total_no = MasterSanctionForm.objects.filter(District__District='Nilgiris').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Nilgiris_total_cost = MasterSanctionForm.objects.filter(District__District='Nilgiris').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Perambalur_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Perambalur'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Perambalur_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Perambalur'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Perambalur_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Perambalur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Perambalur_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Perambalur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Perambalur_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Perambalur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Perambalur_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Perambalur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Perambalur_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Perambalur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Perambalur_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Perambalur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Perambalur_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Perambalur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Perambalur_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Perambalur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Perambalur_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Perambalur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Perambalur_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Perambalur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Perambalur_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Perambalur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Perambalur_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Perambalur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Perambalur_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Perambalur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Perambalur_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Perambalur').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Perambalur_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Perambalur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Perambalur_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Perambalur').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Perambalur_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Perambalur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Perambalur_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Perambalur').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Perambalur_total_no = MasterSanctionForm.objects.filter(District__District='Perambalur').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Perambalur_total_cost = MasterSanctionForm.objects.filter(District__District='Perambalur').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Pudukottai_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Pudukottai'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Pudukottai_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Pudukottai'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Pudukottai_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Pudukottai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Pudukottai_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Pudukottai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Pudukottai_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Pudukottai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Pudukottai_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Pudukottai'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Pudukottai_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Pudukottai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Pudukottai_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Pudukottai'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Pudukottai_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Pudukottai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Pudukottai_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Pudukottai'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Pudukottai_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Pudukottai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Pudukottai_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Pudukottai'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Pudukottai_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Pudukottai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Pudukottai_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Pudukottai'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Pudukottai_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Pudukottai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Pudukottai_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Pudukottai').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Pudukottai_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Pudukottai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Pudukottai_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Pudukottai').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Pudukottai_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Pudukottai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Pudukottai_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Pudukottai').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Pudukottai_total_no = MasterSanctionForm.objects.filter(District__District='Pudukottai').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Pudukottai_total_cost = MasterSanctionForm.objects.filter(District__District='Pudukottai').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        response.context_data['KNMT_Sector'] = list(qs.values('Sector').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').annotate(**metrics).order_by('Sector'))
        Ramanathapuram_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Ramanathapuram'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Ramanathapuram_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Ramanathapuram'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Ramanathapuram_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Ramanathapuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Ramanathapuram_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Ramanathapuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Ramanathapuram_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Ramanathapuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Ramanathapuram_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Ramanathapuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Ramanathapuram_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Ramanathapuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Ramanathapuram_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Ramanathapuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Ramanathapuram_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Ramanathapuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Ramanathapuram_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Ramanathapuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Ramanathapuram_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Ramanathapuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Ramanathapuram_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Ramanathapuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Ramanathapuram_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Ramanathapuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Ramanathapuram_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Ramanathapuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Ramanathapuram_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Ramanathapuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Ramanathapuram_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Ramanathapuram').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Ramanathapuram_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Ramanathapuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Ramanathapuram_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Ramanathapuram').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Ramanathapuram_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Ramanathapuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Ramanathapuram_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Ramanathapuram').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Ramanathapuram_total_no = MasterSanctionForm.objects.filter(District__District='Ramanathapuram').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Ramanathapuram_total_cost = MasterSanctionForm.objects.filter(District__District='Ramanathapuram').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Ranipet_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Ranipet'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Ranipet_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Ranipet'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Ranipet_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Ranipet'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Ranipet_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Ranipet'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Ranipet_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Ranipet'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Ranipet_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Ranipet'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Ranipet_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Ranipet'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Ranipet_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Ranipet'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Ranipet_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Ranipet'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Ranipet_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Ranipet'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Ranipet_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Ranipet'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Ranipet_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Ranipet'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Ranipet_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Ranipet'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Ranipet_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Ranipet'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Ranipet_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Ranipet'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Ranipet_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Ranipet').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Ranipet_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Ranipet'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Ranipet_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Ranipet').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Ranipet_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Ranipet'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Ranipet_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Ranipet').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Ranipet_total_no = MasterSanctionForm.objects.filter(District__District='Ranipet').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Ranipet_total_cost = MasterSanctionForm.objects.filter(District__District='Ranipet').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Salem_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Salem'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Salem_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Salem'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Salem_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Salem'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Salem_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Salem'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Salem_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Salem'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Salem_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Salem'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Salem_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Salem'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Salem_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Salem'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Salem_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Salem'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Salem_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Salem'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Salem_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Salem'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Salem_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Salem'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Salem_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Salem'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Salem_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Salem'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Salem_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Salem'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Salem_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Salem').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Salem_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Salem'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Salem_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Salem').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Salem_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Salem'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Salem_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Salem').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Salem_total_no = MasterSanctionForm.objects.filter(District__District='Salem').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Salem_total_cost = MasterSanctionForm.objects.filter(District__District='Salem').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Sivagangai_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Sivagangai'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Sivagangai_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Sivagangai'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Sivagangai_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Sivagangai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Sivagangai_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Sivagangai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Sivagangai_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Sivagangai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Sivagangai_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Sivagangai'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Sivagangai_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Sivagangai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Sivagangai_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Sivagangai'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Sivagangai_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Sivagangai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Sivagangai_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Sivagangai'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Sivagangai_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Sivagangai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Sivagangai_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Sivagangai'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Sivagangai_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Sivagangai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Sivagangai_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Sivagangai'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Sivagangai_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Sivagangai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Sivagangai_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Sivagangai').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Sivagangai_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Sivagangai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Sivagangai_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Sivagangai').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Sivagangai_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Sivagangai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Sivagangai_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Sivagangai').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Sivagangai_total_no = MasterSanctionForm.objects.filter(District__District='Sivagangai').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Sivagangai_total_cost = MasterSanctionForm.objects.filter(District__District='Sivagangai').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tenkasi_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Tenkasi'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Tenkasi_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Tenkasi'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Tenkasi_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Tenkasi'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Tenkasi_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Tenkasi'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Tenkasi_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Tenkasi'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Tenkasi_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Tenkasi'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tenkasi_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Tenkasi'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Tenkasi_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Tenkasi'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tenkasi_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Tenkasi'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Tenkasi_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Tenkasi'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tenkasi_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Tenkasi'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Tenkasi_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Tenkasi'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tenkasi_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Tenkasi'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Tenkasi_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Tenkasi'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tenkasi_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Tenkasi'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Tenkasi_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Tenkasi').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tenkasi_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Tenkasi'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Tenkasi_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Tenkasi').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tenkasi_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Tenkasi'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Tenkasi_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Tenkasi').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Tenkasi_total_no = MasterSanctionForm.objects.filter(District__District='Tenkasi').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Tenkasi_total_cost = MasterSanctionForm.objects.filter(District__District='Tenkasi').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thanjavur_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Thanjavur'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Thanjavur_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Thanjavur'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Thanjavur_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Thanjavur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Thanjavur_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Thanjavur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Thanjavur_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Thanjavur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Thanjavur_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Thanjavur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thanjavur_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Thanjavur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Thanjavur_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Thanjavur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thanjavur_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Thanjavur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Thanjavur_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Thanjavur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thanjavur_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Thanjavur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Thanjavur_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Thanjavur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thanjavur_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Thanjavur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Thanjavur_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Thanjavur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thanjavur_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Thanjavur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Thanjavur_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Thanjavur').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thanjavur_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Thanjavur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Thanjavur_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Thanjavur').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thanjavur_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Thanjavur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Thanjavur_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Thanjavur').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Thanjavur_total_no = MasterSanctionForm.objects.filter(District__District='Thanjavur').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Thanjavur_total_cost = MasterSanctionForm.objects.filter(District__District='Thanjavur').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Theni_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Theni'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Theni_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Theni'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Theni_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Theni'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Theni_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Theni'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Theni_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Theni'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Theni_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Theni'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Theni_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Theni'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Theni_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Theni'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Theni_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Theni'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Theni_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Theni'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Theni_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Theni'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Theni_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Theni'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Theni_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Theni'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Theni_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Theni'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Theni_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Theni'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Theni_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Theni').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Theni_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Theni'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Theni_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Theni').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Theni_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Theni'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Theni_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Theni').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Theni_total_no = MasterSanctionForm.objects.filter(District__District='Theni').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Theni_total_cost = MasterSanctionForm.objects.filter(District__District='Theni').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thiruvallur_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Thiruvallur'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Thiruvallur_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Thiruvallur'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Thiruvallur_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Thiruvallur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Thiruvallur_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Thiruvallur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Thiruvallur_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Thiruvallur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Thiruvallur_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Thiruvallur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thiruvallur_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Thiruvallur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Thiruvallur_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Thiruvallur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thiruvallur_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Thiruvallur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Thiruvallur_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Thiruvallur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thiruvallur_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Thiruvallur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Thiruvallur_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Thiruvallur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thiruvallur_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Thiruvallur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Thiruvallur_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Thiruvallur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thiruvallur_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Thiruvallur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Thiruvallur_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Thiruvallur').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thiruvallur_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Thiruvallur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Thiruvallur_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Thiruvallur').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thiruvallur_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Thiruvallur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Thiruvallur_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Thiruvallur').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Thiruvallur_total_no = MasterSanctionForm.objects.filter(District__District='Thiruvallur').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Thiruvallur_total_cost = MasterSanctionForm.objects.filter(District__District='Thiruvallur').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thiruvarur_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Thiruvarur'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Thiruvarur_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Thiruvarur'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Thiruvarur_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Thiruvarur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Thiruvarur_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Thiruvarur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Thiruvarur_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Thiruvarur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Thiruvarur_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Thiruvarur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thiruvarur_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Thiruvarur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Thiruvarur_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Thiruvarur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thiruvarur_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Thiruvarur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Thiruvarur_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Thiruvarur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thiruvarur_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Thiruvarur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Thiruvarur_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Thiruvarur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thiruvarur_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Thiruvarur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Thiruvarur_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Thiruvarur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thiruvarur_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Thiruvarur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Thiruvarur_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Thiruvarur').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thiruvarur_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Thiruvarur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Thiruvarur_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Thiruvarur').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thiruvarur_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Thiruvarur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Thiruvarur_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Thiruvarur').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Thiruvarur_total_no = MasterSanctionForm.objects.filter(District__District='Thiruvarur').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Thiruvarur_total_cost = MasterSanctionForm.objects.filter(District__District='Thiruvarur').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thoothukudi_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Thoothukudi'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Thoothukudi_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Thoothukudi'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Thoothukudi_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Thoothukudi'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Thoothukudi_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Thoothukudi'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Thoothukudi_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Thoothukudi'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Thoothukudi_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Thoothukudi'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thoothukudi_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Thoothukudi'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Thoothukudi_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Thoothukudi'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thoothukudi_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Thoothukudi'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Thoothukudi_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Thoothukudi'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thoothukudi_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Thoothukudi'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Thoothukudi_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Thoothukudi'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thoothukudi_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Thoothukudi'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Thoothukudi_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Thoothukudi'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thoothukudi_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Thoothukudi'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Thoothukudi_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Thoothukudi').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thoothukudi_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Thoothukudi'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Thoothukudi_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Thoothukudi').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thoothukudi_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Thoothukudi'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Thoothukudi_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Thoothukudi').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Thoothukudi_total_no = MasterSanctionForm.objects.filter(District__District='Thoothukudi').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Thoothukudi_total_cost = MasterSanctionForm.objects.filter(District__District='Thoothukudi').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tiruchirappalli_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Tiruchirappalli'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Tiruchirappalli_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Tiruchirappalli'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Tiruchirappalli_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Tiruchirappalli'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Tiruchirappalli_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Tiruchirappalli'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Tiruchirappalli_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Tiruchirappalli'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Tiruchirappalli_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Tiruchirappalli'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tiruchirappalli_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Tiruchirappalli'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Tiruchirappalli_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Tiruchirappalli'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tiruchirappalli_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Tiruchirappalli'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Tiruchirappalli_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Tiruchirappalli'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tiruchirappalli_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Tiruchirappalli'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Tiruchirappalli_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Tiruchirappalli'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tiruchirappalli_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Tiruchirappalli'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Tiruchirappalli_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Tiruchirappalli'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tiruchirappalli_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Tiruchirappalli'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Tiruchirappalli_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Tiruchirappalli').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tiruchirappalli_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Tiruchirappalli'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Tiruchirappalli_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Tiruchirappalli').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tiruchirappalli_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Tiruchirappalli'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Tiruchirappalli_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Tiruchirappalli').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Tiruchirappalli_total_no = MasterSanctionForm.objects.filter(District__District='Tiruchirappalli').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Tiruchirappalli_total_cost = MasterSanctionForm.objects.filter(District__District='Tiruchirappalli').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tirunelveli_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Tirunelveli'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Tirunelveli_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Tirunelveli'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Tirunelveli_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Tirunelveli'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Tirunelveli_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Tirunelveli'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Tirunelveli_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Tirunelveli'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Tirunelveli_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Tirunelveli'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tirunelveli_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Tirunelveli'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Tirunelveli_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Tirunelveli'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tirunelveli_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Tirunelveli'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Tirunelveli_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Tirunelveli'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tirunelveli_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Tirunelveli'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Tirunelveli_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Tirunelveli'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tirunelveli_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Tirunelveli'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Tirunelveli_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Tirunelveli'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tirunelveli_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Tirunelveli'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Tirunelveli_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Tirunelveli').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tirunelveli_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Tirunelveli'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Tirunelveli_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Tirunelveli').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tirunelveli_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Tirunelveli'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Tirunelveli_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Tirunelveli').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Tirunelveli_total_no = MasterSanctionForm.objects.filter(District__District='Tirunelveli').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Tirunelveli_total_cost = MasterSanctionForm.objects.filter(District__District='Tirunelveli').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tirupathur_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Tirupathur'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Tirupathur_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Tirupathur'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Tirupathur_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Tirupathur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Tirupathur_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Tirupathur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Tirupathur_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Tirupathur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Tirupathur_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Tirupathur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tirupathur_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Tirupathur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Tirupathur_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Tirupathur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tirupathur_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Tirupathur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Tirupathur_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Tirupathur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tirupathur_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Tirupathur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Tirupathur_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Tirupathur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tirupathur_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Tirupathur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Tirupathur_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Tirupathur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tirupathur_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Tirupathur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Tirupathur_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Tirupathur').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tirupathur_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Tirupathur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Tirupathur_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Tirupathur').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tirupathur_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Tirupathur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Tirupathur_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Tirupathur').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Tirupathur_total_no = MasterSanctionForm.objects.filter(District__District='Tirupathur').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Tirupathur_total_cost = MasterSanctionForm.objects.filter(District__District='Tirupathur').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tiruppur_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Tiruppur'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Tiruppur_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Tiruppur'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Tiruppur_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Tiruppur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Tiruppur_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Tiruppur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Tiruppur_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Tiruppur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Tiruppur_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Tiruppur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tiruppur_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Tiruppur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Tiruppur_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Tiruppur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tiruppur_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Tiruppur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Tiruppur_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Tiruppur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tiruppur_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Tiruppur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Tiruppur_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Tiruppur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tiruppur_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Tiruppur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Tiruppur_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Tiruppur'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tiruppur_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Tiruppur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Tiruppur_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Tiruppur').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tiruppur_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Tiruppur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Tiruppur_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Tiruppur').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tiruppur_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Tiruppur'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Tiruppur_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Tiruppur').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Tiruppur_total_no = MasterSanctionForm.objects.filter(District__District='Tiruppur').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Tiruppur_total_cost = MasterSanctionForm.objects.filter(District__District='Tiruppur').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tiruvannamalai_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Tiruvannamalai'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Tiruvannamalai_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Tiruvannamalai'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Tiruvannamalai_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Tiruvannamalai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Tiruvannamalai_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Tiruvannamalai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Tiruvannamalai_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Tiruvannamalai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Tiruvannamalai_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Tiruvannamalai'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tiruvannamalai_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Tiruvannamalai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Tiruvannamalai_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Tiruvannamalai'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tiruvannamalai_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Tiruvannamalai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Tiruvannamalai_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Tiruvannamalai'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tiruvannamalai_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Tiruvannamalai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Tiruvannamalai_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Tiruvannamalai'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tiruvannamalai_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Tiruvannamalai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Tiruvannamalai_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Tiruvannamalai'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tiruvannamalai_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Tiruvannamalai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Tiruvannamalai_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Tiruvannamalai').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tiruvannamalai_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Tiruvannamalai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Tiruvannamalai_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Tiruvannamalai').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tiruvannamalai_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Tiruvannamalai'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Tiruvannamalai_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Tiruvannamalai').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Tiruvannamalai_total_no = MasterSanctionForm.objects.filter(District__District='Tiruvannamalai').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Tiruvannamalai_total_cost = MasterSanctionForm.objects.filter(District__District='Tiruvannamalai').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Vellore_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Vellore'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Vellore_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Vellore'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Vellore_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Vellore'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Vellore_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Vellore'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Vellore_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Vellore'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Vellore_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Vellore'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Vellore_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Vellore'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Vellore_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Vellore'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Vellore_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Vellore'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Vellore_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Vellore'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Vellore_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Vellore'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Vellore_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Vellore'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Vellore_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Vellore'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Vellore_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Vellore'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Vellore_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Vellore'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Vellore_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Vellore').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Vellore_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Vellore'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Vellore_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Vellore').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Vellore_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Vellore'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Vellore_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Vellore').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Vellore_total_no = MasterSanctionForm.objects.filter(District__District='Vellore').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Vellore_total_cost = MasterSanctionForm.objects.filter(District__District='Vellore').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Villupuram_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Villupuram'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Villupuram_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Villupuram'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Villupuram_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Villupuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Villupuram_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Villupuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Villupuram_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Villupuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Villupuram_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Villupuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Villupuram_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Villupuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Villupuram_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Villupuram').filter(
            District__District='Virudhunagar'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Villupuram_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Villupuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Villupuram_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Villupuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Villupuram_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Villupuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Villupuram_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Villupuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Villupuram_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Villupuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Villupuram_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Villupuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Villupuram_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Villupuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Villupuram_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Villupuram').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Villupuram_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Villupuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Villupuram_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Villupuram').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Villupuram_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Villupuram'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Villupuram_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Villupuram').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Villupuram_total_no = MasterSanctionForm.objects.filter(District__District='Villupuram').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Villupuram_total_cost = MasterSanctionForm.objects.filter(District__District='Villupuram').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Virudhunagar_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Virudhunagar'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Virudhunagar_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(
            District__District='Virudhunagar'
        ).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Virudhunagar_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Virudhunagar'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Virudhunagar_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            District__District='Virudhunagar'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Virudhunagar_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Virudhunagar'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Virudhunagar_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            District__District='Virudhunagar'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Virudhunagar_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Virudhunagar'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Virudhunagar_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            District__District='Virudhunagar'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Virudhunagar_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Virudhunagar'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Virudhunagar_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            District__District='Virudhunagar'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Virudhunagar_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Virudhunagar'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Virudhunagar_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            District__District='Virudhunagar'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Virudhunagar_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Virudhunagar'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Virudhunagar_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            District__District='Virudhunagar'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Virudhunagar_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Virudhunagar'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Virudhunagar_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            District__District='Virudhunagar').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Virudhunagar_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Virudhunagar'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Virudhunagar_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            District__District='Virudhunagar').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Virudhunagar_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Virudhunagar'
        ).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Virudhunagar_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            District__District='Virudhunagar').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        Virudhunagar_total_no = MasterSanctionForm.objects.filter(District__District='Virudhunagar').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        Virudhunagar_total_cost = MasterSanctionForm.objects.filter(District__District='Virudhunagar').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        DMA_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        DMA_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        DMA_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        DMA_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
        DMA_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        DMA_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        DMA_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        DMA_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Villupuram').filter(
            District__District='Virudhunagar'
        ).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        DMA_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        DMA_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        DMA_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        DMA_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        DMA_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        DMA_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        DMA_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        DMA_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        DMA_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        DMA_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        DMA_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        DMA_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        DMA_total_no = MasterSanctionForm.objects.filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        DMA_total_cost = MasterSanctionForm.objects.filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        extra_context = {
            'DMA_BT_RoadDMA_No': DMA_BT_RoadDMA_No,
            'DMA_BT_RoadDMA_Cost': DMA_BT_RoadDMA_Cost,
            'DMA_CC_RoadDMA_No': DMA_CC_RoadDMA_No,
            'DMA_CC_RoadDMA_Cost': DMA_CC_RoadDMA_Cost,
            'DMA_CrematoriumDMA_Cost': DMA_CrematoriumDMA_Cost,
            'DMA_CrematoriumDMA_No': DMA_CrematoriumDMA_No,
            'DMA_CulvertDMA_Cost': DMA_CulvertDMA_Cost,
            'DMA_CulvertDMA_No': DMA_CulvertDMA_No,
            'DMA_KnowledgeDMA_Centre_No': DMA_KnowledgeDMA_Centre_No,
            'DMA_KnowledgeDMA_Centre_Cost': DMA_KnowledgeDMA_Centre_Cost,
            'DMA_MarketDMA_No': DMA_MarketDMA_No,
            'DMA_MarketDMA_Cost': DMA_MarketDMA_Cost,
            'DMA_ParksDMA_No': DMA_ParksDMA_No,
            'DMA_ParksDMA_Cost': DMA_ParksDMA_Cost,
            'DMA_PaverBlockDMA_No': DMA_PaverBlockDMA_No,
            'DMA_PaverBlockDMA_Cost': DMA_PaverBlockDMA_Cost,
            'DMA_SWDDMA_No': DMA_SWDDMA_No,
            'DMA_SWDDMA_Cost': DMA_SWDDMA_Cost,
            'DMA_WBDMA_No': DMA_WBDMA_No,
            'DMA_WBDMA_Cost': DMA_WBDMA_Cost,
            'DMA_total_no': DMA_total_no,
            'DMA_total_cost': DMA_total_cost,
            'Virudhunagar_BT_RoadDMA_No': Virudhunagar_BT_RoadDMA_No,
            'Virudhunagar_BT_RoadDMA_Cost': Virudhunagar_BT_RoadDMA_Cost,
            'Virudhunagar_CC_RoadDMA_No': Virudhunagar_CC_RoadDMA_No,
            'Virudhunagar_CC_RoadDMA_Cost': Virudhunagar_CC_RoadDMA_Cost,
            'Virudhunagar_CrematoriumDMA_Cost': Virudhunagar_CrematoriumDMA_Cost,
            'Virudhunagar_CrematoriumDMA_No': Virudhunagar_CrematoriumDMA_No,
            'Virudhunagar_CulvertDMA_Cost': Virudhunagar_CulvertDMA_Cost,
            'Virudhunagar_CulvertDMA_No': Virudhunagar_CulvertDMA_No,
            'Virudhunagar_KnowledgeDMA_Centre_No': Virudhunagar_KnowledgeDMA_Centre_No,
            'Virudhunagar_KnowledgeDMA_Centre_Cost': Virudhunagar_KnowledgeDMA_Centre_Cost,
            'Virudhunagar_MarketDMA_No': Virudhunagar_MarketDMA_No,
            'Virudhunagar_MarketDMA_Cost': Virudhunagar_MarketDMA_Cost,
            'Virudhunagar_ParksDMA_No': Virudhunagar_ParksDMA_No,
            'Virudhunagar_ParksDMA_Cost': Virudhunagar_ParksDMA_Cost,
            'Virudhunagar_PaverBlockDMA_No': Virudhunagar_PaverBlockDMA_No,
            'Virudhunagar_PaverBlockDMA_Cost': Virudhunagar_PaverBlockDMA_Cost,
            'Virudhunagar_SWDDMA_No': Virudhunagar_SWDDMA_No,
            'Virudhunagar_SWDDMA_Cost': Virudhunagar_SWDDMA_Cost,
            'Virudhunagar_WBDMA_No': Virudhunagar_WBDMA_No,
            'Virudhunagar_WBDMA_Cost': Virudhunagar_WBDMA_Cost,
            'Virudhunagar_total_no': Virudhunagar_total_no,
            'Virudhunagar_total_cost': Virudhunagar_total_cost,

            'Villupuram_BT_RoadDMA_No': Villupuram_BT_RoadDMA_No,
            'Villupuram_BT_RoadDMA_Cost': Villupuram_BT_RoadDMA_Cost,
            'Villupuram_CC_RoadDMA_No': Villupuram_CC_RoadDMA_No,
            'Villupuram_CC_RoadDMA_Cost': Villupuram_CC_RoadDMA_Cost,
            'Villupuram_CrematoriumDMA_Cost': Villupuram_CrematoriumDMA_Cost,
            'Villupuram_CrematoriumDMA_No': Villupuram_CrematoriumDMA_No,
            'Villupuram_CulvertDMA_Cost': Villupuram_CulvertDMA_Cost,
            'Villupuram_CulvertDMA_No': Villupuram_CulvertDMA_No,
            'Villupuram_KnowledgeDMA_Centre_No': Villupuram_KnowledgeDMA_Centre_No,
            'Villupuram_KnowledgeDMA_Centre_Cost': Villupuram_KnowledgeDMA_Centre_Cost,
            'Villupuram_MarketDMA_No': Villupuram_MarketDMA_No,
            'Villupuram_MarketDMA_Cost': Villupuram_MarketDMA_Cost,
            'Villupuram_ParksDMA_No': Villupuram_ParksDMA_No,
            'Villupuram_ParksDMA_Cost': Villupuram_ParksDMA_Cost,
            'Villupuram_PaverBlockDMA_No': Villupuram_PaverBlockDMA_No,
            'Villupuram_PaverBlockDMA_Cost': Villupuram_PaverBlockDMA_Cost,
            'Villupuram_SWDDMA_No': Villupuram_SWDDMA_No,
            'Villupuram_SWDDMA_Cost': Villupuram_SWDDMA_Cost,
            'Villupuram_WBDMA_No': Villupuram_WBDMA_No,
            'Villupuram_WBDMA_Cost': Villupuram_WBDMA_Cost,
            'Villupuram_total_no': Villupuram_total_no,
            'Villupuram_total_cost': Villupuram_total_cost,

            'Vellore_BT_RoadDMA_No': Vellore_BT_RoadDMA_No,
            'Vellore_BT_RoadDMA_Cost': Vellore_BT_RoadDMA_Cost,
            'Vellore_CC_RoadDMA_No': Vellore_CC_RoadDMA_No,
            'Vellore_CC_RoadDMA_Cost': Vellore_CC_RoadDMA_Cost,
            'Vellore_CrematoriumDMA_Cost': Vellore_CrematoriumDMA_Cost,
            'Vellore_CrematoriumDMA_No': Vellore_CrematoriumDMA_No,
            'Vellore_CulvertDMA_Cost': Vellore_CulvertDMA_Cost,
            'Vellore_CulvertDMA_No': Vellore_CulvertDMA_No,
            'Vellore_KnowledgeDMA_Centre_No': Vellore_KnowledgeDMA_Centre_No,
            'Vellore_KnowledgeDMA_Centre_Cost': Vellore_KnowledgeDMA_Centre_Cost,
            'Vellore_MarketDMA_No': Vellore_MarketDMA_No,
            'Vellore_MarketDMA_Cost': Vellore_MarketDMA_Cost,
            'Vellore_ParksDMA_No': Vellore_ParksDMA_No,
            'Vellore_ParksDMA_Cost': Vellore_ParksDMA_Cost,
            'Vellore_PaverBlockDMA_No': Vellore_PaverBlockDMA_No,
            'Vellore_PaverBlockDMA_Cost': Vellore_PaverBlockDMA_Cost,
            'Vellore_SWDDMA_No': Vellore_SWDDMA_No,
            'Vellore_SWDDMA_Cost': Vellore_SWDDMA_Cost,
            'Vellore_WBDMA_No': Vellore_WBDMA_No,
            'Vellore_WBDMA_Cost': Vellore_WBDMA_Cost,
            'Vellore_total_no': Vellore_total_no,
            'Vellore_total_cost': Vellore_total_cost,
            'Tiruvannamalai_BT_RoadDMA_No': Tiruvannamalai_BT_RoadDMA_No,
            'Tiruvannamalai_BT_RoadDMA_Cost': Tiruvannamalai_BT_RoadDMA_Cost,
            'Tiruvannamalai_CC_RoadDMA_No': Tiruvannamalai_CC_RoadDMA_No,
            'Tiruvannamalai_CC_RoadDMA_Cost': Tiruvannamalai_CC_RoadDMA_Cost,
            'Tiruvannamalai_CrematoriumDMA_Cost': Tiruvannamalai_CrematoriumDMA_Cost,
            'Tiruvannamalai_CrematoriumDMA_No': Tiruvannamalai_CrematoriumDMA_No,
            'Tiruvannamalai_CulvertDMA_Cost': Tiruvannamalai_CulvertDMA_Cost,
            'Tiruvannamalai_CulvertDMA_No': Tiruvannamalai_CulvertDMA_No,
            'Tiruvannamalai_KnowledgeDMA_Centre_No': Tiruvannamalai_KnowledgeDMA_Centre_No,
            'Tiruvannamalai_KnowledgeDMA_Centre_Cost': Tiruvannamalai_KnowledgeDMA_Centre_Cost,
            'Tiruvannamalai_MarketDMA_No': Tiruvannamalai_MarketDMA_No,
            'Tiruvannamalai_MarketDMA_Cost': Tiruvannamalai_MarketDMA_Cost,
            'Tiruvannamalai_ParksDMA_No': Tiruvannamalai_ParksDMA_No,
            'Tiruvannamalai_ParksDMA_Cost': Tiruvannamalai_ParksDMA_Cost,
            'Tiruvannamalai_PaverBlockDMA_No': Tiruvannamalai_PaverBlockDMA_No,
            'Tiruvannamalai_PaverBlockDMA_Cost': Tiruvannamalai_PaverBlockDMA_Cost,
            'Tiruvannamalai_SWDDMA_No': Tiruvannamalai_SWDDMA_No,
            'Tiruvannamalai_SWDDMA_Cost': Tiruvannamalai_SWDDMA_Cost,
            'Tiruvannamalai_WBDMA_No': Tiruvannamalai_WBDMA_No,
            'Tiruvannamalai_WBDMA_Cost': Tiruvannamalai_WBDMA_Cost,
            'Tiruvannamalai_total_no': Tiruvannamalai_total_no,
            'Tiruvannamalai_total_cost': Tiruvannamalai_total_cost,
            'Tiruppur_BT_RoadDMA_No': Tiruppur_BT_RoadDMA_No,
            'Tiruppur_BT_RoadDMA_Cost': Tiruppur_BT_RoadDMA_Cost,
            'Tiruppur_CC_RoadDMA_No': Tiruppur_CC_RoadDMA_No,
            'Tiruppur_CC_RoadDMA_Cost': Tiruppur_CC_RoadDMA_Cost,
            'Tiruppur_CrematoriumDMA_Cost': Tiruppur_CrematoriumDMA_Cost,
            'Tiruppur_CrematoriumDMA_No': Tiruppur_CrematoriumDMA_No,
            'Tiruppur_CulvertDMA_Cost': Tiruppur_CulvertDMA_Cost,
            'Tiruppur_CulvertDMA_No': Tiruppur_CulvertDMA_No,
            'Tiruppur_KnowledgeDMA_Centre_No': Tiruppur_KnowledgeDMA_Centre_No,
            'Tiruppur_KnowledgeDMA_Centre_Cost': Tiruppur_KnowledgeDMA_Centre_Cost,
            'Tiruppur_MarketDMA_No': Tiruppur_MarketDMA_No,
            'Tiruppur_MarketDMA_Cost': Tiruppur_MarketDMA_Cost,
            'Tiruppur_ParksDMA_No': Tiruppur_ParksDMA_No,
            'Tiruppur_ParksDMA_Cost': Tiruppur_ParksDMA_Cost,
            'Tiruppur_PaverBlockDMA_No': Tiruppur_PaverBlockDMA_No,
            'Tiruppur_PaverBlockDMA_Cost': Tiruppur_PaverBlockDMA_Cost,
            'Tiruppur_SWDDMA_No': Tiruppur_SWDDMA_No,
            'Tiruppur_SWDDMA_Cost': Tiruppur_SWDDMA_Cost,
            'Tiruppur_WBDMA_No': Tiruppur_WBDMA_No,
            'Tiruppur_WBDMA_Cost': Tiruppur_WBDMA_Cost,
            'Tiruppur_total_no': Tiruppur_total_no,
            'Tiruppur_total_cost': Tiruppur_total_cost,
            'Tirupathur_BT_RoadDMA_No': Tirupathur_BT_RoadDMA_No,
            'Tirupathur_BT_RoadDMA_Cost': Tirupathur_BT_RoadDMA_Cost,
            'Tirupathur_CC_RoadDMA_No': Tirupathur_CC_RoadDMA_No,
            'Tirupathur_CC_RoadDMA_Cost': Tirupathur_CC_RoadDMA_Cost,
            'Tirupathur_CrematoriumDMA_Cost': Tirupathur_CrematoriumDMA_Cost,
            'Tirupathur_CrematoriumDMA_No': Tirupathur_CrematoriumDMA_No,
            'Tirupathur_CulvertDMA_Cost': Tirupathur_CulvertDMA_Cost,
            'Tirupathur_CulvertDMA_No': Tirupathur_CulvertDMA_No,
            'Tirupathur_KnowledgeDMA_Centre_No': Tirupathur_KnowledgeDMA_Centre_No,
            'Tirupathur_KnowledgeDMA_Centre_Cost': Tirupathur_KnowledgeDMA_Centre_Cost,
            'Tirupathur_MarketDMA_No': Tirupathur_MarketDMA_No,
            'Tirupathur_MarketDMA_Cost': Tirupathur_MarketDMA_Cost,
            'Tirupathur_ParksDMA_No': Tirupathur_ParksDMA_No,
            'Tirupathur_ParksDMA_Cost': Tirupathur_ParksDMA_Cost,
            'Tirupathur_PaverBlockDMA_No': Tirupathur_PaverBlockDMA_No,
            'Tirupathur_PaverBlockDMA_Cost': Tirupathur_PaverBlockDMA_Cost,
            'Tirupathur_SWDDMA_No': Tirupathur_SWDDMA_No,
            'Tirupathur_SWDDMA_Cost': Tirupathur_SWDDMA_Cost,
            'Tirupathur_WBDMA_No': Tirupathur_WBDMA_No,
            'Tirupathur_WBDMA_Cost': Tirupathur_WBDMA_Cost,
            'Tirupathur_total_no': Tirupathur_total_no,
            'Tirupathur_total_cost': Tirupathur_total_cost,
            'Tirunelveli_BT_RoadDMA_No': Tirunelveli_BT_RoadDMA_No,
            'Tirunelveli_BT_RoadDMA_Cost': Tirunelveli_BT_RoadDMA_Cost,
            'Tirunelveli_CC_RoadDMA_No': Tirunelveli_CC_RoadDMA_No,
            'Tirunelveli_CC_RoadDMA_Cost': Tirunelveli_CC_RoadDMA_Cost,
            'Tirunelveli_CrematoriumDMA_Cost': Tirunelveli_CrematoriumDMA_Cost,
            'Tirunelveli_CrematoriumDMA_No': Tirunelveli_CrematoriumDMA_No,
            'Tirunelveli_CulvertDMA_Cost': Tirunelveli_CulvertDMA_Cost,
            'Tirunelveli_CulvertDMA_No': Tirunelveli_CulvertDMA_No,
            'Tirunelveli_KnowledgeDMA_Centre_No': Tirunelveli_KnowledgeDMA_Centre_No,
            'Tirunelveli_KnowledgeDMA_Centre_Cost': Tirunelveli_KnowledgeDMA_Centre_Cost,
            'Tirunelveli_MarketDMA_No': Tirunelveli_MarketDMA_No,
            'Tirunelveli_MarketDMA_Cost': Tirunelveli_MarketDMA_Cost,
            'Tirunelveli_ParksDMA_No': Tirunelveli_ParksDMA_No,
            'Tirunelveli_ParksDMA_Cost': Tirunelveli_ParksDMA_Cost,
            'Tirunelveli_PaverBlockDMA_No': Tirunelveli_PaverBlockDMA_No,
            'Tirunelveli_PaverBlockDMA_Cost': Tirunelveli_PaverBlockDMA_Cost,
            'Tirunelveli_SWDDMA_No': Tirunelveli_SWDDMA_No,
            'Tirunelveli_SWDDMA_Cost': Tirunelveli_SWDDMA_Cost,
            'Tirunelveli_WBDMA_No': Tirunelveli_WBDMA_No,
            'Tirunelveli_WBDMA_Cost': Tirunelveli_WBDMA_Cost,
            'Tirunelveli_total_no': Tirunelveli_total_no,
            'Tirunelveli_total_cost': Tirunelveli_total_cost,
            'Tiruchirappalli_BT_RoadDMA_No': Tiruchirappalli_BT_RoadDMA_No,
            'Tiruchirappalli_BT_RoadDMA_Cost': Tiruchirappalli_BT_RoadDMA_Cost,
            'Tiruchirappalli_CC_RoadDMA_No': Tiruchirappalli_CC_RoadDMA_No,
            'Tiruchirappalli_CC_RoadDMA_Cost': Tiruchirappalli_CC_RoadDMA_Cost,
            'Tiruchirappalli_CrematoriumDMA_Cost': Tiruchirappalli_CrematoriumDMA_Cost,
            'Tiruchirappalli_CrematoriumDMA_No': Tiruchirappalli_CrematoriumDMA_No,
            'Tiruchirappalli_CulvertDMA_Cost': Tiruchirappalli_CulvertDMA_Cost,
            'Tiruchirappalli_CulvertDMA_No': Tiruchirappalli_CulvertDMA_No,
            'Tiruchirappalli_KnowledgeDMA_Centre_No': Tiruchirappalli_KnowledgeDMA_Centre_No,
            'Tiruchirappalli_KnowledgeDMA_Centre_Cost': Tiruchirappalli_KnowledgeDMA_Centre_Cost,
            'Tiruchirappalli_MarketDMA_No': Tiruchirappalli_MarketDMA_No,
            'Tiruchirappalli_MarketDMA_Cost': Tiruchirappalli_MarketDMA_Cost,
            'Tiruchirappalli_ParksDMA_No': Tiruchirappalli_ParksDMA_No,
            'Tiruchirappalli_ParksDMA_Cost': Tiruchirappalli_ParksDMA_Cost,
            'Tiruchirappalli_PaverBlockDMA_No': Tiruchirappalli_PaverBlockDMA_No,
            'Tiruchirappalli_PaverBlockDMA_Cost': Tiruchirappalli_PaverBlockDMA_Cost,
            'Tiruchirappalli_SWDDMA_No': Tiruchirappalli_SWDDMA_No,
            'Tiruchirappalli_SWDDMA_Cost': Tiruchirappalli_SWDDMA_Cost,
            'Tiruchirappalli_WBDMA_No': Tiruchirappalli_WBDMA_No,
            'Tiruchirappalli_WBDMA_Cost': Tiruchirappalli_WBDMA_Cost,
            'Tiruchirappalli_total_no': Tiruchirappalli_total_no,
            'Tiruchirappalli_total_cost': Tiruchirappalli_total_cost,
            'Thoothukudi_BT_RoadDMA_No': Thoothukudi_BT_RoadDMA_No,
            'Thoothukudi_BT_RoadDMA_Cost': Thoothukudi_BT_RoadDMA_Cost,
            'Thoothukudi_CC_RoadDMA_No': Thoothukudi_CC_RoadDMA_No,
            'Thoothukudi_CC_RoadDMA_Cost': Thoothukudi_CC_RoadDMA_Cost,
            'Thoothukudi_CrematoriumDMA_Cost': Thoothukudi_CrematoriumDMA_Cost,
            'Thoothukudi_CrematoriumDMA_No': Thoothukudi_CrematoriumDMA_No,
            'Thoothukudi_CulvertDMA_Cost': Thoothukudi_CulvertDMA_Cost,
            'Thoothukudi_CulvertDMA_No': Thoothukudi_CulvertDMA_No,
            'Thoothukudi_KnowledgeDMA_Centre_No': Thoothukudi_KnowledgeDMA_Centre_No,
            'Thoothukudi_KnowledgeDMA_Centre_Cost': Thoothukudi_KnowledgeDMA_Centre_Cost,
            'Thoothukudi_MarketDMA_No': Thoothukudi_MarketDMA_No,
            'Thoothukudi_MarketDMA_Cost': Thoothukudi_MarketDMA_Cost,
            'Thoothukudi_ParksDMA_No': Thoothukudi_ParksDMA_No,
            'Thoothukudi_ParksDMA_Cost': Thoothukudi_ParksDMA_Cost,
            'Thoothukudi_PaverBlockDMA_No': Thoothukudi_PaverBlockDMA_No,
            'Thoothukudi_PaverBlockDMA_Cost': Thoothukudi_PaverBlockDMA_Cost,
            'Thoothukudi_SWDDMA_No': Thoothukudi_SWDDMA_No,
            'Thoothukudi_SWDDMA_Cost': Thoothukudi_SWDDMA_Cost,
            'Thoothukudi_WBDMA_No': Thoothukudi_WBDMA_No,
            'Thoothukudi_WBDMA_Cost': Thoothukudi_WBDMA_Cost,
            'Thoothukudi_total_no': Thoothukudi_total_no,
            'Thoothukudi_total_cost': Thoothukudi_total_cost,
            'Thiruvarur_BT_RoadDMA_No': Thiruvarur_BT_RoadDMA_No,
            'Thiruvarur_BT_RoadDMA_Cost': Thiruvarur_BT_RoadDMA_Cost,
            'Thiruvarur_CC_RoadDMA_No': Thiruvarur_CC_RoadDMA_No,
            'Thiruvarur_CC_RoadDMA_Cost': Thiruvarur_CC_RoadDMA_Cost,
            'Thiruvarur_CrematoriumDMA_Cost': Thiruvarur_CrematoriumDMA_Cost,
            'Thiruvarur_CrematoriumDMA_No': Thiruvarur_CrematoriumDMA_No,
            'Thiruvarur_CulvertDMA_Cost': Thiruvarur_CulvertDMA_Cost,
            'Thiruvarur_CulvertDMA_No': Thiruvarur_CulvertDMA_No,
            'Thiruvarur_KnowledgeDMA_Centre_No': Thiruvarur_KnowledgeDMA_Centre_No,
            'Thiruvarur_KnowledgeDMA_Centre_Cost': Thiruvarur_KnowledgeDMA_Centre_Cost,
            'Thiruvarur_MarketDMA_No': Thiruvarur_MarketDMA_No,
            'Thiruvarur_MarketDMA_Cost': Thiruvarur_MarketDMA_Cost,
            'Thiruvarur_ParksDMA_No': Thiruvarur_ParksDMA_No,
            'Thiruvarur_ParksDMA_Cost': Thiruvarur_ParksDMA_Cost,
            'Thiruvarur_PaverBlockDMA_No': Thiruvarur_PaverBlockDMA_No,
            'Thiruvarur_PaverBlockDMA_Cost': Thiruvarur_PaverBlockDMA_Cost,
            'Thiruvarur_SWDDMA_No': Thiruvarur_SWDDMA_No,
            'Thiruvarur_SWDDMA_Cost': Thiruvarur_SWDDMA_Cost,
            'Thiruvarur_WBDMA_No': Thiruvarur_WBDMA_No,
            'Thiruvarur_WBDMA_Cost': Thiruvarur_WBDMA_Cost,
            'Thiruvarur_total_no': Thiruvarur_total_no,
            'Thiruvarur_total_cost': Thiruvarur_total_cost,
            'Thiruvallur_BT_RoadDMA_No': Thiruvallur_BT_RoadDMA_No,
            'Thiruvallur_BT_RoadDMA_Cost': Thiruvallur_BT_RoadDMA_Cost,
            'Thiruvallur_CC_RoadDMA_No': Thiruvallur_CC_RoadDMA_No,
            'Thiruvallur_CC_RoadDMA_Cost': Thiruvallur_CC_RoadDMA_Cost,
            'Thiruvallur_CrematoriumDMA_Cost': Thiruvallur_CrematoriumDMA_Cost,
            'Thiruvallur_CrematoriumDMA_No': Thiruvallur_CrematoriumDMA_No,
            'Thiruvallur_CulvertDMA_Cost': Thiruvallur_CulvertDMA_Cost,
            'Thiruvallur_CulvertDMA_No': Thiruvallur_CulvertDMA_No,
            'Thiruvallur_KnowledgeDMA_Centre_No': Thiruvallur_KnowledgeDMA_Centre_No,
            'Thiruvallur_KnowledgeDMA_Centre_Cost': Thiruvallur_KnowledgeDMA_Centre_Cost,
            'Thiruvallur_MarketDMA_No': Thiruvallur_MarketDMA_No,
            'Thiruvallur_MarketDMA_Cost': Thiruvallur_MarketDMA_Cost,
            'Thiruvallur_ParksDMA_No': Thiruvallur_ParksDMA_No,
            'Thiruvallur_ParksDMA_Cost': Thiruvallur_ParksDMA_Cost,
            'Thiruvallur_PaverBlockDMA_No': Thiruvallur_PaverBlockDMA_No,
            'Thiruvallur_PaverBlockDMA_Cost': Thiruvallur_PaverBlockDMA_Cost,
            'Thiruvallur_SWDDMA_No': Thiruvallur_SWDDMA_No,
            'Thiruvallur_SWDDMA_Cost': Thiruvallur_SWDDMA_Cost,
            'Thiruvallur_WBDMA_No': Thiruvallur_WBDMA_No,
            'Thiruvallur_WBDMA_Cost': Thiruvallur_WBDMA_Cost,
            'Thiruvallur_total_no': Thiruvallur_total_no,
            'Thiruvallur_total_cost': Thiruvallur_total_cost,
            'Theni_BT_RoadDMA_No': Theni_BT_RoadDMA_No,
            'Theni_BT_RoadDMA_Cost': Theni_BT_RoadDMA_Cost,
            'Theni_CC_RoadDMA_No': Theni_CC_RoadDMA_No,
            'Theni_CC_RoadDMA_Cost': Theni_CC_RoadDMA_Cost,
            'Theni_CrematoriumDMA_Cost': Theni_CrematoriumDMA_Cost,
            'Theni_CrematoriumDMA_No': Theni_CrematoriumDMA_No,
            'Theni_CulvertDMA_Cost': Theni_CulvertDMA_Cost,
            'Theni_CulvertDMA_No': Theni_CulvertDMA_No,
            'Theni_KnowledgeDMA_Centre_No': Theni_KnowledgeDMA_Centre_No,
            'Theni_KnowledgeDMA_Centre_Cost': Theni_KnowledgeDMA_Centre_Cost,
            'Theni_MarketDMA_No': Theni_MarketDMA_No,
            'Theni_MarketDMA_Cost': Theni_MarketDMA_Cost,
            'Theni_ParksDMA_No': Theni_ParksDMA_No,
            'Theni_ParksDMA_Cost': Theni_ParksDMA_Cost,
            'Theni_PaverBlockDMA_No': Theni_PaverBlockDMA_No,
            'Theni_PaverBlockDMA_Cost': Theni_PaverBlockDMA_Cost,
            'Theni_SWDDMA_No': Theni_SWDDMA_No,
            'Theni_SWDDMA_Cost': Theni_SWDDMA_Cost,
            'Theni_WBDMA_No': Theni_WBDMA_No,
            'Theni_WBDMA_Cost': Theni_WBDMA_Cost,
            'Theni_total_no': Theni_total_no,
            'Theni_total_cost': Theni_total_cost,
            'Thanjavur_BT_RoadDMA_No': Thanjavur_BT_RoadDMA_No,
            'Thanjavur_BT_RoadDMA_Cost': Thanjavur_BT_RoadDMA_Cost,
            'Thanjavur_CC_RoadDMA_No': Thanjavur_CC_RoadDMA_No,
            'Thanjavur_CC_RoadDMA_Cost': Thanjavur_CC_RoadDMA_Cost,
            'Thanjavur_CrematoriumDMA_Cost': Thanjavur_CrematoriumDMA_Cost,
            'Thanjavur_CrematoriumDMA_No': Thanjavur_CrematoriumDMA_No,
            'Thanjavur_CulvertDMA_Cost': Thanjavur_CulvertDMA_Cost,
            'Thanjavur_CulvertDMA_No': Thanjavur_CulvertDMA_No,
            'Thanjavur_KnowledgeDMA_Centre_No': Thanjavur_KnowledgeDMA_Centre_No,
            'Thanjavur_KnowledgeDMA_Centre_Cost': Thanjavur_KnowledgeDMA_Centre_Cost,
            'Thanjavur_MarketDMA_No': Thanjavur_MarketDMA_No,
            'Thanjavur_MarketDMA_Cost': Thanjavur_MarketDMA_Cost,
            'Thanjavur_ParksDMA_No': Thanjavur_ParksDMA_No,
            'Thanjavur_ParksDMA_Cost': Thanjavur_ParksDMA_Cost,
            'Thanjavur_PaverBlockDMA_No': Thanjavur_PaverBlockDMA_No,
            'Thanjavur_PaverBlockDMA_Cost': Thanjavur_PaverBlockDMA_Cost,
            'Thanjavur_SWDDMA_No': Thanjavur_SWDDMA_No,
            'Thanjavur_SWDDMA_Cost': Thanjavur_SWDDMA_Cost,
            'Thanjavur_WBDMA_No': Thanjavur_WBDMA_No,
            'Thanjavur_WBDMA_Cost': Thanjavur_WBDMA_Cost,
            'Thanjavur_total_no': Thanjavur_total_no,
            'Thanjavur_total_cost': Thanjavur_total_cost,

            'Tenkasi_BT_RoadDMA_No': Tenkasi_BT_RoadDMA_No,
            'Tenkasi_BT_RoadDMA_Cost': Tenkasi_BT_RoadDMA_Cost,
            'Tenkasi_CC_RoadDMA_No': Tenkasi_CC_RoadDMA_No,
            'Tenkasi_CC_RoadDMA_Cost': Tenkasi_CC_RoadDMA_Cost,
            'Tenkasi_CrematoriumDMA_Cost': Tenkasi_CrematoriumDMA_Cost,
            'Tenkasi_CrematoriumDMA_No': Tenkasi_CrematoriumDMA_No,
            'Tenkasi_CulvertDMA_Cost': Tenkasi_CulvertDMA_Cost,
            'Tenkasi_CulvertDMA_No': Tenkasi_CulvertDMA_No,
            'Tenkasi_KnowledgeDMA_Centre_No': Tenkasi_KnowledgeDMA_Centre_No,
            'Tenkasi_KnowledgeDMA_Centre_Cost': Tenkasi_KnowledgeDMA_Centre_Cost,
            'Tenkasi_MarketDMA_No': Tenkasi_MarketDMA_No,
            'Tenkasi_MarketDMA_Cost': Tenkasi_MarketDMA_Cost,
            'Tenkasi_ParksDMA_No': Tenkasi_ParksDMA_No,
            'Tenkasi_ParksDMA_Cost': Tenkasi_ParksDMA_Cost,
            'Tenkasi_PaverBlockDMA_No': Tenkasi_PaverBlockDMA_No,
            'Tenkasi_PaverBlockDMA_Cost': Tenkasi_PaverBlockDMA_Cost,
            'Tenkasi_SWDDMA_No': Tenkasi_SWDDMA_No,
            'Tenkasi_SWDDMA_Cost': Tenkasi_SWDDMA_Cost,
            'Tenkasi_WBDMA_No': Tenkasi_WBDMA_No,
            'Tenkasi_WBDMA_Cost': Tenkasi_WBDMA_Cost,
            'Tenkasi_total_no': Tenkasi_total_no,
            'Tenkasi_total_cost': Tenkasi_total_cost,
            'Sivagangai_BT_RoadDMA_No': Sivagangai_BT_RoadDMA_No,
            'Sivagangai_BT_RoadDMA_Cost': Sivagangai_BT_RoadDMA_Cost,
            'Sivagangai_CC_RoadDMA_No': Sivagangai_CC_RoadDMA_No,
            'Sivagangai_CC_RoadDMA_Cost': Sivagangai_CC_RoadDMA_Cost,
            'Sivagangai_CrematoriumDMA_Cost': Sivagangai_CrematoriumDMA_Cost,
            'Sivagangai_CrematoriumDMA_No': Sivagangai_CrematoriumDMA_No,
            'Sivagangai_CulvertDMA_Cost': Sivagangai_CulvertDMA_Cost,
            'Sivagangai_CulvertDMA_No': Sivagangai_CulvertDMA_No,
            'Sivagangai_KnowledgeDMA_Centre_No': Sivagangai_KnowledgeDMA_Centre_No,
            'Sivagangai_KnowledgeDMA_Centre_Cost': Sivagangai_KnowledgeDMA_Centre_Cost,
            'Sivagangai_MarketDMA_No': Sivagangai_MarketDMA_No,
            'Sivagangai_MarketDMA_Cost': Sivagangai_MarketDMA_Cost,
            'Sivagangai_ParksDMA_No': Sivagangai_ParksDMA_No,
            'Sivagangai_ParksDMA_Cost': Sivagangai_ParksDMA_Cost,
            'Sivagangai_PaverBlockDMA_No': Sivagangai_PaverBlockDMA_No,
            'Sivagangai_PaverBlockDMA_Cost': Sivagangai_PaverBlockDMA_Cost,
            'Sivagangai_SWDDMA_No': Sivagangai_SWDDMA_No,
            'Sivagangai_SWDDMA_Cost': Sivagangai_SWDDMA_Cost,
            'Sivagangai_WBDMA_No': Sivagangai_WBDMA_No,
            'Sivagangai_WBDMA_Cost': Sivagangai_WBDMA_Cost,
            'Sivagangai_total_no': Sivagangai_total_no,
            'Sivagangai_total_cost': Sivagangai_total_cost,
            'Salem_BT_RoadDMA_No': Salem_BT_RoadDMA_No,
            'Salem_BT_RoadDMA_Cost': Salem_BT_RoadDMA_Cost,
            'Salem_CC_RoadDMA_No': Salem_CC_RoadDMA_No,
            'Salem_CC_RoadDMA_Cost': Salem_CC_RoadDMA_Cost,
            'Salem_CrematoriumDMA_Cost': Salem_CrematoriumDMA_Cost,
            'Salem_CrematoriumDMA_No': Salem_CrematoriumDMA_No,
            'Salem_CulvertDMA_Cost': Salem_CulvertDMA_Cost,
            'Salem_CulvertDMA_No': Salem_CulvertDMA_No,
            'Salem_KnowledgeDMA_Centre_No': Salem_KnowledgeDMA_Centre_No,
            'Salem_KnowledgeDMA_Centre_Cost': Salem_KnowledgeDMA_Centre_Cost,
            'Salem_MarketDMA_No': Salem_MarketDMA_No,
            'Salem_MarketDMA_Cost': Salem_MarketDMA_Cost,
            'Salem_ParksDMA_No': Salem_ParksDMA_No,
            'Salem_ParksDMA_Cost': Salem_ParksDMA_Cost,
            'Salem_PaverBlockDMA_No': Salem_PaverBlockDMA_No,
            'Salem_PaverBlockDMA_Cost': Salem_PaverBlockDMA_Cost,
            'Salem_SWDDMA_No': Salem_SWDDMA_No,
            'Salem_SWDDMA_Cost': Salem_SWDDMA_Cost,
            'Salem_WBDMA_No': Salem_WBDMA_No,
            'Salem_WBDMA_Cost': Salem_WBDMA_Cost,
            'Salem_total_no': Salem_total_no,
            'Salem_total_cost': Salem_total_cost,
            'Ranipet_BT_RoadDMA_No': Ranipet_BT_RoadDMA_No,
            'Ranipet_BT_RoadDMA_Cost': Ranipet_BT_RoadDMA_Cost,
            'Ranipet_CC_RoadDMA_No': Ranipet_CC_RoadDMA_No,
            'Ranipet_CC_RoadDMA_Cost': Ranipet_CC_RoadDMA_Cost,
            'Ranipet_CrematoriumDMA_Cost': Ranipet_CrematoriumDMA_Cost,
            'Ranipet_CrematoriumDMA_No': Ranipet_CrematoriumDMA_No,
            'Ranipet_CulvertDMA_Cost': Ranipet_CulvertDMA_Cost,
            'Ranipet_CulvertDMA_No': Ranipet_CulvertDMA_No,
            'Ranipet_KnowledgeDMA_Centre_No': Ranipet_KnowledgeDMA_Centre_No,
            'Ranipet_KnowledgeDMA_Centre_Cost': Ranipet_KnowledgeDMA_Centre_Cost,
            'Ranipet_MarketDMA_No': Ranipet_MarketDMA_No,
            'Ranipet_MarketDMA_Cost': Ranipet_MarketDMA_Cost,
            'Ranipet_ParksDMA_No': Ranipet_ParksDMA_No,
            'Ranipet_ParksDMA_Cost': Ranipet_ParksDMA_Cost,
            'Ranipet_PaverBlockDMA_No': Ranipet_PaverBlockDMA_No,
            'Ranipet_PaverBlockDMA_Cost': Ranipet_PaverBlockDMA_Cost,
            'Ranipet_SWDDMA_No': Ranipet_SWDDMA_No,
            'Ranipet_SWDDMA_Cost': Ranipet_SWDDMA_Cost,
            'Ranipet_WBDMA_No': Ranipet_WBDMA_No,
            'Ranipet_WBDMA_Cost': Ranipet_WBDMA_Cost,
            'Ranipet_total_no': Ranipet_total_no,
            'Ranipet_total_cost': Ranipet_total_cost,
            'Ramanathapuram_BT_RoadDMA_No': Ramanathapuram_BT_RoadDMA_No,
            'Ramanathapuram_BT_RoadDMA_Cost': Ramanathapuram_BT_RoadDMA_Cost,
            'Ramanathapuram_CC_RoadDMA_No': Ramanathapuram_CC_RoadDMA_No,
            'Ramanathapuram_CC_RoadDMA_Cost': Ramanathapuram_CC_RoadDMA_Cost,
            'Ramanathapuram_CrematoriumDMA_Cost': Ramanathapuram_CrematoriumDMA_Cost,
            'Ramanathapuram_CrematoriumDMA_No': Ramanathapuram_CrematoriumDMA_No,
            'Ramanathapuram_CulvertDMA_Cost': Ramanathapuram_CulvertDMA_Cost,
            'Ramanathapuram_CulvertDMA_No': Ramanathapuram_CulvertDMA_No,
            'Ramanathapuram_KnowledgeDMA_Centre_No': Ramanathapuram_KnowledgeDMA_Centre_No,
            'Ramanathapuram_KnowledgeDMA_Centre_Cost': Ramanathapuram_KnowledgeDMA_Centre_Cost,
            'Ramanathapuram_MarketDMA_No': Ramanathapuram_MarketDMA_No,
            'Ramanathapuram_MarketDMA_Cost': Ramanathapuram_MarketDMA_Cost,
            'Ramanathapuram_ParksDMA_No': Ramanathapuram_ParksDMA_No,
            'Ramanathapuram_ParksDMA_Cost': Ramanathapuram_ParksDMA_Cost,
            'Ramanathapuram_PaverBlockDMA_No': Ramanathapuram_PaverBlockDMA_No,
            'Ramanathapuram_PaverBlockDMA_Cost': Ramanathapuram_PaverBlockDMA_Cost,
            'Ramanathapuram_SWDDMA_No': Ramanathapuram_SWDDMA_No,
            'Ramanathapuram_SWDDMA_Cost': Ramanathapuram_SWDDMA_Cost,
            'Ramanathapuram_WBDMA_No': Ramanathapuram_WBDMA_No,
            'Ramanathapuram_WBDMA_Cost': Ramanathapuram_WBDMA_Cost,
            'Ramanathapuram_total_no': Ramanathapuram_total_no,
            'Ramanathapuram_total_cost': Ramanathapuram_total_cost,
            'Pudukottai_BT_RoadDMA_No': Pudukottai_BT_RoadDMA_No,
            'Pudukottai_BT_RoadDMA_Cost': Pudukottai_BT_RoadDMA_Cost,
            'Pudukottai_CC_RoadDMA_No': Pudukottai_CC_RoadDMA_No,
            'Pudukottai_CC_RoadDMA_Cost': Pudukottai_CC_RoadDMA_Cost,
            'Pudukottai_CrematoriumDMA_Cost': Pudukottai_CrematoriumDMA_Cost,
            'Pudukottai_CrematoriumDMA_No': Pudukottai_CrematoriumDMA_No,
            'Pudukottai_CulvertDMA_Cost': Pudukottai_CulvertDMA_Cost,
            'Pudukottai_CulvertDMA_No': Pudukottai_CulvertDMA_No,
            'Pudukottai_KnowledgeDMA_Centre_No': Pudukottai_KnowledgeDMA_Centre_No,
            'Pudukottai_KnowledgeDMA_Centre_Cost': Pudukottai_KnowledgeDMA_Centre_Cost,
            'Pudukottai_MarketDMA_No': Pudukottai_MarketDMA_No,
            'Pudukottai_MarketDMA_Cost': Pudukottai_MarketDMA_Cost,
            'Pudukottai_ParksDMA_No': Pudukottai_ParksDMA_No,
            'Pudukottai_ParksDMA_Cost': Pudukottai_ParksDMA_Cost,
            'Pudukottai_PaverBlockDMA_No': Pudukottai_PaverBlockDMA_No,
            'Pudukottai_PaverBlockDMA_Cost': Pudukottai_PaverBlockDMA_Cost,
            'Pudukottai_SWDDMA_No': Pudukottai_SWDDMA_No,
            'Pudukottai_SWDDMA_Cost': Pudukottai_SWDDMA_Cost,
            'Pudukottai_WBDMA_No': Pudukottai_WBDMA_No,
            'Pudukottai_WBDMA_Cost': Pudukottai_WBDMA_Cost,
            'Pudukottai_total_no': Pudukottai_total_no,
            'Pudukottai_total_cost': Pudukottai_total_cost,
            'Perambalur_BT_RoadDMA_No': Perambalur_BT_RoadDMA_No,
            'Perambalur_BT_RoadDMA_Cost': Perambalur_BT_RoadDMA_Cost,
            'Perambalur_CC_RoadDMA_No': Perambalur_CC_RoadDMA_No,
            'Perambalur_CC_RoadDMA_Cost': Perambalur_CC_RoadDMA_Cost,
            'Perambalur_CrematoriumDMA_Cost': Perambalur_CrematoriumDMA_Cost,
            'Perambalur_CrematoriumDMA_No': Perambalur_CrematoriumDMA_No,
            'Perambalur_CulvertDMA_Cost': Perambalur_CulvertDMA_Cost,
            'Perambalur_CulvertDMA_No': Perambalur_CulvertDMA_No,
            'Perambalur_KnowledgeDMA_Centre_No': Perambalur_KnowledgeDMA_Centre_No,
            'Perambalur_KnowledgeDMA_Centre_Cost': Perambalur_KnowledgeDMA_Centre_Cost,
            'Perambalur_MarketDMA_No': Perambalur_MarketDMA_No,
            'Perambalur_MarketDMA_Cost': Perambalur_MarketDMA_Cost,
            'Perambalur_ParksDMA_No': Perambalur_ParksDMA_No,
            'Perambalur_ParksDMA_Cost': Perambalur_ParksDMA_Cost,
            'Perambalur_PaverBlockDMA_No': Perambalur_PaverBlockDMA_No,
            'Perambalur_PaverBlockDMA_Cost': Perambalur_PaverBlockDMA_Cost,
            'Perambalur_SWDDMA_No': Perambalur_SWDDMA_No,
            'Perambalur_SWDDMA_Cost': Perambalur_SWDDMA_Cost,
            'Perambalur_WBDMA_No': Perambalur_WBDMA_No,
            'Perambalur_WBDMA_Cost': Perambalur_WBDMA_Cost,
            'Perambalur_total_no': Perambalur_total_no,
            'Perambalur_total_cost': Perambalur_total_cost,
            'ariyalur_BT_RoadDMA_No': ariyalur_BT_RoadDMA_No,
            'ariyalur_BT_RoadDMA_Cost': ariyalur_BT_RoadDMA_Cost,
            'ariyalur_CC_RoadDMA_No': ariyalur_CC_RoadDMA_No,
            'ariyalur_CC_RoadDMA_Cost': ariyalur_CC_RoadDMA_Cost,
            'ariyalur_CrematoriumDMA_Cost': ariyalur_CrematoriumDMA_Cost,
            'ariyalur_CrematoriumDMA_No': ariyalur_CrematoriumDMA_No,
            'ariyalur_CulvertDMA_Cost': ariyalur_CulvertDMA_Cost,
            'ariyalur_CulvertDMA_No': ariyalur_CulvertDMA_No,
            'ariyalur_KnowledgeDMA_Centre_No': ariyalur_KnowledgeDMA_Centre_No,
            'ariyalur_KnowledgeDMA_Centre_Cost': ariyalur_KnowledgeDMA_Centre_Cost,
            'ariyalur_MarketDMA_No': ariyalur_MarketDMA_No,
            'ariyalur_MarketDMA_Cost': ariyalur_MarketDMA_Cost,
            'ariyalur_ParksDMA_No': ariyalur_ParksDMA_No,
            'ariyalur_ParksDMA_Cost': ariyalur_ParksDMA_Cost,
            'ariyalur_PaverBlockDMA_No': ariyalur_PaverBlockDMA_No,
            'ariyalur_PaverBlockDMA_Cost': ariyalur_PaverBlockDMA_Cost,
            'ariyalur_SWDDMA_No': ariyalur_SWDDMA_No,
            'ariyalur_SWDDMA_Cost': ariyalur_SWDDMA_Cost,
            'ariyalur_WBDMA_No': ariyalur_WBDMA_No,
            'ariyalur_WBDMA_Cost': ariyalur_WBDMA_Cost,
            'ariyalur_total_no': ariyalur_total_no,
            'ariyalur_total_cost': ariyalur_total_cost,
            'Chengalpattu_BT_RoadDMA_No': Chengalpattu_BT_RoadDMA_No,
            'Chengalpattu_BT_RoadDMA_Cost': Chengalpattu_BT_RoadDMA_Cost,
            'Chengalpattu_CC_RoadDMA_No': Chengalpattu_CC_RoadDMA_No,
            'Chengalpattu_CC_RoadDMA_Cost': Chengalpattu_CC_RoadDMA_Cost,
            'Chengalpattu_CrematoriumDMA_Cost': Chengalpattu_CrematoriumDMA_Cost,
            'Chengalpattu_CrematoriumDMA_No': Chengalpattu_CrematoriumDMA_No,
            'Chengalpattu_CulvertDMA_Cost': Chengalpattu_CulvertDMA_Cost,
            'Chengalpattu_CulvertDMA_No': Chengalpattu_CulvertDMA_No,
            'Chengalpattu_KnowledgeDMA_Centre_No': Chengalpattu_KnowledgeDMA_Centre_No,
            'Chengalpattu_KnowledgeDMA_Centre_Cost': Chengalpattu_KnowledgeDMA_Centre_Cost,
            'Chengalpattu_MarketDMA_No': Chengalpattu_MarketDMA_No,
            'Chengalpattu_MarketDMA_Cost': Chengalpattu_MarketDMA_Cost,
            'Chengalpattu_ParksDMA_No': Chengalpattu_ParksDMA_No,
            'Chengalpattu_ParksDMA_Cost': Chengalpattu_ParksDMA_Cost,
            'Chengalpattu_PaverBlockDMA_No': Chengalpattu_PaverBlockDMA_No,
            'Chengalpattu_PaverBlockDMA_Cost': Chengalpattu_PaverBlockDMA_Cost,
            'Chengalpattu_SWDDMA_No': Chengalpattu_SWDDMA_No,
            'Chengalpattu_SWDDMA_Cost': Chengalpattu_SWDDMA_Cost,
            'Chengalpattu_WBDMA_No': Chengalpattu_WBDMA_No,
            'Chengalpattu_WBDMA_Cost': Chengalpattu_WBDMA_Cost,
            'Chengalpattu_total_no': Chengalpattu_total_no,
            'Chengalpattu_total_cost': Chengalpattu_total_cost,
            'Coimbatore_BT_RoadDMA_No': Coimbatore_BT_RoadDMA_No,
            'Coimbatore_BT_RoadDMA_Cost': Coimbatore_BT_RoadDMA_Cost,
            'Coimbatore_CC_RoadDMA_No': Coimbatore_CC_RoadDMA_No,
            'Coimbatore_CC_RoadDMA_Cost': Coimbatore_CC_RoadDMA_Cost,
            'Coimbatore_CrematoriumDMA_Cost': Coimbatore_CrematoriumDMA_Cost,
            'Coimbatore_CrematoriumDMA_No': Coimbatore_CrematoriumDMA_No,
            'Coimbatore_CulvertDMA_Cost': Coimbatore_CulvertDMA_Cost,
            'Coimbatore_CulvertDMA_No': Coimbatore_CulvertDMA_No,
            'Coimbatore_KnowledgeDMA_Centre_No': Coimbatore_KnowledgeDMA_Centre_No,
            'Coimbatore_KnowledgeDMA_Centre_Cost': Coimbatore_KnowledgeDMA_Centre_Cost,
            'Coimbatore_MarketDMA_No': Coimbatore_MarketDMA_No,
            'Coimbatore_MarketDMA_Cost': Coimbatore_MarketDMA_Cost,
            'Coimbatore_ParksDMA_No': Coimbatore_ParksDMA_No,
            'Coimbatore_ParksDMA_Cost': Coimbatore_ParksDMA_Cost,
            'Coimbatore_PaverBlockDMA_No': Coimbatore_PaverBlockDMA_No,
            'Coimbatore_PaverBlockDMA_Cost': Coimbatore_PaverBlockDMA_Cost,
            'Coimbatore_SWDDMA_No': Coimbatore_SWDDMA_No,
            'Coimbatore_SWDDMA_Cost': Coimbatore_SWDDMA_Cost,
            'Coimbatore_WBDMA_No': Coimbatore_WBDMA_No,
            'Coimbatore_WBDMA_Cost': Coimbatore_WBDMA_Cost,
            'Coimbatore_total_no': Coimbatore_total_no,
            'Coimbatore_total_cost': Coimbatore_total_cost,

            'Cuddalore_BT_RoadDMA_No': Cuddalore_BT_RoadDMA_No,
            'Cuddalore_BT_RoadDMA_Cost': Cuddalore_BT_RoadDMA_Cost,
            'Cuddalore_CC_RoadDMA_No': Cuddalore_CC_RoadDMA_No,
            'Cuddalore_CC_RoadDMA_Cost': Cuddalore_CC_RoadDMA_Cost,
            'Cuddalore_CrematoriumDMA_Cost': Cuddalore_CrematoriumDMA_Cost,
            'Cuddalore_CrematoriumDMA_No': Cuddalore_CrematoriumDMA_No,
            'Cuddalore_CulvertDMA_Cost': Cuddalore_CulvertDMA_Cost,
            'Cuddalore_CulvertDMA_No': Cuddalore_CulvertDMA_No,
            'Cuddalore_KnowledgeDMA_Centre_No': Cuddalore_KnowledgeDMA_Centre_No,
            'Cuddalore_KnowledgeDMA_Centre_Cost': Cuddalore_KnowledgeDMA_Centre_Cost,
            'Cuddalore_MarketDMA_No': Cuddalore_MarketDMA_No,
            'Cuddalore_MarketDMA_Cost': Cuddalore_MarketDMA_Cost,
            'Cuddalore_ParksDMA_No': Cuddalore_ParksDMA_No,
            'Cuddalore_ParksDMA_Cost': Cuddalore_ParksDMA_Cost,
            'Cuddalore_PaverBlockDMA_No': Cuddalore_PaverBlockDMA_No,
            'Cuddalore_PaverBlockDMA_Cost': Cuddalore_PaverBlockDMA_Cost,
            'Cuddalore_SWDDMA_No': Cuddalore_SWDDMA_No,
            'Cuddalore_SWDDMA_Cost': Cuddalore_SWDDMA_Cost,
            'Cuddalore_WBDMA_No': Cuddalore_WBDMA_No,
            'Cuddalore_WBDMA_Cost': Cuddalore_WBDMA_Cost,
            'Cuddalore_total_no': Cuddalore_total_no,
            'Cuddalore_total_cost': Cuddalore_total_cost,

            'Dharmapuri_BT_RoadDMA_No': Dharmapuri_BT_RoadDMA_No,
            'Dharmapuri_BT_RoadDMA_Cost': Dharmapuri_BT_RoadDMA_Cost,
            'Dharmapuri_CC_RoadDMA_No': Dharmapuri_CC_RoadDMA_No,
            'Dharmapuri_CC_RoadDMA_Cost': Dharmapuri_CC_RoadDMA_Cost,
            'Dharmapuri_CrematoriumDMA_Cost': Dharmapuri_CrematoriumDMA_Cost,
            'Dharmapuri_CrematoriumDMA_No': Dharmapuri_CrematoriumDMA_No,
            'Dharmapuri_CulvertDMA_Cost': Dharmapuri_CulvertDMA_Cost,
            'Dharmapuri_CulvertDMA_No': Dharmapuri_CulvertDMA_No,
            'Dharmapuri_KnowledgeDMA_Centre_No': Dharmapuri_KnowledgeDMA_Centre_No,
            'Dharmapuri_KnowledgeDMA_Centre_Cost': Dharmapuri_KnowledgeDMA_Centre_Cost,
            'Dharmapuri_MarketDMA_No': Dharmapuri_MarketDMA_No,
            'Dharmapuri_MarketDMA_Cost': Dharmapuri_MarketDMA_Cost,
            'Dharmapuri_ParksDMA_No': Dharmapuri_ParksDMA_No,
            'Dharmapuri_ParksDMA_Cost': Dharmapuri_ParksDMA_Cost,
            'Dharmapuri_PaverBlockDMA_No': Dharmapuri_PaverBlockDMA_No,
            'Dharmapuri_PaverBlockDMA_Cost': Dharmapuri_PaverBlockDMA_Cost,
            'Dharmapuri_SWDDMA_No': Dharmapuri_SWDDMA_No,
            'Dharmapuri_SWDDMA_Cost': Dharmapuri_SWDDMA_Cost,
            'Dharmapuri_WBDMA_No': Dharmapuri_WBDMA_No,
            'Dharmapuri_WBDMA_Cost': Dharmapuri_WBDMA_Cost,
            'Dharmapuri_total_no': Dharmapuri_total_no,
            'Dharmapuri_total_cost': Dharmapuri_total_cost,

            'Dindigul_BT_RoadDMA_No': Dindigul_BT_RoadDMA_No,
            'Dindigul_BT_RoadDMA_Cost': Dindigul_BT_RoadDMA_Cost,
            'Dindigul_CC_RoadDMA_No': Dindigul_CC_RoadDMA_No,
            'Dindigul_CC_RoadDMA_Cost': Dindigul_CC_RoadDMA_Cost,
            'Dindigul_CrematoriumDMA_Cost': Dindigul_CrematoriumDMA_Cost,
            'Dindigul_CrematoriumDMA_No': Dindigul_CrematoriumDMA_No,
            'Dindigul_CulvertDMA_Cost': Dindigul_CulvertDMA_Cost,
            'Dindigul_CulvertDMA_No': Dindigul_CulvertDMA_No,
            'Dindigul_KnowledgeDMA_Centre_No': Dindigul_KnowledgeDMA_Centre_No,
            'Dindigul_KnowledgeDMA_Centre_Cost': Dindigul_KnowledgeDMA_Centre_Cost,
            'Dindigul_MarketDMA_No': Dindigul_MarketDMA_No,
            'Dindigul_MarketDMA_Cost': Dindigul_MarketDMA_Cost,
            'Dindigul_ParksDMA_No': Dindigul_ParksDMA_No,
            'Dindigul_ParksDMA_Cost': Dindigul_ParksDMA_Cost,
            'Dindigul_PaverBlockDMA_No': Dindigul_PaverBlockDMA_No,
            'Dindigul_PaverBlockDMA_Cost': Dindigul_PaverBlockDMA_Cost,
            'Dindigul_SWDDMA_No': Dindigul_SWDDMA_No,
            'Dindigul_SWDDMA_Cost': Dindigul_SWDDMA_Cost,
            'Dindigul_WBDMA_No': Dindigul_WBDMA_No,
            'Dindigul_WBDMA_Cost': Dindigul_WBDMA_Cost,
            'Dindigul_total_no': Dindigul_total_no,
            'Dindigul_total_cost': Dindigul_total_cost,

            'Erode_BT_RoadDMA_No': Erode_BT_RoadDMA_No,
            'Erode_BT_RoadDMA_Cost': Erode_BT_RoadDMA_Cost,
            'Erode_CC_RoadDMA_No': Erode_CC_RoadDMA_No,
            'Erode_CC_RoadDMA_Cost': Erode_CC_RoadDMA_Cost,
            'Erode_CrematoriumDMA_Cost': Erode_CrematoriumDMA_Cost,
            'Erode_CrematoriumDMA_No': Erode_CrematoriumDMA_No,
            'Erode_CulvertDMA_Cost': Erode_CulvertDMA_Cost,
            'Erode_CulvertDMA_No': Erode_CulvertDMA_No,
            'Erode_KnowledgeDMA_Centre_No': Erode_KnowledgeDMA_Centre_No,
            'Erode_KnowledgeDMA_Centre_Cost': Erode_KnowledgeDMA_Centre_Cost,
            'Erode_MarketDMA_No': Erode_MarketDMA_No,
            'Erode_MarketDMA_Cost': Erode_MarketDMA_Cost,
            'Erode_ParksDMA_No': Erode_ParksDMA_No,
            'Erode_ParksDMA_Cost': Erode_ParksDMA_Cost,
            'Erode_PaverBlockDMA_No': Erode_PaverBlockDMA_No,
            'Erode_PaverBlockDMA_Cost': Erode_PaverBlockDMA_Cost,
            'Erode_SWDDMA_No': Erode_SWDDMA_No,
            'Erode_SWDDMA_Cost': Erode_SWDDMA_Cost,
            'Erode_WBDMA_No': Erode_WBDMA_No,
            'Erode_WBDMA_Cost': Erode_WBDMA_Cost,
            'Erode_total_no': Erode_total_no,
            'Erode_total_cost': Erode_total_cost,

            'Kallakurichi_BT_RoadDMA_No': Kallakurichi_BT_RoadDMA_No,
            'Kallakurichi_BT_RoadDMA_Cost': Kallakurichi_BT_RoadDMA_Cost,
            'Kallakurichi_CC_RoadDMA_No': Kallakurichi_CC_RoadDMA_No,
            'Kallakurichi_CC_RoadDMA_Cost': Kallakurichi_CC_RoadDMA_Cost,
            'Kallakurichi_CrematoriumDMA_Cost': Kallakurichi_CrematoriumDMA_Cost,
            'Kallakurichi_CrematoriumDMA_No': Kallakurichi_CrematoriumDMA_No,
            'Kallakurichi_CulvertDMA_Cost': Kallakurichi_CulvertDMA_Cost,
            'Kallakurichi_CulvertDMA_No': Kallakurichi_CulvertDMA_No,
            'Kallakurichi_KnowledgeDMA_Centre_No': Kallakurichi_KnowledgeDMA_Centre_No,
            'Kallakurichi_KnowledgeDMA_Centre_Cost': Kallakurichi_KnowledgeDMA_Centre_Cost,
            'Kallakurichi_MarketDMA_No': Kallakurichi_MarketDMA_No,
            'Kallakurichi_MarketDMA_Cost': Kallakurichi_MarketDMA_Cost,
            'Kallakurichi_ParksDMA_No': Kallakurichi_ParksDMA_No,
            'Kallakurichi_ParksDMA_Cost': Kallakurichi_ParksDMA_Cost,
            'Kallakurichi_PaverBlockDMA_No': Kallakurichi_PaverBlockDMA_No,
            'Kallakurichi_PaverBlockDMA_Cost': Kallakurichi_PaverBlockDMA_Cost,
            'Kallakurichi_SWDDMA_No': Kallakurichi_SWDDMA_No,
            'Kallakurichi_SWDDMA_Cost': Kallakurichi_SWDDMA_Cost,
            'Kallakurichi_WBDMA_No': Kallakurichi_WBDMA_No,
            'Kallakurichi_WBDMA_Cost': Kallakurichi_WBDMA_Cost,
            'Kallakurichi_total_no': Kallakurichi_total_no,
            'Kallakurichi_total_cost': Kallakurichi_total_cost,
            'Kancheepuram_BT_RoadDMA_No': Kancheepuram_BT_RoadDMA_No,
            'Kancheepuram_BT_RoadDMA_Cost': Kancheepuram_BT_RoadDMA_Cost,
            'Kancheepuram_CC_RoadDMA_No': Kancheepuram_CC_RoadDMA_No,
            'Kancheepuram_CC_RoadDMA_Cost': Kancheepuram_CC_RoadDMA_Cost,
            'Kancheepuram_CrematoriumDMA_Cost': Kancheepuram_CrematoriumDMA_Cost,
            'Kancheepuram_CrematoriumDMA_No': Kancheepuram_CrematoriumDMA_No,
            'Kancheepuram_CulvertDMA_Cost': Kancheepuram_CulvertDMA_Cost,
            'Kancheepuram_CulvertDMA_No': Kancheepuram_CulvertDMA_No,
            'Kancheepuram_KnowledgeDMA_Centre_No': Kancheepuram_KnowledgeDMA_Centre_No,
            'Kancheepuram_KnowledgeDMA_Centre_Cost': Kancheepuram_KnowledgeDMA_Centre_Cost,
            'Kancheepuram_MarketDMA_No': Kancheepuram_MarketDMA_No,
            'Kancheepuram_MarketDMA_Cost': Kancheepuram_MarketDMA_Cost,
            'Kancheepuram_ParksDMA_No': Kancheepuram_ParksDMA_No,
            'Kancheepuram_ParksDMA_Cost': Kancheepuram_ParksDMA_Cost,
            'Kancheepuram_PaverBlockDMA_No': Kancheepuram_PaverBlockDMA_No,
            'Kancheepuram_PaverBlockDMA_Cost': Kancheepuram_PaverBlockDMA_Cost,
            'Kancheepuram_SWDDMA_No': Kancheepuram_SWDDMA_No,
            'Kancheepuram_SWDDMA_Cost': Kancheepuram_SWDDMA_Cost,
            'Kancheepuram_WBDMA_No': Kancheepuram_WBDMA_No,
            'Kancheepuram_WBDMA_Cost': Kancheepuram_WBDMA_Cost,
            'Kancheepuram_total_no': Kancheepuram_total_no,
            'Kancheepuram_total_cost': Kancheepuram_total_cost,

            'Kanyakumari_BT_RoadDMA_No': Kanyakumari_BT_RoadDMA_No,
            'Kanyakumari_BT_RoadDMA_Cost': Kanyakumari_BT_RoadDMA_Cost,
            'Kanyakumari_CC_RoadDMA_No': Kanyakumari_CC_RoadDMA_No,
            'Kanyakumari_CC_RoadDMA_Cost': Kanyakumari_CC_RoadDMA_Cost,
            'Kanyakumari_CrematoriumDMA_Cost': Kanyakumari_CrematoriumDMA_Cost,
            'Kanyakumari_CrematoriumDMA_No': Kanyakumari_CrematoriumDMA_No,
            'Kanyakumari_CulvertDMA_Cost': Kanyakumari_CulvertDMA_Cost,
            'Kanyakumari_CulvertDMA_No': Kanyakumari_CulvertDMA_No,
            'Kanyakumari_KnowledgeDMA_Centre_No': Kanyakumari_KnowledgeDMA_Centre_No,
            'Kanyakumari_KnowledgeDMA_Centre_Cost': Kanyakumari_KnowledgeDMA_Centre_Cost,
            'Kanyakumari_MarketDMA_No': Kanyakumari_MarketDMA_No,
            'Kanyakumari_MarketDMA_Cost': Kanyakumari_MarketDMA_Cost,
            'Kanyakumari_ParksDMA_No': Kanyakumari_ParksDMA_No,
            'Kanyakumari_ParksDMA_Cost': Kanyakumari_ParksDMA_Cost,
            'Kanyakumari_PaverBlockDMA_No': Kanyakumari_PaverBlockDMA_No,
            'Kanyakumari_PaverBlockDMA_Cost': Kanyakumari_PaverBlockDMA_Cost,
            'Kanyakumari_SWDDMA_No': Kanyakumari_SWDDMA_No,
            'Kanyakumari_SWDDMA_Cost': Kanyakumari_SWDDMA_Cost,
            'Kanyakumari_WBDMA_No': Kanyakumari_WBDMA_No,
            'Kanyakumari_WBDMA_Cost': Kanyakumari_WBDMA_Cost,
            'Kanyakumari_total_no': Kanyakumari_total_no,
            'Kanyakumari_total_cost': Kanyakumari_total_cost,
            'Karur_BT_RoadDMA_No': Karur_BT_RoadDMA_No,
            'Karur_BT_RoadDMA_Cost': Karur_BT_RoadDMA_Cost,
            'Karur_CC_RoadDMA_No': Karur_CC_RoadDMA_No,
            'Karur_CC_RoadDMA_Cost': Karur_CC_RoadDMA_Cost,
            'Karur_CrematoriumDMA_Cost': Karur_CrematoriumDMA_Cost,
            'Karur_CrematoriumDMA_No': Karur_CrematoriumDMA_No,
            'Karur_CulvertDMA_Cost': Karur_CulvertDMA_Cost,
            'Karur_CulvertDMA_No': Karur_CulvertDMA_No,
            'Karur_KnowledgeDMA_Centre_No': Karur_KnowledgeDMA_Centre_No,
            'Karur_KnowledgeDMA_Centre_Cost': Karur_KnowledgeDMA_Centre_Cost,
            'Karur_MarketDMA_No': Karur_MarketDMA_No,
            'Karur_MarketDMA_Cost': Karur_MarketDMA_Cost,
            'Karur_ParksDMA_No': Karur_ParksDMA_No,
            'Karur_ParksDMA_Cost': Karur_ParksDMA_Cost,
            'Karur_PaverBlockDMA_No': Karur_PaverBlockDMA_No,
            'Karur_PaverBlockDMA_Cost': Karur_PaverBlockDMA_Cost,
            'Karur_SWDDMA_No': Karur_SWDDMA_No,
            'Karur_SWDDMA_Cost': Karur_SWDDMA_Cost,
            'Karur_WBDMA_No': Karur_WBDMA_No,
            'Karur_WBDMA_Cost': Karur_WBDMA_Cost,
            'Karur_total_no': Karur_total_no,
            'Karur_total_cost': Karur_total_cost,

            'Krishnagiri_BT_RoadDMA_No': Krishnagiri_BT_RoadDMA_No,
            'Krishnagiri_BT_RoadDMA_Cost': Krishnagiri_BT_RoadDMA_Cost,
            'Krishnagiri_CC_RoadDMA_No': Krishnagiri_CC_RoadDMA_No,
            'Krishnagiri_CC_RoadDMA_Cost': Krishnagiri_CC_RoadDMA_Cost,
            'Krishnagiri_CrematoriumDMA_Cost': Krishnagiri_CrematoriumDMA_Cost,
            'Krishnagiri_CrematoriumDMA_No': Krishnagiri_CrematoriumDMA_No,
            'Krishnagiri_CulvertDMA_Cost': Krishnagiri_CulvertDMA_Cost,
            'Krishnagiri_CulvertDMA_No': Krishnagiri_CulvertDMA_No,
            'Krishnagiri_KnowledgeDMA_Centre_No': Krishnagiri_KnowledgeDMA_Centre_No,
            'Krishnagiri_KnowledgeDMA_Centre_Cost': Krishnagiri_KnowledgeDMA_Centre_Cost,
            'Krishnagiri_MarketDMA_No': Krishnagiri_MarketDMA_No,
            'Krishnagiri_MarketDMA_Cost': Krishnagiri_MarketDMA_Cost,
            'Krishnagiri_ParksDMA_No': Krishnagiri_ParksDMA_No,
            'Krishnagiri_ParksDMA_Cost': Krishnagiri_ParksDMA_Cost,
            'Krishnagiri_PaverBlockDMA_No': Krishnagiri_PaverBlockDMA_No,
            'Krishnagiri_PaverBlockDMA_Cost': Krishnagiri_PaverBlockDMA_Cost,
            'Krishnagiri_SWDDMA_No': Krishnagiri_SWDDMA_No,
            'Krishnagiri_SWDDMA_Cost': Krishnagiri_SWDDMA_Cost,
            'Krishnagiri_WBDMA_No': Krishnagiri_WBDMA_No,
            'Krishnagiri_WBDMA_Cost': Krishnagiri_WBDMA_Cost,
            'Krishnagiri_total_no': Krishnagiri_total_no,
            'Krishnagiri_total_cost': Krishnagiri_total_cost,
            'Madurai_BT_RoadDMA_No': Madurai_BT_RoadDMA_No,
            'Madurai_BT_RoadDMA_Cost': Madurai_BT_RoadDMA_Cost,
            'Madurai_CC_RoadDMA_No': Madurai_CC_RoadDMA_No,
            'Madurai_CC_RoadDMA_Cost': Madurai_CC_RoadDMA_Cost,
            'Madurai_CrematoriumDMA_Cost': Madurai_CrematoriumDMA_Cost,
            'Madurai_CrematoriumDMA_No': Madurai_CrematoriumDMA_No,
            'Madurai_CulvertDMA_Cost': Madurai_CulvertDMA_Cost,
            'Madurai_CulvertDMA_No': Madurai_CulvertDMA_No,
            'Madurai_KnowledgeDMA_Centre_No': Madurai_KnowledgeDMA_Centre_No,
            'Madurai_KnowledgeDMA_Centre_Cost': Madurai_KnowledgeDMA_Centre_Cost,
            'Madurai_MarketDMA_No': Madurai_MarketDMA_No,
            'Madurai_MarketDMA_Cost': Madurai_MarketDMA_Cost,
            'Madurai_ParksDMA_No': Madurai_ParksDMA_No,
            'Madurai_ParksDMA_Cost': Madurai_ParksDMA_Cost,
            'Madurai_PaverBlockDMA_No': Madurai_PaverBlockDMA_No,
            'Madurai_PaverBlockDMA_Cost': Madurai_PaverBlockDMA_Cost,
            'Madurai_SWDDMA_No': Madurai_SWDDMA_No,
            'Madurai_SWDDMA_Cost': Madurai_SWDDMA_Cost,
            'Madurai_WBDMA_No': Madurai_WBDMA_No,
            'Madurai_WBDMA_Cost': Madurai_WBDMA_Cost,
            'Madurai_total_no': Madurai_total_no,
            'Madurai_total_cost': Madurai_total_cost,
            'Mayiladuthurai_BT_RoadDMA_No': Mayiladuthurai_BT_RoadDMA_No,
            'Mayiladuthurai_BT_RoadDMA_Cost': Mayiladuthurai_BT_RoadDMA_Cost,
            'Mayiladuthurai_CC_RoadDMA_No': Mayiladuthurai_CC_RoadDMA_No,
            'Mayiladuthurai_CC_RoadDMA_Cost': Mayiladuthurai_CC_RoadDMA_Cost,
            'Mayiladuthurai_CrematoriumDMA_Cost': Mayiladuthurai_CrematoriumDMA_Cost,
            'Mayiladuthurai_CrematoriumDMA_No': Mayiladuthurai_CrematoriumDMA_No,
            'Mayiladuthurai_CulvertDMA_Cost': Mayiladuthurai_CulvertDMA_Cost,
            'Mayiladuthurai_CulvertDMA_No': Mayiladuthurai_CulvertDMA_No,
            'Mayiladuthurai_KnowledgeDMA_Centre_No': Mayiladuthurai_KnowledgeDMA_Centre_No,
            'Mayiladuthurai_KnowledgeDMA_Centre_Cost': Mayiladuthurai_KnowledgeDMA_Centre_Cost,
            'Mayiladuthurai_MarketDMA_No': Mayiladuthurai_MarketDMA_No,
            'Mayiladuthurai_MarketDMA_Cost': Mayiladuthurai_MarketDMA_Cost,
            'Mayiladuthurai_ParksDMA_No': Mayiladuthurai_ParksDMA_No,
            'Mayiladuthurai_ParksDMA_Cost': Mayiladuthurai_ParksDMA_Cost,
            'Mayiladuthurai_PaverBlockDMA_No': Mayiladuthurai_PaverBlockDMA_No,
            'Mayiladuthurai_PaverBlockDMA_Cost': Mayiladuthurai_PaverBlockDMA_Cost,
            'Mayiladuthurai_SWDDMA_No': Mayiladuthurai_SWDDMA_No,
            'Mayiladuthurai_SWDDMA_Cost': Mayiladuthurai_SWDDMA_Cost,
            'Mayiladuthurai_WBDMA_No': Mayiladuthurai_WBDMA_No,
            'Mayiladuthurai_WBDMA_Cost': Mayiladuthurai_WBDMA_Cost,
            'Mayiladuthurai_total_no': Mayiladuthurai_total_no,
            'Mayiladuthurai_total_cost': Mayiladuthurai_total_cost,
            'Nagapattinam_BT_RoadDMA_No': Nagapattinam_BT_RoadDMA_No,
            'Nagapattinam_BT_RoadDMA_Cost': Nagapattinam_BT_RoadDMA_Cost,
            'Nagapattinam_CC_RoadDMA_No': Nagapattinam_CC_RoadDMA_No,
            'Nagapattinam_CC_RoadDMA_Cost': Nagapattinam_CC_RoadDMA_Cost,
            'Nagapattinam_CrematoriumDMA_Cost': Nagapattinam_CrematoriumDMA_Cost,
            'Nagapattinam_CrematoriumDMA_No': Nagapattinam_CrematoriumDMA_No,
            'Nagapattinam_CulvertDMA_Cost': Nagapattinam_CulvertDMA_Cost,
            'Nagapattinam_CulvertDMA_No': Nagapattinam_CulvertDMA_No,
            'Nagapattinam_KnowledgeDMA_Centre_No': Nagapattinam_KnowledgeDMA_Centre_No,
            'Nagapattinam_KnowledgeDMA_Centre_Cost': Nagapattinam_KnowledgeDMA_Centre_Cost,
            'Nagapattinam_MarketDMA_No': Nagapattinam_MarketDMA_No,
            'Nagapattinam_MarketDMA_Cost': Nagapattinam_MarketDMA_Cost,
            'Nagapattinam_ParksDMA_No': Nagapattinam_ParksDMA_No,
            'Nagapattinam_ParksDMA_Cost': Nagapattinam_ParksDMA_Cost,
            'Nagapattinam_PaverBlockDMA_No': Nagapattinam_PaverBlockDMA_No,
            'Nagapattinam_PaverBlockDMA_Cost': Nagapattinam_PaverBlockDMA_Cost,
            'Nagapattinam_SWDDMA_No': Nagapattinam_SWDDMA_No,
            'Nagapattinam_SWDDMA_Cost': Nagapattinam_SWDDMA_Cost,
            'Nagapattinam_WBDMA_No': Nagapattinam_WBDMA_No,
            'Nagapattinam_WBDMA_Cost': Nagapattinam_WBDMA_Cost,
            'Nagapattinam_total_no': Nagapattinam_total_no,
            'Nagapattinam_total_cost': Nagapattinam_total_cost,
            'Namakkal_BT_RoadDMA_No': Namakkal_BT_RoadDMA_No,
            'Namakkal_BT_RoadDMA_Cost': Namakkal_BT_RoadDMA_Cost,
            'Namakkal_CC_RoadDMA_No': Namakkal_CC_RoadDMA_No,
            'Namakkal_CC_RoadDMA_Cost': Namakkal_CC_RoadDMA_Cost,
            'Namakkal_CrematoriumDMA_Cost': Namakkal_CrematoriumDMA_Cost,
            'Namakkal_CrematoriumDMA_No': Namakkal_CrematoriumDMA_No,
            'Namakkal_CulvertDMA_Cost': Namakkal_CulvertDMA_Cost,
            'Namakkal_CulvertDMA_No': Namakkal_CulvertDMA_No,
            'Namakkal_KnowledgeDMA_Centre_No': Namakkal_KnowledgeDMA_Centre_No,
            'Namakkal_KnowledgeDMA_Centre_Cost': Namakkal_KnowledgeDMA_Centre_Cost,
            'Namakkal_MarketDMA_No': Namakkal_MarketDMA_No,
            'Namakkal_MarketDMA_Cost': Namakkal_MarketDMA_Cost,
            'Namakkal_ParksDMA_No': Namakkal_ParksDMA_No,
            'Namakkal_ParksDMA_Cost': Namakkal_ParksDMA_Cost,
            'Namakkal_PaverBlockDMA_No': Namakkal_PaverBlockDMA_No,
            'Namakkal_PaverBlockDMA_Cost': Namakkal_PaverBlockDMA_Cost,
            'Namakkal_SWDDMA_No': Namakkal_SWDDMA_No,
            'Namakkal_SWDDMA_Cost': Namakkal_SWDDMA_Cost,
            'Namakkal_WBDMA_No': Namakkal_WBDMA_No,
            'Namakkal_WBDMA_Cost': Namakkal_WBDMA_Cost,
            'Namakkal_total_no': Namakkal_total_no,
            'Namakkal_total_cost': Namakkal_total_cost,
            'Nilgiris_BT_RoadDMA_No': Nilgiris_BT_RoadDMA_No,
            'Nilgiris_BT_RoadDMA_Cost': Nilgiris_BT_RoadDMA_Cost,
            'Nilgiris_CC_RoadDMA_No': Nilgiris_CC_RoadDMA_No,
            'Nilgiris_CC_RoadDMA_Cost': Nilgiris_CC_RoadDMA_Cost,
            'Nilgiris_CrematoriumDMA_Cost': Nilgiris_CrematoriumDMA_Cost,
            'Nilgiris_CrematoriumDMA_No': Nilgiris_CrematoriumDMA_No,
            'Nilgiris_CulvertDMA_Cost': Nilgiris_CulvertDMA_Cost,
            'Nilgiris_CulvertDMA_No': Nilgiris_CulvertDMA_No,
            'Nilgiris_KnowledgeDMA_Centre_No': Nilgiris_KnowledgeDMA_Centre_No,
            'Nilgiris_KnowledgeDMA_Centre_Cost': Nilgiris_KnowledgeDMA_Centre_Cost,
            'Nilgiris_MarketDMA_No': Nilgiris_MarketDMA_No,
            'Nilgiris_MarketDMA_Cost': Nilgiris_MarketDMA_Cost,
            'Nilgiris_ParksDMA_No': Nilgiris_ParksDMA_No,
            'Nilgiris_ParksDMA_Cost': Nilgiris_ParksDMA_Cost,
            'Nilgiris_PaverBlockDMA_No': Nilgiris_PaverBlockDMA_No,
            'Nilgiris_PaverBlockDMA_Cost': Nilgiris_PaverBlockDMA_Cost,
            'Nilgiris_SWDDMA_No': Nilgiris_SWDDMA_No,
            'Nilgiris_SWDDMA_Cost': Nilgiris_SWDDMA_Cost,
            'Nilgiris_WBDMA_No': Nilgiris_WBDMA_No,
            'Nilgiris_WBDMA_Cost': Nilgiris_WBDMA_Cost,
            'Nilgiris_total_no': Nilgiris_total_no,
            'Nilgiris_total_cost': Nilgiris_total_cost,
        }
        response.context_data.update(extra_context)
        return response


admin.site.register(ULBReleaseRequest)


@admin.register(ULBProgressIncompleted)
class ULBProgressIncompletedAdmin(admin.ModelAdmin):
    change_list_template = 'admin/ulbprogressincompleted.html'

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        response.context_data['report'] = list(
            qs.values('user__first_name', 'Project_ID', 'Sector').order_by('user__first_name').filter(
                status=None).filter(Scheme='KNMT'))
        return response


def Decimal(x):
    return float(x)


@admin.register(ProjectProgressDetailsReport)
class ProjectProgressDetailsReportAdmin(admin.ModelAdmin):
    change_list_template = 'admin/projectprogressdetails.html'

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        qs1 = MasterSanctionForm.objects.values_list('Sector', 'Project_ID', 'District__District',
                                                     'ApprovedProjectCost')

        r_qs1 = MasterSanctionForm.objects.all()
        r_qs1.query = pickle.loads(pickle.dumps(qs1.query))
        qs2 = AgencyProgressModel.objects.values_list('Sector', 'Project_ID', 'status')

        r_qs2 = AgencyProgressModel.objects.all()
        r_qs2.query = pickle.loads(pickle.dumps(qs2.query))

        query_set = []
        for i in r_qs1:
            for j in r_qs2:
                if i['Project_ID'] == j['Project_ID']:
                    i['status'] = j['status']
                    query_set.append(i)

        response.context_data['report'] = list(
            qs.values('Sector').order_by('user__first_name').filter(
                status=None).filter(Scheme='KNMT'))

        return response


@admin.register(Dashboard)
class DashboardAdmin(admin.ModelAdmin):
    change_list_template = "admin/dashboard.html"

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        ULBType = []
        for i in map(str, request.user.groups.all()):
            ULBType.append(i)
        metrics = {
            'Sector_total': Count('Sector'),
        }
        metrics_project = {
            'project_cost': Sum('ApprovedProjectCost'),
        }
        ulb_metrics = {
            'ulb_project_cost': Sum('ApprovedProjectCost'),
            'ulb_works': Count('Project_ID')
        }

        response.context_data['sectorbarchart'] = list(qs.values('Sector').exclude(
            Sector__in=['BT Road', 'CC Road', 'Retaining wall', 'Paver Block', 'SWD', 'Culvert',
                        'Metal Beam Crash Barriers']).filter(Scheme__Scheme='KNMT').annotate(
            **metrics_project).order_by('Sector'))

        response.context_data['sectorbarchartDMA'] = list(qs.values('Sector').exclude(
            Sector__in=['BT Road', 'CC Road', 'Retaining wall', 'Paver Block', 'SWD', 'Culvert',
                        'Metal Beam Crash Barriers']).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').annotate(**metrics_project).order_by('Sector'))

        response.context_data['sectorbarchartCTP'] = list(qs.values('Sector').exclude(
            Sector__in=['BT Road', 'CC Road', 'Retaining wall', 'Paver Block', 'SWD', 'Culvert',
                        'Metal Beam Crash Barriers']).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').annotate(**metrics_project).order_by('Sector'))

        response.context_data['piechart'] = list(
            qs.values('Sector').filter(Scheme__Scheme='KNMT').annotate(**metrics).order_by('Sector'))
        if request.user.groups.filter(name__in=['Corporation']).exists():
            response.context_data['ulbpiechart'] = list(
                qs.values('Sector').filter(AgencyName__AgencyName=request.user.first_name).annotate(
                    **ulb_metrics).order_by(
                    'Sector'))
            response.context_data['ulbdonutchart'] = list(
                qs.values('Sector').filter(AgencyName__AgencyName=request.user.first_name).annotate(
                    **ulb_metrics).order_by(
                    'ulb_works'))
        else:
            response.context_data['ulbpiechart'] = list(
                qs.values('Sector').filter(AgencyName__AgencyName=request.user.first_name).filter(
                    AgencyType__AgencyType=ULBType[1]).annotate(**ulb_metrics).order_by(
                    'Sector'))
            response.context_data['ulbdonutchart'] = list(
                qs.values('Sector').filter(AgencyName__AgencyName=request.user.first_name).filter(
                    AgencyType__AgencyType=ULBType[1]).annotate(**ulb_metrics).order_by(
                    'ulb_works'))

        road = MasterSanctionForm.objects.filter(
            Sector__in=['BT Road', 'CC Road', 'Retaining wall', 'Paver Block', 'SWD', 'Culvert',
                        'Metal Beam Crash Barriers']).filter(Scheme__Scheme='KNMT').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        road_total = MasterSanctionForm.objects.filter(
            Sector__in=['BT Road', 'CC Road', 'Retaining wall', 'Paver Block', 'SWD', 'Culvert',
                        'Metal Beam Crash Barriers']).filter(Scheme__Scheme='KNMT').count()
        roadDMA = MasterSanctionForm.objects.filter(
            Sector__in=['BT Road', 'CC Road', 'Retaining wall', 'Paver Block', 'SWD', 'Culvert',
                        'Metal Beam Crash Barriers']).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType="Municipality").aggregate(project_cost=Sum('ApprovedProjectCost'))
        roadDMA_total = MasterSanctionForm.objects.filter(
            Sector__in=['BT Road', 'CC Road', 'Retaining wall', 'Paver Block', 'SWD', 'Culvert',
                        'Metal Beam Crash Barriers']).filter(
            AgencyType__AgencyType="Municipality").filter(Scheme__Scheme='KNMT').count()
        roadCTP = MasterSanctionForm.objects.filter(
            Sector__in=['BT Road', 'CC Road', 'Retaining wall', 'Paver Block', 'SWD', 'Culvert',
                        'Metal Beam Crash Barriers']).filter(
            AgencyType__AgencyType="Town Panchayat").filter(Scheme__Scheme='KNMT').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        roadCTP_total = MasterSanctionForm.objects.filter(
            Sector__in=['BT Road', 'CC Road', 'Retaining wall', 'Paver Block', 'SWD', 'Culvert',
                        'Metal Beam Crash Barriers']).filter(
            AgencyType__AgencyType="Town Panchayat").filter(Scheme__Scheme='KNMT').count()

        busstand = MasterSanctionForm.objects.filter(Sector__in=['Bus Stand']).filter(Scheme__Scheme='KNMT').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        busstand_total = MasterSanctionForm.objects.filter(Sector__in=['Bus Stand']).filter(
            Scheme__Scheme='KNMT').count()
        busstandDMA = MasterSanctionForm.objects.filter(Sector__in=['Bus Stand']).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType="Municipality").aggregate(project_cost=Sum('ApprovedProjectCost'))
        busstandDMA_total = MasterSanctionForm.objects.filter(Sector__in=['Bus Stand']).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType="Municipality").count()
        busstandCTP = MasterSanctionForm.objects.filter(Sector__in=['Bus Stand']).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType="Town Panchayat").aggregate(project_cost=Sum('ApprovedProjectCost'))
        busstandCTP_total = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector__in=['Bus Stand']).filter(
            AgencyType__AgencyType="Town Panchayat").count()

        ch = MasterSanctionForm.objects.filter(Sector__in=['Community Hall']).filter(Scheme__Scheme='KNMT').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        ch_total = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector__in=['Community Hall']).count()
        chDMA = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector__in=['Community Hall']).filter(
            AgencyType__AgencyType="Municipality").aggregate(project_cost=Sum('ApprovedProjectCost'))
        chDMA_total = MasterSanctionForm.objects.filter(Sector__in=['Community Hall']).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType="Municipality").count()
        chCTP = MasterSanctionForm.objects.filter(Sector="Community Hall").filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType="Town Panchayat").aggregate(project_cost=Sum('ApprovedProjectCost'))
        chCTP_total = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector__in=['Community Hall']).filter(
            AgencyType__AgencyType="Town Panchayat").count()

        crematorium = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector__in=['Crematorium']).aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        crematorium_total = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector__in=['Crematorium']).count()
        crematoriumDMA = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector__in=['Crematorium']).filter(
            AgencyType__AgencyType="Municipality").filter(Scheme__Scheme='KNMT').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        crematoriumDMA_total = MasterSanctionForm.objects.filter(Sector__in=['Crematorium']).filter(
            Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType="Municipality").count()
        crematoriumCTP = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector__in=['Crematorium']).filter(
            AgencyType__AgencyType="Town Panchayat").aggregate(project_cost=Sum('ApprovedProjectCost'))
        crematoriumCTP_total = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector__in=['Crematorium']).filter(
            AgencyType__AgencyType="Town Panchayat").count()

        KC = MasterSanctionForm.objects.filter(Sector__in=['Knowledge Centre']).filter(Scheme__Scheme='KNMT').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        KC_total = MasterSanctionForm.objects.filter(Sector__in=['Knowledge Centre']).filter(
            Scheme__Scheme='KNMT').count()
        KCDMA = MasterSanctionForm.objects.filter(Sector__in=['Knowledge Centre']).filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType="Municipality").aggregate(project_cost=Sum('ApprovedProjectCost'))
        KCDMA_total = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector__in=['Knowledge Centre']).filter(
            AgencyType__AgencyType="Municipality").count()
        KCCTP = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector__in=['Knowledge Centre']).filter(
            AgencyType__AgencyType="Town Panchayat").aggregate(project_cost=Sum('ApprovedProjectCost'))
        KCCTP_total = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector__in=['Knowledge Centre']).filter(
            AgencyType__AgencyType="Town Panchayat").count()

        market = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector__in=['Market']).aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        market_total = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector__in=['Market']).count()
        marketDMA = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector__in=['Market']).filter(
            AgencyType__AgencyType="Municipality").aggregate(project_cost=Sum('ApprovedProjectCost'))
        marketDMA_total = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector__in=['Market']).filter(
            AgencyType__AgencyType="Municipality").count()
        marketCTP = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector__in=['Market']).filter(
            AgencyType__AgencyType="Town Panchayat").aggregate(project_cost=Sum('ApprovedProjectCost'))
        marketCTP_total = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector__in=['Market']).filter(
            AgencyType__AgencyType="Town Panchayat").count()

        park = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector__in=['Parks']).aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        park_total = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector__in=['Parks']).count()
        parkDMA = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector__in=['Parks']).filter(
            AgencyType__AgencyType="Municipality").aggregate(project_cost=Sum('ApprovedProjectCost'))
        parkDMA_total = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector__in=['Parks']).filter(
            AgencyType__AgencyType="Municipality").count()
        parkCTP = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector__in=['Parks']).filter(
            AgencyType__AgencyType="Town Panchayat").aggregate(project_cost=Sum('ApprovedProjectCost'))
        parkCTP_total = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector__in=['Parks']).filter(
            AgencyType__AgencyType="Town Panchayat").count()

        SWM = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector__in=['Solid Waste Mgt.']).aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        SWM_total = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector__in=['Solid Waste Mgt.']).count()
        SWMDMA = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector__in=['Solid Waste Mgt.']).filter(
            AgencyType__AgencyType="Municipality").aggregate(project_cost=Sum('ApprovedProjectCost'))
        SWMDMA_total = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector__in=['Solid Waste Mgt.']).filter(
            AgencyType__AgencyType="Municipality").count()
        SWMCTP = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector__in=['Solid Waste Mgt.']).filter(
            AgencyType__AgencyType="Town Panchayat").aggregate(project_cost=Sum('ApprovedProjectCost'))
        SWMCTP_total = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector__in=['Solid Waste Mgt.']).filter(
            AgencyType__AgencyType="Town Panchayat").count()

        WB = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector__in=['Water Bodies']).aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        WB_total = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector__in=['Water Bodies']).count()
        WBDMA = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector__in=['Water Bodies']).filter(
            AgencyType__AgencyType="Municipality").aggregate(project_cost=Sum('ApprovedProjectCost'))
        WBDMA_total = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector__in=['Water Bodies']).filter(
            AgencyType__AgencyType="Municipality").count()
        WBCTP = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector="Water Bodies").filter(
            AgencyType__AgencyType="Town Panchayat").aggregate(project_cost=Sum('ApprovedProjectCost'))
        WBCTP_total = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector__in=['Water Bodies']).filter(
            AgencyType__AgencyType="Town Panchayat").count()

        total_projects = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').count()
        project_cost = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').aggregate(
            project_cost=Sum('ApprovedProjectCost'))

        busstand_percentage = "{:.2f}".format((busstand['project_cost']) / (project_cost['project_cost']) * 100)
        ch_percent = "{:.2f}".format((ch['project_cost']) / (project_cost['project_cost']) * 100)
        crematorium_pt = "{:.2f}".format((crematorium['project_cost']) / (project_cost['project_cost']) * 100)
        KC_pt = "{:.2f}".format((KC['project_cost']) / (project_cost['project_cost']) * 100)
        market_pt = "{:.2f}".format((market['project_cost']) / (project_cost['project_cost']) * 100)
        park_pt = "{:.2f}".format((park['project_cost']) / (project_cost['project_cost']) * 100)
        SWM_pt = "{:.2f}".format((SWM['project_cost']) / (project_cost['project_cost']) * 100)
        WB_pt = "{:.2f}".format((WB['project_cost']) / (project_cost['project_cost']) * 100)
        road_pt = "{:.2f}".format((road['project_cost']) / (project_cost['project_cost']) * 100)

        def bus_dma_percent():
            if busstandDMA['project_cost'] == None:
                v = 0
            else:
                v = busstandDMA['project_cost']
            return v

        def ch_dma_percent():
            if chDMA['project_cost'] == None:
                v = 0
            else:
                v = chDMA['project_cost']
            return v

        def SWM_dma_percent():
            if SWMDMA['project_cost'] == None:
                v = 0
            else:
                v = SWMDMA['project_cost']
            return v

        def park_ctp_percent():
            if parkCTP['project_cost'] == None:
                return 0
            else:
                return parkCTP['project_cost']

        def water_bodies_ctp_percent():
            if WBCTP['project_cost'] == None:
                return 0
            else:
                return WBCTP['project_cost']

        dmp_project_cost = MasterSanctionForm.objects.filter(
            AgencyType__AgencyType='Municipality').filter(Scheme__Scheme='KNMT').aggregate(
            dmp_project_cost=Sum('ApprovedProjectCost'))
        ctp_project_cost = MasterSanctionForm.objects.filter(
            AgencyType__AgencyType='Town Panchayat').filter(Scheme__Scheme='KNMT').aggregate(
            ctp_project_cost=Sum('ApprovedProjectCost'))

        DMAbusstand_percentage = "{:.2f}".format(bus_dma_percent() / (project_cost['project_cost']) * 100)
        DMAch_percent = "{:.2f}".format(ch_dma_percent() / (project_cost['project_cost']) * 100)
        DMAcrematorium_pt = "{:.2f}".format((crematoriumDMA['project_cost']) / (project_cost['project_cost']) * 100)
        DMAKC_pt = "{:.2f}".format((KCDMA['project_cost']) / (project_cost['project_cost']) * 100)
        DMAmarket_pt = "{:.2f}".format((marketDMA['project_cost']) / (project_cost['project_cost']) * 100)
        DMApark_pt = "{:.2f}".format((parkDMA['project_cost']) / (project_cost['project_cost']) * 100)
        DMAroad_pt = "{:.2f}".format((roadDMA['project_cost']) / (project_cost['project_cost']) * 100)
        DMASWM_pt = "{:.2f}".format(SWM_dma_percent() / (project_cost['project_cost']) * 100)
        DMAWB_pt = "{:.2f}".format((WBDMA['project_cost']) / (project_cost['project_cost']) * 100)
        DMA_total_percent = "{:.2f}".format(dmp_project_cost['dmp_project_cost'] / (project_cost['project_cost']) * 100)

        CTPbusstand_percentage = "{:.2f}".format((busstandCTP['project_cost']) / (project_cost['project_cost']) * 100)
        CTPch_percent = "{:.2f}".format(chCTP['project_cost'] / (project_cost['project_cost']) * 100)
        CTPcrematorium_pt = "{:.2f}".format((crematoriumCTP['project_cost']) / (project_cost['project_cost']) * 100)
        CTPKC_pt = "{:.2f}".format((KCCTP['project_cost']) / (project_cost['project_cost']) * 100)
        CTPmarket_pt = "{:.2f}".format((marketCTP['project_cost']) / (project_cost['project_cost']) * 100)
        CTPpark_pt = "{:.2f}".format(park_ctp_percent() / (project_cost['project_cost']) * 100)
        CTProad_pt = "{:.2f}".format((roadCTP['project_cost']) / (project_cost['project_cost']) * 100)
        CTPSWM_pt = "{:.2f}".format(SWMCTP['project_cost'] / (project_cost['project_cost']) * 100)
        CTPWB_pt = "{:.2f}".format(water_bodies_ctp_percent() / (project_cost['project_cost']) * 100)
        CTP_total_percent = "{:.2f}".format(ctp_project_cost['ctp_project_cost'] / (project_cost['project_cost']) * 100)

        knmt = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').aggregate(knmt_share=Sum('SchemeShare'))
        ulb_share = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').aggregate(ulb_share=Sum('ULBShare'))
        dmp_total_projects = MasterSanctionForm.objects.filter(AgencyType__AgencyType='Municipality').count()
        dmp_knmt = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(dmp_knmt=Sum('SchemeShare'))
        dmp_ulb_share = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(dmp_ulb_share=Sum('ULBShare'))
        ctp_total_projects = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        ctp_project_cost = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(ctp_project_cost=Sum('ApprovedProjectCost'))
        ctp_knmt = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(ctp_knmt=Sum('SchemeShare'))
        ctp_ulb_share = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(ctp_ulb_share=Sum('ULBShare'))
        if request.user.groups.filter(name__in=['Corporation', ]).exists():
            ulb_total_project = MasterSanctionForm.objects.filter(
                AgencyName__AgencyName=request.user.first_name).count()
            ulb_project_cost = MasterSanctionForm.objects.filter(
                AgencyName__AgencyName=request.user.first_name).aggregate(
                project_cost=Sum('ApprovedProjectCost'))
        else:
            ulb_total_project = MasterSanctionForm.objects.filter(
                AgencyName__AgencyName=request.user.first_name).filter(
                AgencyType__AgencyType=ULBType[1]).count()
            ulb_project_cost = MasterSanctionForm.objects.filter(AgencyName__AgencyName=request.user.first_name).filter(
                AgencyType__AgencyType=ULBType[1]).aggregate(
                project_cost=Sum('ApprovedProjectCost'))

        ulb_knmt_share = MasterSanctionForm.objects.filter(AgencyName__AgencyName=request.user.first_name).filter(
            AgencyType__AgencyType=ULBType[1]).filter(
            Scheme__Scheme='KNMT').aggregate(knmt_share=Sum('SchemeShare'))

        ulb_share_ulb = MasterSanctionForm.objects.filter(AgencyName__AgencyName=request.user.first_name).filter(
            Scheme__Scheme='KNMT').filter(AgencyType__AgencyType=ULBType[1]).aggregate(ulb_share=Sum('ULBShare'))
        ulb_singara_share = MasterSanctionForm.objects.filter(AgencyName__AgencyName=request.user.first_name).filter(
            Scheme__Scheme='Singara Chennai 2.0').aggregate(singara_share=Sum('SchemeShare'))
        ulb_share_ulb_singara = MasterSanctionForm.objects.filter(
            AgencyName__AgencyName=request.user.first_name).filter(
            Scheme__Scheme='Singara Chennai 2.0').aggregate(ulb_share=Sum('ULBShare'))

        pie_chart2 = {
            "Bus Stand": float(busstand['project_cost']),
            "Community Hall": float(ch['project_cost']),
            "Crematorium": float(crematorium['project_cost']),
            "Knowledge Centre": float(KC['project_cost']),
            "Market": float(market['project_cost']),
            "Park": float(park['project_cost']),
            "Road Works": float(road['project_cost']),
            "Solid Waste Mgt.": float(SWM['project_cost']),
            "Water Bodies": float(WB['project_cost'])
        }
        donut_chart2 = {
            "Bus Stand": int(busstand_total),
            "Community Hall": int(ch_total),
            "Crematorium": int(crematorium_total),
            "Knowledge Centre": int(KC_total),
            "Market": int(market_total),
            "Park": int(park_total),
            "Road Works": int(road_total),
            "Solid Waste Mgt.": int(SWM_total),
            "Water Bodies": int(WB_total)
        }

        pie_chart_DMA = {
            "Crematorium": float(crematoriumDMA['project_cost']),
            "Knowledge Centre": float(KCDMA['project_cost']),
            "Market": float(marketDMA['project_cost']),
            "Park": float(parkDMA['project_cost']),
            "Road Works": float(roadDMA['project_cost']),
            "Water Bodies": float(WBDMA['project_cost'])
        }

        donut_chart_DMA = {
            "Crematorium": int(crematoriumDMA_total),
            "Knowledge Centre": int(KCDMA_total),
            "Market": int(marketDMA_total),
            "Park": int(parkDMA_total),
            "Road Works": int(roadDMA_total),
            "Water Bodies": int(WBDMA_total)
        }

        pie_chart_CTP = {
            "Bus Stand": float(busstandCTP['project_cost']),
            "Community Hall": float(chCTP['project_cost']),
            "Crematorium": float(crematoriumCTP['project_cost']),
            "Knowledge Centre": float(KCCTP['project_cost']),
            "Market": float(marketCTP['project_cost']),
            "Park": float(parkCTP['project_cost']),
            "Road Works": float(roadCTP['project_cost']),
            "Solid Waste Mgt.": float(SWMCTP['project_cost']),
            "Water Bodies": float(WBCTP['project_cost'])
        }
        donut_chart_CTP = {
            "Bus Stand": int(busstandCTP_total),
            "Community Hall": int(chCTP_total),
            "Crematorium": int(crematoriumCTP_total),
            "Knowledge Centre": int(KCCTP_total),
            "Market": int(marketCTP_total),
            "Park": int(parkCTP_total),
            "Road Works": int(roadCTP_total),
            "Solid Waste Mgt.": int(SWMCTP_total),
            "Water Bodies": int(WBCTP_total)
        }

        pie_chart_sectorDMA = dict(sorted(pie_chart_DMA.items(), key=lambda x: x[1]))
        pie_chart_sector = dict(sorted(pie_chart2.items(), key=lambda x: x[1]))
        donut_chart_sector = dict(sorted(donut_chart2.items(), key=lambda x: x[1]))
        donut_chart_sectorDMA = dict(sorted(donut_chart_DMA.items(), key=lambda x: x[1]))
        pie_chart_CTP = dict(sorted(pie_chart_CTP.items(), key=lambda x: x[1]))
        donut_chart_CTP = dict(sorted(donut_chart_CTP.items(), key=lambda x: x[1]))

        # District Project Description

        Ariyalur_project_cost = MasterSanctionForm.objects.filter(District__District="Ariyalur").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Ariyalur_total_projects = MasterSanctionForm.objects.filter(District__District="Ariyalur").count()
        DMAAriyalur_project_cost = MasterSanctionForm.objects.filter(District__District="Ariyalur").filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        DMAAriyalur_total_projects = MasterSanctionForm.objects.filter(District__District="Ariyalur").filter(
            AgencyType__AgencyType='Municipality').count()
        CTPAriyalur_project_cost = MasterSanctionForm.objects.filter(District__District="Ariyalur").filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        CTPAriyalur_total_projects = MasterSanctionForm.objects.filter(District__District="Ariyalur").filter(
            AgencyType__AgencyType='Town Panchayat').count()

        Coimbatore_project_cost = MasterSanctionForm.objects.filter(District__District="Coimbatore").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Coimbatore_total_projects = MasterSanctionForm.objects.filter(District__District="Coimbatore").count()
        DMACoimbatore_project_cost = MasterSanctionForm.objects.filter(District__District="Coimbatore").filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        DMACoimbatore_total_projects = MasterSanctionForm.objects.filter(District__District="Coimbatore").filter(
            AgencyType__AgencyType='Municipality').count()
        CTPCoimbatore_project_cost = MasterSanctionForm.objects.filter(District__District="Coimbatore").filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        CTPCoimbatore_total_projects = MasterSanctionForm.objects.filter(District__District="Coimbatore").filter(
            AgencyType__AgencyType='Town Panchayat').count()

        Perambalur_project_cost = MasterSanctionForm.objects.filter(District__District="Perambalur").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Perambalur_total_projects = MasterSanctionForm.objects.filter(District__District="Perambalur").count()

        Chengalpattu_project_cost = MasterSanctionForm.objects.filter(District__District="Chengalpattu").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Chengalpattu_total_projects = MasterSanctionForm.objects.filter(District__District="Chengalpattu").count()
        DMAChengalpattu_project_cost = MasterSanctionForm.objects.filter(District__District="Chengalpattu").filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        DMAChengalpattu_total_projects = MasterSanctionForm.objects.filter(District__District="Chengalpattu").filter(
            AgencyType__AgencyType='Municipality').count()
        CTPChengalpattu_project_cost = MasterSanctionForm.objects.filter(District__District="Chengalpattu").filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        CTPChengalpattu_total_projects = MasterSanctionForm.objects.filter(District__District="Chengalpattu").filter(
            AgencyType__AgencyType='Town Panchayat').count()

        DMACuddalore_project_cost = MasterSanctionForm.objects.filter(District__District="Cuddalore").filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        DMACuddalore_total_projects = MasterSanctionForm.objects.filter(District__District="Cuddalore").filter(
            AgencyType__AgencyType='Municipality').count()
        CTPCuddalore_project_cost = MasterSanctionForm.objects.filter(District__District="Cuddalore").filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        CTPCuddalore_total_projects = MasterSanctionForm.objects.filter(District__District="Cuddalore").filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Cuddalore_project_cost = MasterSanctionForm.objects.filter(District__District="Cuddalore").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Cuddalore_total_projects = MasterSanctionForm.objects.filter(District__District="Cuddalore").count()

        DMADharmapuri_project_cost = MasterSanctionForm.objects.filter(District__District="Dharmapuri").filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        DMADharmapuri_total_projects = MasterSanctionForm.objects.filter(District__District="Dharmapuri").filter(
            AgencyType__AgencyType='Municipality').count()
        CTPDharmapuri_project_cost = MasterSanctionForm.objects.filter(District__District="Dharmapuri").filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        CTPDharmapuri_total_projects = MasterSanctionForm.objects.filter(District__District="Dharmapuri").filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Dharmapuri_project_cost = MasterSanctionForm.objects.filter(District__District="Dharmapuri").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Dharmapuri_total_projects = MasterSanctionForm.objects.filter(District__District="Dharmapuri").count()

        DMADindigul_project_cost = MasterSanctionForm.objects.filter(District__District="Dindigul").filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        DMADindigul_total_projects = MasterSanctionForm.objects.filter(District__District="Dindigul").filter(
            AgencyType__AgencyType='Municipality').count()
        CTPDindigul_project_cost = MasterSanctionForm.objects.filter(District__District="Dindigul").filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        CTPDindigul_total_projects = MasterSanctionForm.objects.filter(District__District="Dindigul").filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Dindigul_project_cost = MasterSanctionForm.objects.filter(District__District="Dindigul").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Dindigul_total_projects = MasterSanctionForm.objects.filter(District__District="Dindigul").count()

        DMAErode_project_cost = MasterSanctionForm.objects.filter(District__District="Erode").filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        DMAErode_total_projects = MasterSanctionForm.objects.filter(District__District="Erode").filter(
            AgencyType__AgencyType='Municipality').count()
        CTPErode_project_cost = MasterSanctionForm.objects.filter(District__District="Erode").filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        CTPErode_total_projects = MasterSanctionForm.objects.filter(District__District="Erode").filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Erode_project_cost = MasterSanctionForm.objects.filter(District__District="Erode").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Erode_total_projects = MasterSanctionForm.objects.filter(District__District="Erode").count()

        DMAKallakurichi_project_cost = MasterSanctionForm.objects.filter(District__District="Kallakurichi").filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        DMAKallakurichi_total_projects = MasterSanctionForm.objects.filter(District__District="Kallakurichi").filter(
            AgencyType__AgencyType='Municipality').count()
        CTPKallakurichi_project_cost = MasterSanctionForm.objects.filter(District__District="Kallakurichi").filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        CTPKallakurichi_total_projects = MasterSanctionForm.objects.filter(District__District="Kallakurichi").filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Kallakurichi_project_cost = MasterSanctionForm.objects.filter(District__District="Kallakurichi").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Kallakurichi_total_projects = MasterSanctionForm.objects.filter(District__District="Kallakurichi").count()

        DMAKancheepuram_project_cost = MasterSanctionForm.objects.filter(District__District="Kancheepuram").filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        DMAKancheepuram_total_projects = MasterSanctionForm.objects.filter(District__District="Kancheepuram").filter(
            AgencyType__AgencyType='Municipality').count()
        CTPKancheepuram_project_cost = MasterSanctionForm.objects.filter(District__District="Kancheepuram").filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        CTPKancheepuram_total_projects = MasterSanctionForm.objects.filter(District__District="Kancheepuram").filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Kancheepuram_project_cost = MasterSanctionForm.objects.filter(District__District="Kancheepuram").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Kancheepuram_total_projects = MasterSanctionForm.objects.filter(District__District="Kancheepuram").count()

        DMAKanyakumari_project_cost = MasterSanctionForm.objects.filter(District__District="Kanyakumari").filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        DMAKanyakumari_total_projects = MasterSanctionForm.objects.filter(District__District="Kanyakumari").filter(
            AgencyType__AgencyType='Municipality').count()
        CTPKanyakumari_project_cost = MasterSanctionForm.objects.filter(District__District="Kanyakumari").filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        CTPKanyakumari_total_projects = MasterSanctionForm.objects.filter(District__District="Kanyakumari").filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Kanyakumari_project_cost = MasterSanctionForm.objects.filter(District__District="Kanyakumari").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Kanyakumari_total_projects = MasterSanctionForm.objects.filter(District__District="Kanyakumari").count()

        Karur_project_cost = MasterSanctionForm.objects.filter(District__District="Karur").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Karur_total_projects = MasterSanctionForm.objects.filter(District__District="Karur").count()
        DMAKarur_project_cost = MasterSanctionForm.objects.filter(District__District="Karur").filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        DMAKarur_total_projects = MasterSanctionForm.objects.filter(District__District="Karur").filter(
            AgencyType__AgencyType='Municipality').count()
        CTPKarur_project_cost = MasterSanctionForm.objects.filter(District__District="Karur").filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        CTPKarur_total_projects = MasterSanctionForm.objects.filter(District__District="Karur").filter(
            AgencyType__AgencyType='Town Panchayat').count()

        DMAMayiladuthurai_project_cost = MasterSanctionForm.objects.filter(District__District="Mayiladuthurai").filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        DMAMayiladuthurai_total_projects = MasterSanctionForm.objects.filter(
            District__District="Mayiladuthurai").filter(
            AgencyType__AgencyType='Municipality').count()
        CTPMayiladuthurai_project_cost = MasterSanctionForm.objects.filter(District__District="Mayiladuthurai").filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        CTPMayiladuthurai_total_projects = MasterSanctionForm.objects.filter(
            District__District="Mayiladuthurai").filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Mayiladuthurai_project_cost = MasterSanctionForm.objects.filter(District__District="Mayiladuthurai").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Mayiladuthurai_total_projects = MasterSanctionForm.objects.filter(District__District="Mayiladuthurai").count()

        Krishnagiri_project_cost = MasterSanctionForm.objects.filter(District__District="Krishnagiri").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Krishnagiri_total_projects = MasterSanctionForm.objects.filter(District__District="Krishnagiri").count()
        DMAKrishnagiri_project_cost = MasterSanctionForm.objects.filter(District__District="Krishnagiri").filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        DMAKrishnagiri_total_projects = MasterSanctionForm.objects.filter(District__District="Krishnagiri").filter(
            AgencyType__AgencyType='Municipality').count()
        CTPKrishnagiri_project_cost = MasterSanctionForm.objects.filter(District__District="Krishnagiri").filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        CTPKrishnagiri_total_projects = MasterSanctionForm.objects.filter(District__District="Krishnagiri").filter(
            AgencyType__AgencyType='Town Panchayat').count()

        DMAMadurai_project_cost = MasterSanctionForm.objects.filter(District__District="Madurai").filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        DMAMadurai_total_projects = MasterSanctionForm.objects.filter(District__District="Madurai").filter(
            AgencyType__AgencyType='Municipality').count()
        CTPMadurai_project_cost = MasterSanctionForm.objects.filter(District__District="Madurai").filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        CTPMadurai_total_projects = MasterSanctionForm.objects.filter(District__District="Madurai").filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Madurai_project_cost = MasterSanctionForm.objects.filter(District__District="Madurai").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Madurai_total_projects = MasterSanctionForm.objects.filter(District__District="Madurai").count()

        DMANagapattinam_project_cost = MasterSanctionForm.objects.filter(District__District="Nagapattinam").filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        DMANagapattinam_total_projects = MasterSanctionForm.objects.filter(District__District="Nagapattinam").filter(
            AgencyType__AgencyType='Municipality').count()
        CTPNagapattinam_project_cost = MasterSanctionForm.objects.filter(District__District="Nagapattinam").filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        CTPNagapattinam_total_projects = MasterSanctionForm.objects.filter(District__District="Nagapattinam").filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Nagapattinam_project_cost = MasterSanctionForm.objects.filter(District__District="Nagapattinam").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Nagapattinam_total_projects = MasterSanctionForm.objects.filter(District__District="Nagapattinam").count()

        DMANamakkal_project_cost = MasterSanctionForm.objects.filter(District__District="Namakkal").filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        DMANamakkal_total_projects = MasterSanctionForm.objects.filter(District__District="Namakkal").filter(
            AgencyType__AgencyType='Municipality').count()
        CTPNamakkal_project_cost = MasterSanctionForm.objects.filter(District__District="Namakkal").filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        CTPNamakkal_total_projects = MasterSanctionForm.objects.filter(District__District="Namakkal").filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Namakkal_project_cost = MasterSanctionForm.objects.filter(District__District="Namakkal").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Namakkal_total_projects = MasterSanctionForm.objects.filter(District__District="Namakkal").count()

        Nilgiris_project_cost = MasterSanctionForm.objects.filter(District__District="Nilgiris").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Nilgiris_total_projects = MasterSanctionForm.objects.filter(District__District="Nilgiris").count()
        DMANilgiris_project_cost = MasterSanctionForm.objects.filter(District__District="Nilgiris").filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        DMANilgiris_total_projects = MasterSanctionForm.objects.filter(District__District="Nilgiris").filter(
            AgencyType__AgencyType='Municipality').count()
        CTPNilgiris_project_cost = MasterSanctionForm.objects.filter(District__District="Nilgiris").filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        CTPNilgiris_total_projects = MasterSanctionForm.objects.filter(District__District="Nilgiris").filter(
            AgencyType__AgencyType='Town Panchayat').count()

        DMAPudukkottai_project_cost = MasterSanctionForm.objects.filter(District__District="Pudukottai").filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        DMAPudukkottai_total_projects = MasterSanctionForm.objects.filter(District__District="Pudukottai").filter(
            AgencyType__AgencyType='Municipality').count()
        CTPPudukkottai_project_cost = MasterSanctionForm.objects.filter(District__District="Pudukottai").filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        CTPPudukkottai_total_projects = MasterSanctionForm.objects.filter(District__District="Pudukottai").filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Pudukkottai_project_cost = MasterSanctionForm.objects.filter(District__District="Pudukottai").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Pudukkottai_total_projects = MasterSanctionForm.objects.filter(District__District="Pudukottai").count()

        Ramanathapuram_project_cost = MasterSanctionForm.objects.filter(District__District="Ramanathapuram").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        DMARamanathapuram_project_cost = MasterSanctionForm.objects.filter(
            District__District="Ramanathapuram").filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        DMARamanathapuram_total_projects = MasterSanctionForm.objects.filter(
            District__District="Ramanathapuram").filter(
            AgencyType__AgencyType='Municipality').count()
        CTPRamanathapuram_project_cost = MasterSanctionForm.objects.filter(
            District__District="Ramanathapuram").filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        CTPRamanathapuram_total_projects = MasterSanctionForm.objects.filter(
            District__District="Ramanathapuram").filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Ramanathapuram_total_projects = MasterSanctionForm.objects.filter(District__District="Ramanathapuram").count()

        Ranipet_project_cost = MasterSanctionForm.objects.filter(District__District="Ranipet").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Ranipet_total_projects = MasterSanctionForm.objects.filter(District__District="Ranipet").count()
        DMARanipet_project_cost = MasterSanctionForm.objects.filter(District__District="Ranipet").filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        DMARanipet_total_projects = MasterSanctionForm.objects.filter(District__District="Ranipet").filter(
            AgencyType__AgencyType='Municipality').count()
        CTPRanipet_project_cost = MasterSanctionForm.objects.filter(District__District="Ranipet").filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        CTPRanipet_total_projects = MasterSanctionForm.objects.filter(District__District="Ranipet").filter(
            AgencyType__AgencyType='Town Panchayat').count()

        Salem_project_cost = MasterSanctionForm.objects.filter(District__District="Salem").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Salem_total_projects = MasterSanctionForm.objects.filter(District__District="Salem").count()
        DMASalem_project_cost = MasterSanctionForm.objects.filter(District__District="Salem").filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        DMASalem_total_projects = MasterSanctionForm.objects.filter(District__District="Salem").filter(
            AgencyType__AgencyType='Municipality').count()
        CTPSalem_project_cost = MasterSanctionForm.objects.filter(District__District="Salem").filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        CTPSalem_total_projects = MasterSanctionForm.objects.filter(District__District="Salem").filter(
            AgencyType__AgencyType='Town Panchayat').count()

        Tenkasi_project_cost = MasterSanctionForm.objects.filter(District__District="Tenkasi").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tenkasi_total_projects = MasterSanctionForm.objects.filter(District__District="Tenkasi").count()
        DMATenkasi_project_cost = MasterSanctionForm.objects.filter(District__District="Tenkasi").filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        DMATenkasi_total_projects = MasterSanctionForm.objects.filter(District__District="Tenkasi").filter(
            AgencyType__AgencyType='Municipality').count()
        CTPTenkasi_project_cost = MasterSanctionForm.objects.filter(District__District="Tenkasi").filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        CTPTenkasi_total_projects = MasterSanctionForm.objects.filter(District__District="Tenkasi").filter(
            AgencyType__AgencyType='Town Panchayat').count()

        Thanjavur_project_cost = MasterSanctionForm.objects.filter(District__District="Thanjavur").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thanjavur_total_projects = MasterSanctionForm.objects.filter(District__District="Thanjavur").count()
        DMAThanjavur_project_cost = MasterSanctionForm.objects.filter(District__District="Thanjavur").filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        DMAThanjavur_total_projects = MasterSanctionForm.objects.filter(District__District="Thanjavur").filter(
            AgencyType__AgencyType='Municipality').count()
        CTPThanjavur_project_cost = MasterSanctionForm.objects.filter(District__District="Thanjavur").filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        CTPThanjavur_total_projects = MasterSanctionForm.objects.filter(District__District="Thanjavur").filter(
            AgencyType__AgencyType='Town Panchayat').count()

        Theni_project_cost = MasterSanctionForm.objects.filter(District__District="Theni").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Theni_total_projects = MasterSanctionForm.objects.filter(District__District="Theni").count()
        DMATheni_project_cost = MasterSanctionForm.objects.filter(District__District="Theni").filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        DMATheni_total_projects = MasterSanctionForm.objects.filter(District__District="Theni").filter(
            AgencyType__AgencyType='Municipality').count()
        CTPTheni_project_cost = MasterSanctionForm.objects.filter(District__District="Theni").filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        CTPTheni_total_projects = MasterSanctionForm.objects.filter(District__District="Theni").filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Thirupathur_project_cost = MasterSanctionForm.objects.filter(District__District="Thirupathur").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thirupathur_total_projects = MasterSanctionForm.objects.filter(District__District="Thirupathur").count()
        DMAThirupathur_project_cost = MasterSanctionForm.objects.filter(District__District="Thirupathur").filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        DMAThirupathur_total_projects = MasterSanctionForm.objects.filter(District__District="Thirupathur").filter(
            AgencyType__AgencyType='Municipality').count()
        CTPThirupathur_project_cost = MasterSanctionForm.objects.filter(District__District="Thirupathur").filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        CTPThirupathur_total_projects = MasterSanctionForm.objects.filter(District__District="Thirupathur").filter(
            AgencyType__AgencyType='Town Panchayat').count()
        Thiruvallur_project_cost = MasterSanctionForm.objects.filter(District__District="Thiruvallur").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thiruvallur_total_projects = MasterSanctionForm.objects.filter(District__District="Thiruvallur").count()
        DMAThiruvallur_project_cost = MasterSanctionForm.objects.filter(District__District="Thiruvallur").filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        DMAThiruvallur_total_projects = MasterSanctionForm.objects.filter(District__District="Thiruvallur").filter(
            AgencyType__AgencyType='Municipality').count()
        CTPThiruvallur_project_cost = MasterSanctionForm.objects.filter(District__District="Thiruvallur").filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        CTPThiruvallur_total_projects = MasterSanctionForm.objects.filter(District__District="Thiruvallur").filter(
            AgencyType__AgencyType='Town Panchayat').count()

        Thiruvannamalai_project_cost = MasterSanctionForm.objects.filter(District__District="Tiruvannamalai").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thiruvannamalai_total_projects = MasterSanctionForm.objects.filter(District__District="Tiruvannamalai").count()
        DMAThiruvannamalai_project_cost = MasterSanctionForm.objects.filter(
            District__District="Tiruvannamalai").filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        DMAThiruvannamalai_total_projects = MasterSanctionForm.objects.filter(
            District__District="Tiruvannamalai").filter(
            AgencyType__AgencyType='Municipality').count()
        CTPThiruvannamalai_project_cost = MasterSanctionForm.objects.filter(
            District__District="Tiruvannamalai").filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        CTPThiruvannamalai_total_projects = MasterSanctionForm.objects.filter(
            District__District="Tiruvannamalai").filter(
            AgencyType__AgencyType='Town Panchayat').count()

        DMAThiruvarur_project_cost = MasterSanctionForm.objects.filter(
            District__District="Thiruvarur").filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        DMAThiruvarur_total_projects = MasterSanctionForm.objects.filter(
            District__District="Thiruvarur").filter(
            AgencyType__AgencyType='Municipality').count()
        CTPThiruvarur_project_cost = MasterSanctionForm.objects.filter(
            District__District="Thiruvarur").filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        CTPThiruvarur_total_projects = MasterSanctionForm.objects.filter(
            District__District="Thiruvarur").filter(
            AgencyType__AgencyType='Town Panchayat').count()

        Thiruvarur_project_cost = MasterSanctionForm.objects.filter(District__District="Thiruvarur").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thiruvarur_total_projects = MasterSanctionForm.objects.filter(District__District="Thiruvarur").count()

        DMAThoothukudi_project_cost = MasterSanctionForm.objects.filter(
            District__District="Thoothukudi").filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        DMAThoothukudi_total_projects = MasterSanctionForm.objects.filter(
            District__District="Thoothukudi").filter(
            AgencyType__AgencyType='Municipality').count()
        CTPThoothukudi_project_cost = MasterSanctionForm.objects.filter(
            District__District="Thoothukudi").filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        CTPThoothukudi_total_projects = MasterSanctionForm.objects.filter(
            District__District="Thoothukudi").filter(
            AgencyType__AgencyType='Town Panchayat').count()

        Thoothukudi_project_cost = MasterSanctionForm.objects.filter(District__District="Thoothukudi").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thoothukudi_total_projects = MasterSanctionForm.objects.filter(District__District="Thoothukudi").count()

        DMATiruchirappalli_project_cost = MasterSanctionForm.objects.filter(
            District__District="Tiruchirappalli").filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        DMATiruchirappalli_total_projects = MasterSanctionForm.objects.filter(
            District__District="Tiruchirappalli").filter(
            AgencyType__AgencyType='Municipality').count()
        CTPTiruchirappalli_project_cost = MasterSanctionForm.objects.filter(
            District__District="Tiruchirappalli").filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        CTPTiruchirappalli_total_projects = MasterSanctionForm.objects.filter(
            District__District="Tiruchirappalli").filter(
            AgencyType__AgencyType='Town Panchayat').count()

        Tiruchirappalli_project_cost = MasterSanctionForm.objects.filter(
            District__District="Tiruchirappalli").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tiruchirappalli_total_projects = MasterSanctionForm.objects.filter(District__District="Tiruchirappalli").count()

        DMATirunelveli_project_cost = MasterSanctionForm.objects.filter(
            District__District="Tirunelveli").filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        DMATirunelveli_total_projects = MasterSanctionForm.objects.filter(
            District__District="Tirunelveli").filter(
            AgencyType__AgencyType='Municipality').count()
        CTPTirunelveli_project_cost = MasterSanctionForm.objects.filter(
            District__District="Tirunelveli").filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        CTPTirunelveli_total_projects = MasterSanctionForm.objects.filter(
            District__District="Tirunelveli").filter(
            AgencyType__AgencyType='Town Panchayat').count()

        Tirunelveli_project_cost = MasterSanctionForm.objects.filter(District__District="Tirunelveli").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tirunelveli_total_projects = MasterSanctionForm.objects.filter(District__District="Tirunelveli").count()

        DMATirupathur_project_cost = MasterSanctionForm.objects.filter(
            District__District="Tirupathur").filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        DMATirupathur_total_projects = MasterSanctionForm.objects.filter(
            District__District="Tirupathur").filter(
            AgencyType__AgencyType='Municipality').count()
        CTPTirupathur_project_cost = MasterSanctionForm.objects.filter(
            District__District="Tirupathur").filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        CTPTirupathur_total_projects = MasterSanctionForm.objects.filter(
            District__District="Tirupathur").filter(
            AgencyType__AgencyType='Town Panchayat').count()

        Tirupathur_project_cost = MasterSanctionForm.objects.filter(District__District="Tirupathur").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tirupathur_total_projects = MasterSanctionForm.objects.filter(District__District="Tirupathur").count()

        DMATiruppur_project_cost = MasterSanctionForm.objects.filter(
            District__District="Tiruppur").filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        DMATiruppur_total_projects = MasterSanctionForm.objects.filter(
            District__District="Tiruppur").filter(
            AgencyType__AgencyType='Municipality').count()
        CTPTiruppur_project_cost = MasterSanctionForm.objects.filter(
            District__District="Tiruppur").filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        CTPTiruppur_total_projects = MasterSanctionForm.objects.filter(
            District__District="Tiruppur").filter(
            AgencyType__AgencyType='Town Panchayat').count()

        Tiruppur_project_cost = MasterSanctionForm.objects.filter(District__District="Tiruppur").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tiruppur_total_projects = MasterSanctionForm.objects.filter(District__District="Tiruppur").count()

        DMATrivallur_project_cost = MasterSanctionForm.objects.filter(
            District__District="Trivallur").filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        DMATrivallur_total_projects = MasterSanctionForm.objects.filter(
            District__District="Trivallur").filter(
            AgencyType__AgencyType='Municipality').count()
        CTPTrivallur_project_cost = MasterSanctionForm.objects.filter(
            District__District="Trivallur").filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        CTPTrivallur_total_projects = MasterSanctionForm.objects.filter(
            District__District="Trivallur").filter(
            AgencyType__AgencyType='Town Panchayat').count()

        Trivallur_project_cost = MasterSanctionForm.objects.filter(District__District="Trivallur").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Trivallur_total_projects = MasterSanctionForm.objects.filter(District__District="Trivallur").count()

        DMAVellore_project_cost = MasterSanctionForm.objects.filter(
            District__District="Vellore").filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        DMAVellore_total_projects = MasterSanctionForm.objects.filter(
            District__District="Vellore").filter(
            AgencyType__AgencyType='Municipality').count()
        CTPVellore_project_cost = MasterSanctionForm.objects.filter(
            District__District="Vellore").filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        CTPVellore_total_projects = MasterSanctionForm.objects.filter(
            District__District="Vellore").filter(
            AgencyType__AgencyType='Town Panchayat').count()

        Vellore_project_cost = MasterSanctionForm.objects.filter(District__District="Vellore").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Vellore_total_projects = MasterSanctionForm.objects.filter(District__District="Vellore").count()

        DMAVillupuram_project_cost = MasterSanctionForm.objects.filter(
            District__District="Villupuram").filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        DMAVillupuram_total_projects = MasterSanctionForm.objects.filter(
            District__District="Villupuram").filter(
            AgencyType__AgencyType='Municipality').count()
        CTPVillupuram_project_cost = MasterSanctionForm.objects.filter(
            District__District="Villupuram").filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        CTPVillupuram_total_projects = MasterSanctionForm.objects.filter(
            District__District="Villupuram").filter(
            AgencyType__AgencyType='Town Panchayat').count()

        Villupuram_project_cost = MasterSanctionForm.objects.filter(District__District="Villupuram").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Villupuram_total_projects = MasterSanctionForm.objects.filter(District__District="Villupuram").count()

        DMAVirudhunagar_project_cost = MasterSanctionForm.objects.filter(
            District__District="Virudhunagar").filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        DMAVirudhunagar_total_projects = MasterSanctionForm.objects.filter(
            District__District="Virudhunagar").filter(
            AgencyType__AgencyType='Municipality').count()
        CTPVirudhunagar_project_cost = MasterSanctionForm.objects.filter(
            District__District="Virudhunagar").filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
        CTPVirudhunagar_total_projects = MasterSanctionForm.objects.filter(
            District__District="Virudhunagar").filter(
            AgencyType__AgencyType='Town Panchayat').count()

        Virudhunagar_project_cost = MasterSanctionForm.objects.filter(District__District="Virudhunagar").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Virudhunagar_total_projects = MasterSanctionForm.objects.filter(District__District="Virudhunagar").count()
        district_info = District.objects.exclude(District='Chennai').all()

        busstand_approved_project_count = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector='Bus Stand').count()
        busstand_approved_project_cost = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector='Bus Stand').aggregate(project_cost=Sum('ApprovedProjectCost'))
        busstand_completed_count = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector='Bus Stand').filter(status='Completed').count()
        busstand_completed_approved_project_cost = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector='Bus Stand').filter(status='Completed').aggregate(project_cost=Sum('ApprovedProjectCost'))
        busstand_inprogress_count = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector='Bus Stand').filter(status='In Progress').count()
        busstand_inprogress_approved_project_cost = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector='Bus Stand').filter(status='In Progress').aggregate(project_cost=Sum('ApprovedProjectCost'))
        busstand_tobecommenced_count = busstand_approved_project_count-(busstand_completed_count+busstand_inprogress_count)
        busstand_tobecommenced_project_cost = round(float(busstand_approved_project_cost['project_cost']) - float(busstand_inprogress_approved_project_cost['project_cost']),2)

        busstand_district = AgencyProgressModel.objects.values('District').order_by('District').filter(Scheme='KNMT').filter(Sector='Bus Stand').filter(status='In Progress').annotate(percent = Sum('percentageofworkdone'))
        print(busstand_district)
        extra_context = {
            'busstand_district': busstand_district,
            'busstand_tobecommenced_count': busstand_tobecommenced_count,
            'busstand_tobecommenced_project_cost':busstand_tobecommenced_project_cost,
            'busstand_inprogress_count': busstand_inprogress_count,
            'busstand_inprogress_approved_project_cost': busstand_inprogress_approved_project_cost,

            'busstand_approved_project_cost':busstand_approved_project_cost,
            'busstand_completed_approved_project_cost':busstand_completed_approved_project_cost,
            'busstand_approved_project_count': busstand_approved_project_count,
            'busstand_completed_count': busstand_completed_count,
            'CTPVirudhunagar_total_projects': CTPVirudhunagar_total_projects,
            'CTPVirudhunagar_project_cost': CTPVirudhunagar_project_cost,
            'DMAVirudhunagar_total_projects': DMAVirudhunagar_total_projects,
            'DMAVirudhunagar_project_cost': DMAVirudhunagar_project_cost,
            'CTPVillupuram_total_projects': CTPVillupuram_total_projects,
            'CTPVillupuram_project_cost': CTPVillupuram_project_cost,
            'DMAVillupuram_total_projects': DMAVillupuram_total_projects,
            'DMAVillupuram_project_cost': DMAVillupuram_project_cost,
            'CTPVellore_total_projects': CTPVellore_total_projects,
            'CTPVellore_project_cost': CTPVellore_project_cost,
            'DMAVellore_total_projects': DMAVellore_total_projects,
            'DMAVellore_project_cost': DMAVellore_project_cost,
            'CTPTrivallur_total_projects': CTPTrivallur_total_projects,
            'CTPTrivallur_project_cost': CTPTrivallur_project_cost,
            'DMATrivallur_total_projects': DMATrivallur_total_projects,
            'DMATrivallur_project_cost': DMATrivallur_project_cost,
            'CTPTiruppur_total_projects': CTPTiruppur_total_projects,
            'CTPTiruppur_project_cost': CTPTiruppur_project_cost,
            'DMATiruppur_total_projects': DMATiruppur_total_projects,
            'DMATiruppur_project_cost': DMATiruppur_project_cost,
            'CTPTirupathur_total_projects': CTPTirupathur_total_projects,
            'CTPTirupathur_project_cost': CTPTirupathur_project_cost,
            'DMATirupathur_total_projects': DMATirupathur_total_projects,
            'DMATirupathur_project_cost': DMATirupathur_project_cost,
            'CTPTirunelveli_project_cost': CTPTirunelveli_project_cost,
            'CTPTirunelveli_total_projects': CTPTirunelveli_total_projects,
            'DMATirunelveli_total_projects': DMATirunelveli_total_projects,
            'DMATirunelveli_project_cost': DMATirunelveli_project_cost,
            'CTPTiruchirappalli_total_projects': CTPTiruchirappalli_total_projects,
            'CTPTiruchirappalli_project_cost': CTPTiruchirappalli_project_cost,
            'DMATiruchirappalli_total_projects': DMATiruchirappalli_total_projects,
            'DMATiruchirappalli_project_cost': DMATiruchirappalli_project_cost,
            'district_info': district_info,
            'CTPThoothukudi_total_projects': CTPThoothukudi_total_projects,
            'CTPThoothukudi_project_cost': CTPThoothukudi_project_cost,
            'DMAThoothukudi_total_projects': DMAThoothukudi_total_projects,
            'DMAThoothukudi_project_cost': DMAThoothukudi_project_cost,
            'CTPThiruvarur_total_projects': CTPThiruvarur_total_projects,
            'DMAThiruvarur_project_cost': DMAThiruvarur_project_cost,
            'DMAThiruvarur_total_projects': DMAThiruvarur_total_projects,
            'CTPThiruvarur_project_cost': CTPThiruvarur_project_cost,
            'DMAPudukkottai_project_cost': DMAPudukkottai_project_cost,
            'DMAPudukkottai_total_projects': DMAPudukkottai_total_projects,
            'CTPPudukkottai_project_cost': CTPPudukkottai_project_cost,
            'CTPPudukkottai_total_projects': CTPPudukkottai_total_projects,
            'DMANilgiris_project_cost': DMANilgiris_project_cost,
            'DMANilgiris_total_projects': DMANilgiris_total_projects,
            'CTPNilgiris_project_cost': CTPNilgiris_project_cost,
            'CTPNilgiris_total_projects': CTPNilgiris_total_projects,

            'DMARamanathapuram_project_cost': DMARamanathapuram_project_cost,
            'DMARamanathapuram_total_projects': DMARamanathapuram_total_projects,
            'CTPRamanathapuram_project_cost': CTPRamanathapuram_project_cost,
            'CTPRamanathapuram_total_projects': CTPRamanathapuram_total_projects,

            'DMARanipet_project_cost': DMARanipet_project_cost,
            'DMARanipet_total_projects': DMARanipet_total_projects,
            'CTPRanipet_project_cost': CTPRanipet_project_cost,
            'CTPRanipet_total_projects': CTPRanipet_total_projects,

            'DMASalem_project_cost': DMASalem_project_cost,
            'DMASalem_total_projects': DMASalem_total_projects,
            'CTPSalem_project_cost': CTPSalem_project_cost,
            'CTPSalem_total_projects': CTPSalem_total_projects,

            'DMATenkasi_project_cost': DMATenkasi_project_cost,
            'DMATenkasi_total_projects': DMATenkasi_total_projects,
            'CTPTenkasi_project_cost': CTPTenkasi_project_cost,
            'CTP Tenkasi_total_projects': CTPTenkasi_total_projects,

            'DMAThanjavur_project_cost': DMAThanjavur_project_cost,
            'DMAThanjavur_total_projects': DMAThanjavur_total_projects,
            'CTPThanjavur_project_cost': CTPThanjavur_project_cost,
            'CTPThanjavur_total_projects': CTPThanjavur_total_projects,

            'DMAThirupathur_project_cost': DMAThirupathur_project_cost,
            'DMAThirupathur_total_projects': DMAThirupathur_total_projects,
            'CTPThirupathur_project_cost': CTPThirupathur_project_cost,
            'CTPThirupathur_total_projects': CTPThirupathur_total_projects,

            'DMAThiruvallur_project_cost': DMAThiruvallur_project_cost,
            'DMAThiruvallur_total_projects': DMAThiruvallur_total_projects,
            'CTPThiruvallur_project_cost': CTPThiruvallur_project_cost,
            'CTPThiruvallur_total_projects': CTPThiruvallur_total_projects,

            'DMAThiruvannamalai_project_cost': DMAThiruvannamalai_project_cost,
            'DMAThiruvannamalai_total_projects': DMAThiruvannamalai_total_projects,
            'CTPThiruvannamalai_project_cost': CTPThiruvannamalai_project_cost,
            'CTPThiruvannamalai_total_projects': CTPThiruvannamalai_total_projects,

            'DMATheni_project_cost': DMATheni_project_cost,
            'DMATheni_total_projects': DMATheni_total_projects,
            'CTPTheni_project_cost': CTPTheni_project_cost,
            'CTPTheni_total_projects': CTPTheni_total_projects,

            'DMANamakkal_project_cost': DMANamakkal_project_cost,
            'DMANamakkal_total_projects': DMANamakkal_total_projects,
            'CTPNamakkal_project_cost': CTPNamakkal_project_cost,
            'CTPNamakkal_total_projects': CTPNamakkal_total_projects,

            'DMANagapattinam_project_cost': DMANagapattinam_project_cost,
            'DMANagapattinam_total_projects': DMANagapattinam_total_projects,
            'CTPNagapattinam_project_cost': CTPNagapattinam_project_cost,
            'CTPNagapattinam_total_projects': CTPNagapattinam_total_projects,

            'DMAMayiladuthurai_project_cost': DMAMayiladuthurai_project_cost,
            'DMAMayiladuthurai_total_projects': DMAMayiladuthurai_total_projects,
            'CTPMayiladuthurai_project_cost': CTPMayiladuthurai_project_cost,
            'CTPMayiladuthurai_total_projects': CTPMayiladuthurai_total_projects,

            'DMAMadurai_project_cost': DMAMadurai_project_cost,
            'DMAMadurai_total_projects': DMAMadurai_total_projects,
            'CTPMadurai_project_cost': CTPMadurai_project_cost,
            'CTPMadurai_total_projects': CTPMadurai_total_projects,

            'DMAKrishnagiri_project_cost': DMAKrishnagiri_project_cost,
            'DMAKrishnagiri_total_projects': DMAKrishnagiri_total_projects,
            'CTPKrishnagiri_project_cost': CTPKrishnagiri_project_cost,
            'CTPKrishnagiri_total_projects': CTPKrishnagiri_total_projects,

            'DMAKarur_project_cost': DMAKarur_project_cost,
            'DMAKarur_total_projects': DMAKarur_total_projects,
            'CTPKarur_project_cost': CTPKarur_project_cost,
            'CTPKarur_total_projects': CTPKarur_total_projects,

            'DMAKanyakumari_project_cost': DMAKanyakumari_project_cost,
            'DMAKanyakumari_total_projects': DMAKanyakumari_total_projects,
            'CTPKanyakumari_project_cost': CTPKanyakumari_project_cost,
            'CTPKanyakumari_total_projects': CTPKanyakumari_total_projects,

            'DMAKancheepuram_project_cost': DMAKancheepuram_project_cost,
            'DMAKancheepuram_total_projects': DMAKancheepuram_total_projects,
            'CTPKancheepuram_project_cost': CTPKancheepuram_project_cost,
            'CTPKancheepuram_total_projects': CTPKancheepuram_total_projects,

            'DMAKallakurichi_project_cost': DMAKallakurichi_project_cost,
            'DMAKallakurichi_total_projects': DMAKallakurichi_total_projects,
            'CTPKallakurichi_project_cost': CTPKallakurichi_project_cost,
            'CTPKallakurichi_total_projects': CTPKallakurichi_total_projects,

            'DMAErode_project_cost': DMAErode_project_cost,
            'DMAErode_total_projects': DMAErode_total_projects,
            'CTPErode_project_cost': CTPErode_project_cost,
            'CTPErode_total_projects': CTPErode_total_projects,

            'DMADindigul_project_cost': DMADindigul_project_cost,
            'DMADindigul_total_projects': DMADindigul_total_projects,
            'CTPDindigul_project_cost': CTPDindigul_project_cost,
            'CTPDindigul_total_projects': CTPDindigul_total_projects,

            'DMADharmapuri_project_cost': DMADharmapuri_project_cost,
            'DMADharmapuri_total_projects': DMADharmapuri_total_projects,
            'CTPDharmapuri_project_cost': CTPDharmapuri_project_cost,
            'CTPDharmapuri_total_projects': CTPDharmapuri_total_projects,

            'DMACuddalore_project_cost': DMACuddalore_project_cost,
            'DMACuddalore_total_projects': DMACuddalore_total_projects,
            'CTPCuddalore_project_cost': CTPCuddalore_project_cost,
            'CTPCuddalore_total_projects': CTPCuddalore_total_projects,
            'DMAAriyalur_project_cost': DMAAriyalur_project_cost,
            'DMAAriyalur_total_projects': DMAAriyalur_total_projects,
            'CTPAriyalur_project_cost': CTPAriyalur_project_cost,
            'CTPAriyalur_total_projects': CTPAriyalur_total_projects,
            'DMAChengalpattu_project_cost': DMAChengalpattu_project_cost,
            'DMAChengalpattu_total_projects': DMAChengalpattu_total_projects,
            'CTPChengalpattu_project_cost': CTPChengalpattu_project_cost,
            'CTPChengalpattu_total_projects': CTPChengalpattu_total_projects,
            'DMACoimbatore_project_cost': DMACoimbatore_project_cost,
            'DMACoimbatore_total_projects': DMACoimbatore_total_projects,
            'CTPCoimbatore_project_cost': CTPCoimbatore_project_cost,
            'CTPCoimbatore_total_projects': CTPCoimbatore_total_projects,
            'ulb_singara_share': ulb_singara_share,
            'ulb_share_ulb_singara': ulb_share_ulb_singara,
            'Vellore_project_cost': Vellore_project_cost,
            'Virudhunagar_project_cost': Virudhunagar_project_cost,
            'Virudhunagar_total_projects': Virudhunagar_total_projects,
            'Villupuram_project_cost': Villupuram_project_cost,
            'Villupuram_total_projects': Villupuram_total_projects,
            'Vellore_total_projects': Vellore_total_projects,
            'Trivallur_project_cost': Trivallur_project_cost,
            'Trivallur_total_projects': Trivallur_total_projects,
            'Tiruppur_project_cost': Tiruppur_project_cost,
            'Tiruppur_total_projects': Tiruppur_total_projects,
            'Tirupathur_project_cost': Tirupathur_project_cost,
            'Tirupathur_total_projects': Tirupathur_total_projects,
            'Tirunelveli_project_cost': Tirunelveli_project_cost,
            'Tirunelveli_total_projects': Tirunelveli_total_projects,
            'Tiruchirappalli_project_cost': Tiruchirappalli_project_cost,
            'Tiruchirappalli_total_projects': Tiruchirappalli_total_projects,
            'Thoothukudi_project_cost': Thoothukudi_project_cost,
            'Thoothukudi_total_projects': Thoothukudi_total_projects,
            'Thiruvarur_project_cost': Thiruvarur_project_cost,
            'Thiruvarur_total_projects': Thiruvarur_total_projects,
            'Thiruvannamalai_project_cost': Thiruvannamalai_project_cost,
            'Thiruvannamalai_total_projects': Thiruvannamalai_total_projects,

            'pie_chart_CTP': pie_chart_CTP,
            'donut_chart_CTP': donut_chart_CTP,
            'donut_chart_sectorDMA': donut_chart_sectorDMA,
            'pie_chart_sectorDMA': pie_chart_sectorDMA,
            'ulb_share_ulb': ulb_share_ulb,
            'ulb_knmt_share': ulb_knmt_share,
            'ulb_project_cost': ulb_project_cost,
            'ulb_total_project': ulb_total_project,
            'Thiruvallur_project_cost': Thiruvallur_project_cost,
            'Thiruvallur_total_projects': Thiruvallur_total_projects,
            'Thirupathur_project_cost': Thirupathur_project_cost,
            'Thirupathur_total_projects': Thirupathur_total_projects,
            'Theni_project_cost': Theni_project_cost,
            'Theni_total_projects': Theni_total_projects,
            'Thanjavur_project_cost': Thanjavur_project_cost,
            'Thanjavur_total_projects': Thanjavur_total_projects,
            'Tenkasi_project_cost': Tenkasi_project_cost,
            'Tenkasi_total_projects': Tenkasi_total_projects,
            'Salem_project_cost': Salem_project_cost,
            'Salem_total_projects': Salem_total_projects,
            'Ranipet_project_cost': Ranipet_project_cost,
            'Ranipet_total_projects': Ranipet_total_projects,
            'Ramanathapuram_project_cost': Ramanathapuram_project_cost,
            'Ramanathapuram_total_projects': Ramanathapuram_total_projects,
            'Pudukkottai_project_cost': Pudukkottai_project_cost,
            'Pudukkottai_total_projects': Pudukkottai_total_projects,
            'Perambalur_project_cost': Perambalur_project_cost,
            'Perambalur_total_projects': Perambalur_total_projects,
            'Nilgiris_project_cost': Nilgiris_project_cost,
            'Nilgiris_total_projects': Nilgiris_total_projects,
            'Namakkal_project_cost': Namakkal_project_cost,
            'Namakkal_total_projects': Namakkal_total_projects,
            'Nagapattinam_project_cost': Nagapattinam_project_cost,
            'Nagapattinam_total_projects': Nagapattinam_total_projects,
            'Mayiladuthurai_project_cost': Mayiladuthurai_project_cost,
            'Mayiladuthurai_total_projects': Mayiladuthurai_total_projects,
            'Madurai_project_cost': Madurai_project_cost,
            'Madurai_total_projects': Madurai_total_projects,
            'Krishnagiri_project_cost': Krishnagiri_project_cost,
            'Krishnagiri_total_projects': Krishnagiri_total_projects,
            'Karur_project_cost': Karur_project_cost,
            'Karur_total_projects': Karur_total_projects,
            'Kanyakumari_project_cost': Kanyakumari_project_cost,
            'Kanyakumari_total_projects': Kanyakumari_total_projects,
            'Kancheepuram_project_cost': Kancheepuram_project_cost,
            'Kancheepuram_total_projects': Kancheepuram_total_projects,
            'Kallakurichi_project_cost': Kallakurichi_project_cost,
            'Kallakurichi_total_projects': Kallakurichi_total_projects,
            'Erode_project_cost': Erode_project_cost,
            'Erode_total_projects': Erode_total_projects,
            'Dindigul_total_projects': Dindigul_total_projects,
            'Dindigul_project_cost': Dindigul_project_cost,
            'Dharmapuri_total_projects': Dharmapuri_total_projects,
            'Dharmapuri_project_cost': Dharmapuri_project_cost,
            'Cuddalore_total_projects': Cuddalore_total_projects,
            'Cuddalore_project_cost': Cuddalore_project_cost,
            'Ariyalur_total_projects': Ariyalur_total_projects,
            'Ariyalur_project_cost': Ariyalur_project_cost,
            'Chengalpattu_project_cost': Chengalpattu_project_cost,
            'Chengalpattu_total_projects': Chengalpattu_total_projects,
            'total_projects': total_projects,
            'project_cost': project_cost,
            'knmt': knmt,
            'ulb_share': ulb_share,
            'dmp_total_projects': dmp_total_projects,
            'dmp_knmt': dmp_knmt,
            'dmp_project_cost': dmp_project_cost,
            'dmp_ulb_share': dmp_ulb_share,
            'ctp_total_projects': ctp_total_projects,
            'ctp_project_cost': ctp_project_cost,
            'ctp_knmt': ctp_knmt,
            'ctp_ulb_share': ctp_ulb_share,
            'road': road,
            'roadDMA': roadDMA,
            'roadCTP': roadCTP,
            'road_total': road_total,
            'roadDMA_total': roadDMA_total,
            'roadCTP_total': roadCTP_total,
            'busstand': busstand,
            'busstand_total': busstand_total,
            'busstandDMA': busstandDMA,
            'busstandDMA_total': busstandDMA_total,
            'busstandCTP': busstandCTP,
            'busstandCTP_total': busstandCTP_total,
            'ch': ch,
            'ch_total': ch_total,
            'chDMA': chDMA,
            'chDMA_total': chDMA_total,
            'chCTP': chCTP,
            'chCTP_total': chCTP_total,
            'crematorium': crematorium,
            'crematorium_total': crematorium_total,
            'crematoriumDMA': crematoriumDMA,
            'crematoriumDMA_total': crematoriumDMA_total,
            'crematoriumCTP': crematoriumCTP,
            'crematoriumCTP_total': crematoriumCTP_total,
            'KC': KC,
            'KC_total': KC_total,
            'KCDMA': KCDMA,
            'KCDMA_total': KCDMA_total,
            'KCCTP': KCCTP,
            'KCCTP_total': KCCTP_total,
            'market': market,
            'market_total': market_total,
            'marketDMA': marketDMA,
            'marketDMA_total': marketDMA_total,
            'marketCTP': marketCTP,
            'marketCTP_total': marketCTP_total,
            'park': park,
            'park_total': park_total,
            'parkDMA': parkDMA,
            'parkDMA_total': parkDMA_total,
            'parkCTP': parkCTP,
            'parkCTP_total': parkCTP_total,
            'SWM': SWM,
            'SWM_total': SWM_total,
            'SWMDMA': SWMDMA,
            'SWMDMA_total': SWMDMA_total,
            'SWMCTP': SWMCTP,
            'SWMCTP_total': SWMCTP_total,
            'WB': WB,
            'WB_total': WB_total,
            'WBDMA': WBDMA,
            'WBDMA_total': WBDMA_total,
            'WBCTP': WBCTP,
            'WBCTP_total': WBCTP_total,
            "busstand_percentage": busstand_percentage,
            "ch_percent": ch_percent,
            'crematorium_pt': crematorium_pt,
            "KC_pt": KC_pt,
            "market_pt": market_pt,
            'park_pt': park_pt,
            'SWM_pt': SWM_pt,
            'WB_pt': WB_pt,
            'road_pt': road_pt,
            'DMAbusstand_percentage': DMAbusstand_percentage,
            'DMAch_percent': DMAch_percent,
            'DMAcrematorium_pt': DMAcrematorium_pt,
            'DMAKC_pt': DMAKC_pt,
            'DMAmarket_pt': DMAmarket_pt,
            'DMApark_pt': DMApark_pt,
            'DMAroad_pt': DMAroad_pt,
            'DMASWM_pt': DMASWM_pt,
            'DMAWB_pt': DMAWB_pt,
            'DMA_total_percent': DMA_total_percent,
            'CTPbusstand_percentage': CTPbusstand_percentage,
            'CTPch_percent': CTPch_percent,
            'CTPcrematorium_pt': CTPcrematorium_pt,
            'CTPKC_pt': CTPKC_pt,
            'CTPmarket_pt': CTPmarket_pt,
            'CTPpark_pt': CTPpark_pt,
            'CTProad_pt': CTProad_pt,
            'CTPSWM_pt': CTPSWM_pt,
            'CTPWB_pt': CTPWB_pt,
            'CTP_total_percent': CTP_total_percent,
            'pie_chart_sector': pie_chart_sector,
            'donut_chart_sector': donut_chart_sector,
            'Coimbatore_project_cost': Coimbatore_project_cost,
            'Coimbatore_total_projects': Coimbatore_total_projects
        }

        response.context_data.update(extra_context)
        return response

admin.site.register(PageCounter)