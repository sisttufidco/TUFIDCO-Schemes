import functools
from urllib import request
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.db.models import Count, Sum
from import_export.admin import ImportExportModelAdmin
from mapbox_location_field.admin import MapAdmin
from .resources import *
from .forms import *

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


@admin.register(Dashboard)
class DashboardAdmin(admin.ModelAdmin):
    change_list_template = "admin/dashboard.html"

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

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
                        'Metal Beam Crash Barriers']).annotate(**metrics_project).order_by('Sector'))

        response.context_data['sectorbarchartDMA'] = list(qs.values('Sector').exclude(
            Sector__in=['BT Road', 'CC Road', 'Retaining wall', 'Paver Block', 'SWD', 'Culvert', 'Metal Beam Crash Barriers']).filter(
            AgencyType__AgencyType='Municipality').annotate(**metrics_project).order_by('Sector'))

        response.context_data['sectorbarchartCTP'] = list(qs.values('Sector').exclude(
            Sector__in=['BT Road', 'CC Road', 'Retaining wall', 'Paver Block', 'SWD', 'Culvert', 'Metal Beam Crash Barriers']).filter(
            AgencyType__AgencyType='Town Panchayat').annotate(**metrics_project).order_by('Sector'))

        response.context_data['piechart'] = list(qs.values('Sector').annotate(**metrics).order_by('Sector'))
        response.context_data['ulbpiechart'] = list(
            qs.values('Sector').filter(AgencyName__AgencyName=request.user.first_name).annotate(**ulb_metrics).order_by(
                'ApprovedProjectCost'))
        response.context_data['ulbdonutchart'] = list(
            qs.values('Sector').filter(AgencyName__AgencyName=request.user.first_name).annotate(**ulb_metrics).order_by(
                'ulb_works'))

        road = MasterSanctionForm.objects.filter(
            Sector__in=['BT Road', 'CC Road', 'Retaining wall', 'Paver Block', 'SWD', 'Culvert',
                        'Metal Beam Crash Barriers']).aggregate(project_cost=Sum('ApprovedProjectCost'))
        road_total = MasterSanctionForm.objects.filter(
            Sector__in=['BT Road', 'CC Road', 'Retaining wall', 'Paver Block', 'SWD', 'Culvert', 'Metal Beam Crash Barriers']).count()
        roadDMA = MasterSanctionForm.objects.filter(
            Sector__in=['BT Road', 'CC Road', 'Retaining wall', 'Paver Block', 'SWD', 'Culvert', 'Metal Beam Crash Barriers']).filter(
            AgencyType__AgencyType="Municipality").aggregate(project_cost=Sum('ApprovedProjectCost'))
        roadDMA_total = MasterSanctionForm.objects.filter(
            Sector__in=['BT Road', 'CC Road', 'Retaining wall', 'Paver Block', 'SWD', 'Culvert', 'Metal Beam Crash Barriers']).filter(
            AgencyType__AgencyType="Municipality").count()
        roadCTP = MasterSanctionForm.objects.filter(
            Sector__in=['BT Road', 'CC Road', 'Retaining wall', 'Paver Block', 'SWD', 'Culvert', 'Metal Beam Crash Barriers']).filter(
            AgencyType__AgencyType="Town Panchayat").aggregate(project_cost=Sum('ApprovedProjectCost'))
        roadCTP_total = MasterSanctionForm.objects.filter(
            Sector__in=['BT Road', 'CC Road', 'Retaining wall', 'Paver Block', 'SWD', 'Culvert', 'Metal Beam Crash Barriers']).filter(
            AgencyType__AgencyType="Town Panchayat").count()

        busstand = MasterSanctionForm.objects.filter(Sector__in=['Bus Stand']).aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        busstand_total = MasterSanctionForm.objects.filter(Sector__in=['Bus Stand']).count()
        busstandDMA = MasterSanctionForm.objects.filter(Sector__in=['Bus Stand']).filter(
            AgencyType__AgencyType="Municipality").aggregate(project_cost=Sum('ApprovedProjectCost'))
        busstandDMA_total = MasterSanctionForm.objects.filter(Sector__in=['Bus Stand']).filter(
            AgencyType__AgencyType="Municipality").count()
        busstandCTP = MasterSanctionForm.objects.filter(Sector__in=['Bus Stand']).filter(
            AgencyType__AgencyType="Town Panchayat").aggregate(project_cost=Sum('ApprovedProjectCost'))
        busstandCTP_total = MasterSanctionForm.objects.filter(Sector__in=['Bus Stand']).filter(
            AgencyType__AgencyType="Town Panchayat").count()

        ch = MasterSanctionForm.objects.filter(Sector__in=['Community Hall']).aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        ch_total = MasterSanctionForm.objects.filter(Sector__in=['Community Hall']).count()
        chDMA = MasterSanctionForm.objects.filter(Sector__in=['Community Hall']).filter(
            AgencyType__AgencyType="Municipality").aggregate(project_cost=Sum('ApprovedProjectCost'))
        chDMA_total = MasterSanctionForm.objects.filter(Sector__in=['Community Hall']).filter(
            AgencyType__AgencyType="Municipality").count()
        chCTP = MasterSanctionForm.objects.filter(Sector="Community Hall").filter(
            AgencyType__AgencyType="Town Panchayat").aggregate(project_cost=Sum('ApprovedProjectCost'))
        chCTP_total = MasterSanctionForm.objects.filter(Sector__in=['Community Hall']).filter(
            AgencyType__AgencyType="Town Panchayat").count()

        crematorium = MasterSanctionForm.objects.filter(Sector__in=['Crematorium']).aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        crematorium_total = MasterSanctionForm.objects.filter(Sector__in=['Crematorium']).count()
        crematoriumDMA = MasterSanctionForm.objects.filter(Sector__in=['Crematorium']).filter(
            AgencyType__AgencyType="Municipality").aggregate(project_cost=Sum('ApprovedProjectCost'))
        crematoriumDMA_total = MasterSanctionForm.objects.filter(Sector__in=['Crematorium']).filter(
            AgencyType__AgencyType="Municipality").count()
        crematoriumCTP = MasterSanctionForm.objects.filter(Sector__in=['Crematorium']).filter(
            AgencyType__AgencyType="Town Panchayat").aggregate(project_cost=Sum('ApprovedProjectCost'))
        crematoriumCTP_total = MasterSanctionForm.objects.filter(Sector__in=['Crematorium']).filter(
            AgencyType__AgencyType="Town Panchayat").count()

        KC = MasterSanctionForm.objects.filter(Sector__in=['Knowledge Centre']).aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        KC_total = MasterSanctionForm.objects.filter(Sector__in=['Knowledge Centre']).count()
        KCDMA = MasterSanctionForm.objects.filter(Sector__in=['Knowledge Centre']).filter(
            AgencyType__AgencyType="Municipality").aggregate(project_cost=Sum('ApprovedProjectCost'))
        KCDMA_total = MasterSanctionForm.objects.filter(Sector__in=['Knowledge Centre']).filter(
            AgencyType__AgencyType="Municipality").count()
        KCCTP = MasterSanctionForm.objects.filter(Sector__in=['Knowledge Centre']).filter(
            AgencyType__AgencyType="Town Panchayat").aggregate(project_cost=Sum('ApprovedProjectCost'))
        KCCTP_total = MasterSanctionForm.objects.filter(Sector__in=['Knowledge Centre']).filter(
            AgencyType__AgencyType="Town Panchayat").count()

        market = MasterSanctionForm.objects.filter(Sector__in=['Market']).aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        market_total = MasterSanctionForm.objects.filter(Sector__in=['Market']).count()
        marketDMA = MasterSanctionForm.objects.filter(Sector__in=['Market']).filter(
            AgencyType__AgencyType="Municipality").aggregate(project_cost=Sum('ApprovedProjectCost'))
        marketDMA_total = MasterSanctionForm.objects.filter(Sector__in=['Market']).filter(
            AgencyType__AgencyType="Municipality").count()
        marketCTP = MasterSanctionForm.objects.filter(Sector__in=['Market']).filter(
            AgencyType__AgencyType="Town Panchayat").aggregate(project_cost=Sum('ApprovedProjectCost'))
        marketCTP_total = MasterSanctionForm.objects.filter(Sector__in=['Market']).filter(
            AgencyType__AgencyType="Town Panchayat").count()

        park = MasterSanctionForm.objects.filter(Sector__in=['Parks']).aggregate(project_cost=Sum('ApprovedProjectCost'))
        park_total = MasterSanctionForm.objects.filter(Sector__in=['Parks']).count()
        parkDMA = MasterSanctionForm.objects.filter(Sector__in=['Parks']).filter(
            AgencyType__AgencyType="Municipality").aggregate(project_cost=Sum('ApprovedProjectCost'))
        parkDMA_total = MasterSanctionForm.objects.filter(Sector__in=['Parks']).filter(
            AgencyType__AgencyType="Municipality").count()
        parkCTP = MasterSanctionForm.objects.filter(Sector__in=['Parks']).filter(
            AgencyType__AgencyType="Town Panchayat").aggregate(project_cost=Sum('ApprovedProjectCost'))
        parkCTP_total = MasterSanctionForm.objects.filter(Sector__in=['Parks']).filter(
            AgencyType__AgencyType="Town Panchayat").count()

        SWM = MasterSanctionForm.objects.filter(Sector__in=['Solid Waste Mgt.']).aggregate(project_cost=Sum('ApprovedProjectCost'))
        SWM_total = MasterSanctionForm.objects.filter(Sector__in=['Solid Waste Mgt.']).count()
        SWMDMA = MasterSanctionForm.objects.filter(Sector__in=['Solid Waste Mgt.']).filter(
            AgencyType__AgencyType="Municipality").aggregate(project_cost=Sum('ApprovedProjectCost'))
        SWMDMA_total = MasterSanctionForm.objects.filter(Sector__in=['Solid Waste Mgt.']).filter(
            AgencyType__AgencyType="Municipality").count()
        SWMCTP = MasterSanctionForm.objects.filter(Sector__in=['Solid Waste Mgt.']).filter(
            AgencyType__AgencyType="Town Panchayat").aggregate(project_cost=Sum('ApprovedProjectCost'))
        SWMCTP_total = MasterSanctionForm.objects.filter(Sector__in=['Solid Waste Mgt.']).filter(
            AgencyType__AgencyType="Town Panchayat").count()

        WB = MasterSanctionForm.objects.filter(Sector__in=['Water Bodies']).aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        WB_total = MasterSanctionForm.objects.filter(Sector__in=['Water Bodies']).count()
        WBDMA = MasterSanctionForm.objects.filter(Sector__in=['Water Bodies']).filter(
            AgencyType__AgencyType="Municipality").aggregate(project_cost=Sum('ApprovedProjectCost'))
        WBDMA_total = MasterSanctionForm.objects.filter(Sector__in=['Water Bodies']).filter(
            AgencyType__AgencyType="Municipality").count()
        WBCTP = MasterSanctionForm.objects.filter(Sector="Water Bodies").filter(
            AgencyType__AgencyType="Town Panchayat").aggregate(project_cost=Sum('ApprovedProjectCost'))
        WBCTP_total = MasterSanctionForm.objects.filter(Sector__in=['Water Bodies']).filter(
            AgencyType__AgencyType="Town Panchayat").count()

        total_projects = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').count()
        project_cost = MasterSanctionForm.objects.aggregate(project_cost=Sum('ApprovedProjectCost'))

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
            AgencyType__AgencyType='Municipality').aggregate(dmp_project_cost=Sum('ApprovedProjectCost'))
        ctp_project_cost = MasterSanctionForm.objects.filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(ctp_project_cost=Sum('ApprovedProjectCost'))

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
        ctp_total_projects = MasterSanctionForm.objects.filter(AgencyType__AgencyType='Town Panchayat').count()
        ctp_project_cost = MasterSanctionForm.objects.filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(ctp_project_cost=Sum('ApprovedProjectCost'))
        ctp_knmt = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(ctp_knmt=Sum('SchemeShare'))
        ctp_ulb_share = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(ctp_ulb_share=Sum('ULBShare'))

        ulb_total_project = MasterSanctionForm.objects.filter(AgencyName__AgencyName=request.user.first_name).count()
        ulb_project_cost = MasterSanctionForm.objects.filter(AgencyName__AgencyName=request.user.first_name).aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        ulb_knmt_share = MasterSanctionForm.objects.filter(AgencyName__AgencyName=request.user.first_name).filter(
            Scheme__Scheme='KNMT').aggregate(knmt_share=Sum('SchemeShare'))
        ulb_share_ulb = MasterSanctionForm.objects.filter(AgencyName__AgencyName=request.user.first_name).filter(
            Scheme__Scheme='KNMT').aggregate(ulb_share=Sum('ULBShare'))

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


        Perambalur_project_cost = MasterSanctionForm.objects.filter(District__District="Perambalur").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Perambalur_total_projects = MasterSanctionForm.objects.filter(District__District="Perambalur").count()
        coimbatore_project_cost = MasterSanctionForm.objects.filter(District__District="Coimbatore").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        coimbatore_total_projects = MasterSanctionForm.objects.filter(District__District="Coimbatore").count()
        Chengalpattu_project_cost = MasterSanctionForm.objects.filter(District__District="Chengalpattu").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Chengalpattu_total_projects = MasterSanctionForm.objects.filter(District__District="Chengalpattu").count()
        Ariyalur_project_cost = MasterSanctionForm.objects.filter(District__District="Ariyalur").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Ariyalur_total_projects = MasterSanctionForm.objects.filter(District__District="Ariyalur").count()
        Chengalpet_project_cost = MasterSanctionForm.objects.filter(District__District="Chengalpet").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Chengalpet_total_projects = MasterSanctionForm.objects.filter(District__District="Chengalpet").count()
        Cuddalore_project_cost = MasterSanctionForm.objects.filter(District__District="Cuddalore").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Cuddalore_total_projects = MasterSanctionForm.objects.filter(District__District="Cuddalore").count()
        Dharmapuri_project_cost = MasterSanctionForm.objects.filter(District__District="Dharmapuri").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Dharmapuri_total_projects = MasterSanctionForm.objects.filter(District__District="Dharmapuri").count()
        Dindigul_project_cost = MasterSanctionForm.objects.filter(District__District="Dindigul").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Dindigul_total_projects = MasterSanctionForm.objects.filter(District__District="Dindigul").count()
        Erode_project_cost = MasterSanctionForm.objects.filter(District__District="Erode").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Erode_total_projects = MasterSanctionForm.objects.filter(District__District="Erode").count()
        Kallakurichi_project_cost = MasterSanctionForm.objects.filter(District__District="Kallakurichi").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Kallakurichi_total_projects = MasterSanctionForm.objects.filter(District__District="Kallakurichi").count()
        Kancheepuram_project_cost = MasterSanctionForm.objects.filter(District__District="Kancheepuram").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Kancheepuram_total_projects = MasterSanctionForm.objects.filter(District__District="Kancheepuram").count()
        Kanyakumari_project_cost = MasterSanctionForm.objects.filter(District__District="Kanyakumari").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Kanyakumari_total_projects = MasterSanctionForm.objects.filter(District__District="Kanyakumari").count()
        Karur_project_cost = MasterSanctionForm.objects.filter(District__District="Karur").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Karur_total_projects = MasterSanctionForm.objects.filter(District__District="Krishnagiri").count()
        Krishnagiri_project_cost = MasterSanctionForm.objects.filter(District__District="Krishnagiri").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Krishnagiri_total_projects = MasterSanctionForm.objects.filter(District__District="Krishnagiri").count()
        Madurai_project_cost = MasterSanctionForm.objects.filter(District__District="Madurai").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Madurai_total_projects = MasterSanctionForm.objects.filter(District__District="Madurai").count()
        Mayiladuthurai_project_cost = MasterSanctionForm.objects.filter(District__District="Mayiladuthurai").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Mayiladuthurai_total_projects = MasterSanctionForm.objects.filter(District__District="Mayiladuthurai").count()
        Nagapattinam_project_cost = MasterSanctionForm.objects.filter(District__District="Nagapattinam").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Nagapattinam_total_projects = MasterSanctionForm.objects.filter(District__District="Nagapattinam").count()
        Namakkal_project_cost = MasterSanctionForm.objects.filter(District__District="Namakkal").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Namakkal_total_projects = MasterSanctionForm.objects.filter(District__District="Namakkal").count()
        Nilgiris_project_cost = MasterSanctionForm.objects.filter(District__District="Nilgiris").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Nilgiris_total_projects = MasterSanctionForm.objects.filter(District__District="Nilgiris").count()
        Pudukkottai_project_cost = MasterSanctionForm.objects.filter(District__District="Pudukkottai").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Pudukkottai_total_projects = MasterSanctionForm.objects.filter(District__District="Pudukkottai").count()
        Ramanathapuram_project_cost = MasterSanctionForm.objects.filter(District__District="Ramanathapuram").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Ramanathapuram_total_projects = MasterSanctionForm.objects.filter(District__District="Ramanathapuram").count()
        Ranipet_project_cost = MasterSanctionForm.objects.filter(District__District="Ranipet").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Ranipet_total_projects = MasterSanctionForm.objects.filter(District__District="Ranipet").count()
        Salem_project_cost = MasterSanctionForm.objects.filter(District__District="Salem").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Salem_total_projects = MasterSanctionForm.objects.filter(District__District="Salem").count()
        Tenkasi_project_cost = MasterSanctionForm.objects.filter(District__District="Tenkasi").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tenkasi_total_projects = MasterSanctionForm.objects.filter(District__District="Tenkasi").count()
        Thanjavur_project_cost = MasterSanctionForm.objects.filter(District__District="Thanjavur").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thanjavur_total_projects = MasterSanctionForm.objects.filter(District__District="Thanjavur").count()
        Theni_project_cost = MasterSanctionForm.objects.filter(District__District="Theni").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Theni_total_projects = MasterSanctionForm.objects.filter(District__District="Theni").count()
        Thirupathur_project_cost = MasterSanctionForm.objects.filter(District__District="Thirupathur").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thirupathur_total_projects = MasterSanctionForm.objects.filter(District__District="Thirupathur").count()
        Thiruvallur_project_cost = MasterSanctionForm.objects.filter(District__District="Thiruvallur").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thiruvallur_total_projects = MasterSanctionForm.objects.filter(District__District="Thiruvallur").count()
        Thiruvannamalai_project_cost = MasterSanctionForm.objects.filter(District__District="Tiruvannamalai").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thiruvannamalai_total_projects = MasterSanctionForm.objects.filter(District__District="Tiruvannamalai").count()
        Thiruvarur_project_cost = MasterSanctionForm.objects.filter(District__District="Thiruvarur").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thiruvarur_total_projects = MasterSanctionForm.objects.filter(District__District="Thiruvarur").count()	
        Thoothukudi_project_cost = MasterSanctionForm.objects.filter(District__District="Thoothukudi").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Thoothukudi_total_projects = MasterSanctionForm.objects.filter(District__District="Thoothukudi").count()
        Tiruchirappalli_project_cost = MasterSanctionForm.objects.filter(District__District="Tiruchirappalli").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tiruchirappalli_total_projects = MasterSanctionForm.objects.filter(District__District="Tiruchirappalli").count()
        Tirunelveli_project_cost = MasterSanctionForm.objects.filter(District__District="Tirunelveli").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tirunelveli_total_projects = MasterSanctionForm.objects.filter(District__District="Tirunelveli").count()
        Tirupathur_project_cost = MasterSanctionForm.objects.filter(District__District="Tirupathur").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tirupathur_total_projects = MasterSanctionForm.objects.filter(District__District="Tirupathur").count()
        Tiruppur_project_cost = MasterSanctionForm.objects.filter(District__District="Tiruppur").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Tiruppur_total_projects = MasterSanctionForm.objects.filter(District__District="Tiruppur").count()
        Trichy_project_cost = MasterSanctionForm.objects.filter(District__District="Trichy").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Trichy_total_projects = MasterSanctionForm.objects.filter(District__District="Trichy").count()
        Trivallur_project_cost = MasterSanctionForm.objects.filter(District__District="Trivallur").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Trivallur_total_projects = MasterSanctionForm.objects.filter(District__District="Trivallur").count()
        Vellore_project_cost = MasterSanctionForm.objects.filter(District__District="Vellore").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Vellore_total_projects = MasterSanctionForm.objects.filter(District__District="Vellore").count()
        Villupuram_project_cost = MasterSanctionForm.objects.filter(District__District="Villupuram").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Villupuram_total_projects = MasterSanctionForm.objects.filter(District__District="Villupuram").count()
        Virudhunagar_project_cost = MasterSanctionForm.objects.filter(District__District="Virudhunagar").aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        Virudhunagar_total_projects = MasterSanctionForm.objects.filter(District__District="Virudhunagar").count()

        extra_context = {
            'Vellore_project_cost':Vellore_project_cost,
            'Virudhunagar_project_cost':Virudhunagar_project_cost,
            'Virudhunagar_total_projects':Virudhunagar_total_projects,
            'Villupuram_project_cost':Villupuram_project_cost,
            'Villupuram_total_projects':Villupuram_total_projects,
            'Vellore_total_projects':Vellore_total_projects,
            'Trivallur_project_cost':Trivallur_project_cost,
            'Trivallur_total_projects':Trivallur_total_projects,
            'Trichy_project_cost':Trichy_project_cost,
            'Trichy_total_projects':Trichy_total_projects,
            'Tiruppur_project_cost':Tiruppur_project_cost,
            'Tiruppur_total_projects':Tiruppur_total_projects,
            'Tirupathur_project_cost':Tirupathur_project_cost,
            'Tirupathur_total_projects':Tirupathur_total_projects,
            'Tirunelveli_project_cost': Tirunelveli_project_cost,
            'Tirunelveli_total_projects': Tirunelveli_total_projects,
            'Tiruchirappalli_project_cost':Tiruchirappalli_project_cost,
            'Tiruchirappalli_total_projects': Tiruchirappalli_total_projects,
            'Thoothukudi_project_cost':Thoothukudi_project_cost,
            'Thoothukudi_total_projects':Thoothukudi_total_projects,
            'Thiruvarur_project_cost':Thiruvarur_project_cost,
            'Thiruvarur_total_projects':Thiruvarur_total_projects,
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
            'Chengalpet_total_projects': Chengalpet_total_projects,
            'Chengalpet_project_cost': Chengalpet_project_cost,
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
            'coimbatore_project_cost': coimbatore_project_cost,
            'coimbatore_total_projects': coimbatore_total_projects
        }

        response.context_data.update(extra_context)
        return response


