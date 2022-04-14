import functools
from urllib import request
from django.contrib import admin
from django.contrib.admin import AdminSite
import json
from django.db.models import Count, Sum, Avg, Func
from import_export.admin import ImportExportModelAdmin
from .resources import *
from .forms import *
import pickle
from django.db.models import Q
from ULBForms.models import AgencyBankDetails

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


admin.site.register(About)


class SchemeAdmin(ImportExportModelAdmin, admin.AdminSite):
    model = Scheme

    list_display = [
        'Scheme'
    ]


admin.site.register(Scheme, SchemeAdmin)

admin.site.register(SchemeSanctionPdf)


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


class FundReleaseDetailsAdmin(admin.StackedInline):
    model = FundReleaseDetails
    extra = 5


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


admin.site.register(ULBReleaseRequest)

admin.site.register(PageCounter)


@admin.register(ReleaseRequestModel)
class ReleaseRequestAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (('Scheme', 'ULBType', 'ULBName'), ('Sector', 'Project_ID'))
        }),
        (
            'Bank Details', {
                'fields': ('bank_name_ulb',
                           'bank_branch_name',
                           'bank_branch',
                           'account_number',
                           'ifsc_code')
            }
        ),
        (
            'Fund Release Details', {
                'fields': (
                    (
                        'release1Date',
                        'release1Amount',
                    ), (
                        'release2Date',
                        'release2Amount',
                        'sqm_report2',
                    ), (
                        'release3Date',
                        'release3Amount',
                        'sqm_report3',
                    ), (
                        'release4Date',
                        'release4Amount',
                        'sqm_report4',
                    ), (
                        'release5Date',
                        'release5Amount',
                        'sqm_report5'
                    )
                )
            }
        )
    )

    def save_model(self, request, obj, form, change):
        obj.account_number = AgencyBankDetails.objects.values_list('account_number', flat=True).filter(
            user__first_name=form.cleaned_data['ULBName'])
        obj.bank_name_ulb = AgencyBankDetails.objects.values_list('beneficiary_name', flat=True).filter(
            user__first_name=form.cleaned_data['ULBName'])
        obj.bank_branch_name = AgencyBankDetails.objects.values_list('bank_name', flat=True).filter(
            user__first_name=form.cleaned_data['ULBName'])
        obj.bank_branch = AgencyBankDetails.objects.values_list('branch', flat=True).filter(
            user__first_name=form.cleaned_data['ULBName'])
        obj.ifsc_code = AgencyBankDetails.objects.values_list('IFSC_code', flat=True).filter(
            user__first_name=form.cleaned_data['ULBName'])
        obj.Sector = MasterSanctionForm.objects.values_list('Sector', flat=True).filter(
            Sector=form.cleaned_data['Sector']
        )
        obj.save()