"""
    Agency admin
"""





class AgencyBankDetailsAdmin(admin.ModelAdmin):
    change_form_template = 'admin/bankagencydetails.html'

    exclude = ['user']

    readonly_fields = ['passbook_preview']

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
        'status'
    ]

    def save_model(self, request, obj, form, change):
        if request.user.groups.filter(name__in=['Agency']).exists():
            obj.user = request.user
            obj.ProjectName = MasterSanctionForm.objects.values_list('ProjectName', flat=True).filter(Project_ID=form.cleaned_data['Project_ID'])
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
    fields = (('Scheme', 'Sector', 'Project_ID'),'ts_awarded', 'tsrefno', 'tsdate', 'tr_awarded', 'tawddate', 'wd_awarded', 'wdawddate')

    list_filter = [
        'ts_awarded',
        'tr_awarded',
        'wd_awarded'
    ]

    
    def save_model(self, request, obj, form, change):
        if request.user.groups.filter(name__in=['Agency']).exists():
            obj.user =  request.user
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
        BT_Road_SchemeShare = MasterSanctionForm.objects.filter(Scheme__Scheme="KNMT").filter(Sector="BT Road").aggregate(BT_Road_SchemeShare = Sum('SchemeShare'))
        BT_Road_ULBShare = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector='BT Road').aggregate(BT_Road_ULBShare=Sum('ULBShare'))
        BT_Road_Total = BT_Road_SchemeShare['BT_Road_SchemeShare'] + BT_Road_ULBShare['BT_Road_ULBShare']
        BT_Road_Approved = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector='BT Road').count()
        BT_Road_Completed = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector='BT Road').filter(status='Completed').count()
        BT_Road_inprogress = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector='BT Road').filter(status='In Progress').count()
        BT_Road_Taken = BT_Road_inprogress + BT_Road_Completed
        Bus_Stand_SchemeShare = MasterSanctionForm.objects.filter(Scheme__Scheme="KNMT").filter(Sector="Bus Stand").aggregate(Bus_Stand_SchemeShare = Sum('SchemeShare'))
        Bus_Stand_ULBShare = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector='Bus Stand').aggregate(Bus_Stand_ULBShare=Sum('ULBShare'))
        Bus_Stand_Total = Bus_Stand_SchemeShare['Bus_Stand_SchemeShare'] + Bus_Stand_ULBShare['Bus_Stand_ULBShare']
        Bus_Stand_Approved = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector='Bus Stand').count()
        Bus_Stand_Completed = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector='Bus Stand').filter(status='Completed').count()
        Bus_Stand_inprogress = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector='Bus Stand').filter(status='In Progress').count()
        Bus_Stand_Taken = Bus_Stand_inprogress + Bus_Stand_Completed
        CC_Road_SchemeShare = MasterSanctionForm.objects.filter(Scheme__Scheme="KNMT").filter(Sector="CC Road").aggregate(CC_Road_SchemeShare = Sum('SchemeShare'))
        CC_Road_ULBShare = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector='CC Road').aggregate(CC_Road_ULBShare=Sum('ULBShare'))
        CC_Road_Total = CC_Road_SchemeShare['CC_Road_SchemeShare'] + CC_Road_ULBShare['CC_Road_ULBShare']
        CC_Road_Approved = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector='CC Road').count()
        CC_Road_Completed = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector='CC Road').filter(status='Completed').count()
        CC_Road_inprogress = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector='CC Road').filter(status='In Progress').count()
        CC_Road_Taken = CC_Road_inprogress + CC_Road_Completed
        #Community Hall
        Community_Hall_SchemeShare = MasterSanctionForm.objects.filter(Scheme__Scheme="KNMT").filter(Sector="Community Hall").aggregate(Community_Hall_SchemeShare = Sum('SchemeShare'))
        Community_Hall_ULBShare = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector='Community Hall').aggregate(Community_Hall_ULBShare=Sum('ULBShare'))
        Community_Hall_Total = Community_Hall_SchemeShare['Community_Hall_SchemeShare'] + Community_Hall_ULBShare['Community_Hall_ULBShare']
        Community_Hall_Approved = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector='Community Hall').count()
        Community_Hall_Completed = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector='Community Hall').filter(status='Completed').count()
        Community_Hall_inprogress = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector='Community Hall').filter(status='In Progress').count()
        Community_Hall_Taken = Community_Hall_inprogress + Community_Hall_Completed
        #Crematorium
        Crematorium_SchemeShare = MasterSanctionForm.objects.filter(Scheme__Scheme="KNMT").filter(Sector="Crematorium").aggregate(Crematorium_SchemeShare = Sum('SchemeShare'))
        Crematorium_ULBShare = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector='Crematorium').aggregate(Crematorium_ULBShare=Sum('ULBShare'))
        Crematorium_Total = Crematorium_SchemeShare['Crematorium_SchemeShare'] + Crematorium_ULBShare['Crematorium_ULBShare']
        Crematorium_Approved = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector='Crematorium').count()
        Crematorium_Completed = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector='Crematorium').filter(status='Completed').count()
        Crematorium_inprogress = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector='Crematorium').filter(status='In Progress').count()
        Crematorium_Taken = Crematorium_inprogress + Crematorium_Completed
        #	Culvert
        Culvert_SchemeShare = MasterSanctionForm.objects.filter(Scheme__Scheme="KNMT").filter(Sector="Culvert").aggregate(Culvert_SchemeShare = Sum('SchemeShare'))
        Culvert_ULBShare = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector='Culvert').aggregate(Culvert_ULBShare=Sum('ULBShare'))
        Culvert_Total = Culvert_SchemeShare['Culvert_SchemeShare'] + Culvert_ULBShare['Culvert_ULBShare']
        Culvert_Approved = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector='Culvert').count()
        Culvert_Completed = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector='Culvert').filter(status='Completed').count()
        Culvert_inprogress = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector='Culvert').filter(status='In Progress').count()
        Culvert_Taken = Culvert_inprogress + Culvert_Completed
            #Knowledge Centre
        Knowledge_Centre_SchemeShare = MasterSanctionForm.objects.filter(Scheme__Scheme="KNMT").filter(Sector="Knowledge Centre").aggregate(Knowledge_Centre_SchemeShare = Sum('SchemeShare'))
        Knowledge_Centre_ULBShare = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector='Knowledge Centre').aggregate(Knowledge_Centre_ULBShare=Sum('ULBShare'))
        Knowledge_Centre_Total = Knowledge_Centre_SchemeShare['Knowledge_Centre_SchemeShare'] + Knowledge_Centre_ULBShare['Knowledge_Centre_ULBShare']
        Knowledge_Centre_Approved = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector='Knowledge Centre').count()
        Knowledge_Centre_Completed = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector='Knowledge Centre').filter(status='Completed').count()
        Knowledge_Centre_inprogress = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector='Knowledge Centre').filter(status='In Progress').count()
        Knowledge_Centre_Taken = Knowledge_Centre_inprogress + Knowledge_Centre_Completed
            #Market
        Market_SchemeShare = MasterSanctionForm.objects.filter(Scheme__Scheme="KNMT").filter(Sector="Market").aggregate(Market_SchemeShare = Sum('SchemeShare'))
        Market_ULBShare = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector='Market').aggregate(Market_ULBShare=Sum('ULBShare'))
        Market_Total = Market_SchemeShare['Market_SchemeShare'] + Market_ULBShare['Market_ULBShare']
        Market_Approved = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector='Market').count()
        Market_Completed = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector='Market').filter(status='Completed').count()
        Market_inprogress = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector='Market').filter(status='In Progress').count()
        Market_Taken = Market_inprogress + Market_Completed
        #Metal Beam Crash Barriers
        M_B_C_B_SchemeShare = MasterSanctionForm.objects.filter(Scheme__Scheme="KNMT").filter(Sector="Metal Beam Crash Barriers").aggregate(M_B_C_B_SchemeShare = Sum('SchemeShare'))
        M_B_C_B_ULBShare = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector='Metal Beam Crash Barriers').aggregate(M_B_C_B_ULBShare=Sum('ULBShare'))
        M_B_C_B_Total = M_B_C_B_SchemeShare['M_B_C_B_SchemeShare'] + M_B_C_B_ULBShare['M_B_C_B_ULBShare']
        M_B_C_B_Approved = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector='Metal Beam Crash Barriers').count()
        M_B_C_B_Completed = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector='Metal Beam Crash Barriers').filter(status='Completed').count()
        M_B_C_B_inprogress = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector='Metal Beam Crash Barriers').filter(status='In Progress').count()
        M_B_C_B_Taken = M_B_C_B_inprogress + M_B_C_B_Completed

        #Parks
        Parks_SchemeShare = MasterSanctionForm.objects.filter(Scheme__Scheme="KNMT").filter(Sector="Parks").aggregate(Parks_SchemeShare = Sum('SchemeShare'))
        Parks_ULBShare = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector='Parks').aggregate(Parks_ULBShare=Sum('ULBShare'))
        Parks_Total = Parks_SchemeShare['Parks_SchemeShare'] + Parks_ULBShare['Parks_ULBShare']
        Parks_Approved = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector='Parks').count()
        Parks_Completed = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector='Parks').filter(status='Completed').count()
        Parks_inprogress = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector='Parks').filter(status='In Progress').count()
        Parks_Taken = Parks_inprogress + Parks_Completed

        #Paver Block
        Paver_Block_SchemeShare = MasterSanctionForm.objects.filter(Scheme__Scheme="KNMT").filter(Sector="Paver Block").aggregate(Paver_Block_SchemeShare = Sum('SchemeShare'))
        Paver_Block_ULBShare = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector='Paver Block').aggregate(Paver_Block_ULBShare=Sum('ULBShare'))
        Paver_Block_Total = Paver_Block_SchemeShare['Paver_Block_SchemeShare'] + Paver_Block_ULBShare['Paver_Block_ULBShare']
        Paver_Block_Approved = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector='Paver Block').count()
        Paver_Block_Completed = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector='Paver Block').filter(status='Completed').count()
        Paver_Block_inprogress = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector='Paver Block').filter(status='In Progress').count()
        Paver_Block_Taken = Paver_Block_inprogress + Paver_Block_Completed

        #Retaining wall
        Retaining_wall_SchemeShare = MasterSanctionForm.objects.filter(Scheme__Scheme="KNMT").filter(Sector="Retaining wall").aggregate(Retaining_wall_SchemeShare = Sum('SchemeShare'))
        Retaining_wall_ULBShare = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector='Retaining wall').aggregate(Retaining_wall_ULBShare=Sum('ULBShare'))
        Retaining_wall_Total = Retaining_wall_SchemeShare['Retaining_wall_SchemeShare'] + Retaining_wall_ULBShare['Retaining_wall_ULBShare']
        Retaining_wall_Approved = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector='Retaining wall').count()
        Retaining_wall_Completed = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector='Retaining wall').filter(status='Completed').count()
        Retaining_wall_inprogress = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector='Retaining wall').filter(status='In Progress').count()
        Retaining_wall_Taken = Retaining_wall_inprogress + Retaining_wall_Completed
        #Solid Waste Mgt. SWM
        SWM_SchemeShare = MasterSanctionForm.objects.filter(Scheme__Scheme="KNMT").filter(Sector="Solid Waste Mgt.").aggregate(SWM_SchemeShare = Sum('SchemeShare'))
        SWM_ULBShare = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector='Solid Waste Mgt.').aggregate(SWM_ULBShare=Sum('ULBShare'))
        SWM_Total = SWM_SchemeShare['SWM_SchemeShare'] + SWM_ULBShare['SWM_ULBShare']
        SWM_Approved = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector='Solid Waste Mgt.').count()
        SWM_Completed = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector='Solid Waste Mgt.').filter(status='Completed').count()
        SWM_inprogress = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector='Solid Waste Mgt.').filter(status='In Progress').count()
        SWM_Taken = SWM_inprogress + SWM_Completed
        #SWD
        SWD_SchemeShare = MasterSanctionForm.objects.filter(Scheme__Scheme="KNMT").filter(Sector="SWD").aggregate(SWD_SchemeShare = Sum('SchemeShare'))
        SWD_ULBShare = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector='SWD').aggregate(SWD_ULBShare=Sum('ULBShare'))
        SWD_Total = SWD_SchemeShare['SWD_SchemeShare'] + SWD_ULBShare['SWD_ULBShare']
        SWD_Approved = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector='SWD').count()
        SWD_Completed = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector='SWD').filter(status='Completed').count()
        SWD_inprogress = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector='SWD').filter(status='In Progress').count()
        SWD_Taken = SWD_inprogress + SWD_Completed

        #Water Bodies
        Water_Bodies_SchemeShare = MasterSanctionForm.objects.filter(Scheme__Scheme="KNMT").filter(Sector="Water Bodies").aggregate(Water_Bodies_SchemeShare = Sum('SchemeShare'))
        Water_Bodies_ULBShare = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector='Water Bodies').aggregate(Water_Bodies_ULBShare=Sum('ULBShare'))
        Water_Bodies_Total = Water_Bodies_SchemeShare['Water_Bodies_SchemeShare'] + Water_Bodies_ULBShare['Water_Bodies_ULBShare']
        Water_Bodies_Approved = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector='Water Bodies').count()
        Water_Bodies_Completed = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector='Water Bodies').filter(status='Completed').count()
        Water_Bodies_inprogress = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector='Water Bodies').filter(status='In Progress').count()
        Water_Bodies_Taken = Water_Bodies_inprogress + Water_Bodies_Completed
        
        SchemeShare = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').aggregate(SchemeShare = Sum('SchemeShare'))
        ULBShare = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').aggregate(ULBShare=Sum('ULBShare'))
        ProjectCost = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').aggregate(ProjectCost=Sum('ApprovedProjectCost'))
        work_approved_total = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').count()
        
        works_inprogress_total = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(status='In Progress').count()
        works_completed_total = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(status='Completed').count()
        works_taken_total = works_inprogress_total+works_completed_total

        extra_context = {
            'works_taken_total':works_taken_total,
            'works_inprogress_total':works_inprogress_total,
            'works_completed_total':works_completed_total,
            'work_approved_total':work_approved_total,
            'ProjectCost': ProjectCost,
            'ULBShare': ULBShare,
            'SchemeShare':SchemeShare,  
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
            'Community_Hall_SchemeShare':Community_Hall_SchemeShare,
            'Community_Hall_ULBShare': Community_Hall_ULBShare,
            'Community_Hall_Total': Community_Hall_Total,
            'Community_Hall_inprogress': Community_Hall_inprogress,
            'Community_Hall_Completed': Community_Hall_Completed,
            'Community_Hall_Approved': Community_Hall_Approved,
            'Community_Hall_Taken': Community_Hall_Taken,

            'Crematorium_SchemeShare':Crematorium_SchemeShare,
            'Crematorium_ULBShare': Crematorium_ULBShare,
            'Crematorium_Total': Crematorium_Total,
            'Crematorium_inprogress': Crematorium_inprogress,
            'Crematorium_Completed': Crematorium_Completed,
            'Crematorium_Approved': Crematorium_Approved,
            'Crematorium_Taken': Crematorium_Taken,
            
            'Culvert_SchemeShare':Culvert_SchemeShare,
            'Culvert_ULBShare': Culvert_ULBShare,
            'Culvert_Total': Culvert_Total,
            'Culvert_inprogress': Culvert_inprogress,
            'Culvert_Completed': Culvert_Completed,
            'Culvert_Approved': Culvert_Approved,
            'Culvert_Taken': Culvert_Taken,


            'Knowledge_Centre_SchemeShare':Knowledge_Centre_SchemeShare,
            'Knowledge_Centre_ULBShare': Knowledge_Centre_ULBShare,
            'Knowledge_Centre_Total': Knowledge_Centre_Total,
            'Knowledge_Centre_inprogress': Knowledge_Centre_inprogress,
            'Knowledge_Centre_Completed': Knowledge_Centre_Completed,
            'Knowledge_Centre_Approved': Knowledge_Centre_Approved,
            'Knowledge_Centre_Taken': Knowledge_Centre_Taken,

              
            'Market_SchemeShare':Market_SchemeShare,
            'Market_ULBShare': Market_ULBShare,
            'Market_Total': Market_Total,
            'Market_inprogress': Market_inprogress,
            'Market_Completed': Market_Completed,
            'Market_Approved': Market_Approved,
            'Market_Taken': Market_Taken,

            'M_B_C_B_SchemeShare':M_B_C_B_SchemeShare,
            'M_B_C_B_ULBShare': M_B_C_B_ULBShare,
            'M_B_C_B_Total': M_B_C_B_Total,
            'M_B_C_B_inprogress': M_B_C_B_inprogress,
            'M_B_C_B_Completed': M_B_C_B_Completed,
            'M_B_C_B_Approved': M_B_C_B_Approved,
            'M_B_C_B_Taken': M_B_C_B_Taken,
        
            'Parks_SchemeShare':Parks_SchemeShare,
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
