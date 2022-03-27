from django.contrib import admin
from .models import Dashboard
from django.db.models import Count, Sum, Avg, Func, FloatField, F
from django.db.models import Q
from TUFIDCOapp.models import *
from ULBForms.models import *
import xlwt
from django.http import HttpResponse


# Register your models here.
class Round(Func):
    function = "ROUND"
    arity = 2


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

        a = AgencyProgressModel.objects.values_list('Project_ID', flat=True).filter(Scheme='KNMT').filter(
            status='Completed')

        b = AgencyProgressModel.objects.values_list('Project_ID', flat=True).filter(Scheme='KNMT').filter(
            status='In Progress')

        response.context_data['district_c'] = list(
            qs.values('District__District').order_by('District__District').filter(Scheme__Scheme='KNMT').filter(
                Sector='Bus Stand').filter(
                ~Q(Project_ID__in=a)).annotate(count=Count('Project_ID'))
        )
        response.context_data['district_btroad'] = list(
            qs.values('District__District').order_by('District__District').filter(Scheme__Scheme='KNMT').filter(
                Sector='BT Road').filter(
                ~Q(Project_ID__in=a)).annotate(count=Count('Project_ID'))
        )
        response.context_data['district_ccroad'] = list(
            qs.values('District__District').order_by('District__District').filter(Scheme__Scheme='KNMT').filter(
                Sector='CC Road').filter(
                ~Q(Project_ID__in=a)).annotate(count=Count('Project_ID'))
        )
        response.context_data['district_ch'] = list(
            qs.values('District__District').order_by('District__District').filter(Scheme__Scheme='KNMT').filter(
                Sector='Community Hall').filter(
                ~Q(Project_ID__in=a)).annotate(count=Count('Project_ID'))
        )
        response.context_data['district_cr'] = list(
            qs.values('District__District').order_by('District__District').filter(Scheme__Scheme='KNMT').filter(
                Sector='Crematorium').filter(
                ~Q(Project_ID__in=a)).annotate(count=Count('Project_ID'))
        )
        response.context_data['district_cul'] = list(
            qs.values('District__District').order_by('District__District').filter(Scheme__Scheme='KNMT').filter(
                Sector='Culvert').filter(
                ~Q(Project_ID__in=a)).annotate(count=Count('Project_ID'))
        )
        response.context_data['district_kc'] = list(
            qs.values('District__District').order_by('District__District').filter(Scheme__Scheme='KNMT').filter(
                Sector='Knowledge Centre').filter(
                ~Q(Project_ID__in=a)).annotate(count=Count('Project_ID'))
        )
        response.context_data['district_m'] = list(
            qs.values('District__District').order_by('District__District').filter(Scheme__Scheme='KNMT').filter(
                Sector='Market').filter(
                ~Q(Project_ID__in=a)).annotate(count=Count('Project_ID'))
        )
        response.context_data['district_mbcb'] = list(
            qs.values('District__District').order_by('District__District').filter(Scheme__Scheme='KNMT').filter(
                Sector='Metal Beam Crash Barriers').filter(
                ~Q(Project_ID__in=a)).annotate(count=Count('Project_ID'))
        )

        response.context_data['district_p'] = list(
            qs.values('District__District').order_by('District__District').filter(
                Sector='Parks').filter(~Q(Project_ID__in=a)).filter(~Q(Project_ID__in=b)).annotate(count=Count('Project_ID'))
        )




        response.context_data['district_pb'] = list(
            qs.values('District__District').order_by('District__District').filter(Scheme__Scheme='KNMT').filter(
                Sector='Paver Block').filter(
                ~Q(Project_ID__in=a)).annotate(count=Count('Project_ID'))
        )
        response.context_data['district_rw'] = list(
            qs.values('District__District').order_by('District__District').filter(Scheme__Scheme='KNMT').filter(
                Sector='Retaining wall').filter(
                ~Q(Project_ID__in=a)).annotate(count=Count('Project_ID'))
        )
        response.context_data['district_swm'] = list(
            qs.values('District__District').order_by('District__District').filter(Scheme__Scheme='KNMT').filter(
                Sector='Solid Waste Mgt.').filter(
                ~Q(Project_ID__in=a)).annotate(count=Count('Project_ID'))
        )
        response.context_data['district_swd'] = list(
            qs.values('District__District').order_by('District__District').filter(Scheme__Scheme='KNMT').filter(
                Sector='SWD').filter(
                ~Q(Project_ID__in=a)).annotate(count=Count('Project_ID'))
        )
        response.context_data['district_wb'] = list(
            qs.values('District__District').order_by('District__District').filter(Scheme__Scheme='KNMT').filter(
                Sector='Water Bodies').filter(
                ~Q(Project_ID__in=a)).annotate(count=Count('Project_ID'))
        )
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

        RW = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector__in=['Retaining wall']).aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        RW_total = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector__in=['Retaining wall']).count()
        RWDMA = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector__in=['Retaining wall']).filter(
            AgencyType__AgencyType="Municipality").aggregate(project_cost=Sum('ApprovedProjectCost'))
        RWDMA_total = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector__in=['Retaining wall']).filter(
            AgencyType__AgencyType="Municipality").count()
        RWCTP = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector="Retaining wall").filter(
            AgencyType__AgencyType="Town Panchayat").aggregate(project_cost=Sum('ApprovedProjectCost'))
        RWCTP_total = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector__in=['Retaining wall']).filter(
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
        rw_pt = "{:.2f}".format((RW['project_cost']) / (project_cost['project_cost']) * 100)

        def rw_dma_percent():
            if RWDMA['project_cost'] == None:
                v = 0
            else:
                v = RWDMA['project_Cost']
            return v

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
        RWDMA_pt = "{:.2f}".format(rw_dma_percent() / (project_cost['project_cost']) * 100)
        DMA_total_percent = "{:.2f}".format(dmp_project_cost['dmp_project_cost'] / (project_cost['project_cost']) * 100)

        CTPRW_pt = "{:.2f}".format((RWCTP['project_cost']) / (project_cost['project_cost']) * 100)
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

        list_agency_progress = list(AgencyProgressModel.objects.values_list('Project_ID', flat=True).filter(
            Scheme='KNMT').filter(status='In Progress'))

        list_agency_completed = list(AgencyProgressModel.objects.values_list('Project_ID', flat=True).filter(
            Scheme='KNMT').filter(status='Completed'))
        final_list = list_agency_progress + list_agency_completed

        busstand_approved_project_count = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector='Bus Stand').count()
        busstand_approved_project_cost = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector='Bus Stand').aggregate(project_cost=Sum('ApprovedProjectCost'))
        busstand_completed_count = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector='Bus Stand').filter(
            status='Completed').count()
        busstand_completed_approved_project_cost = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            Sector='Bus Stand').filter(status='Completed').aggregate(project_cost=Sum('ApprovedProjectCost'))
        busstand_inprogress_count = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector='Bus Stand').filter(
            status='In Progress').count()
        busstand_inprogress_approved_project_cost = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            Sector='Bus Stand').filter(status='In Progress').aggregate(project_cost=Sum('ApprovedProjectCost'))
        busstand_tobecommenced_count = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector='Bus Stand').filter(~Q(Project_ID__in=final_list)).count()
        busstand_tobecommenced_project_cost = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector='Bus Stand').filter(~Q(Project_ID__in=final_list)).aggregate(project_cost=Sum('ApprovedProjectCost'))

        busstand_district = AgencyProgressModel.objects.values('District').order_by('District').filter(
            Scheme='KNMT').filter(Sector='Bus Stand').filter(status='In Progress').annotate(
            percent=Avg('percentageofworkdone'))

        btroad_approved_project_count = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector='BT Road').count()
        btroad_approved_project_cost = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector='BT Road').aggregate(project_cost=Sum('ApprovedProjectCost'))
        btroad_completed_count = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector='BT Road').filter(
            status='Completed').count()
        btroad_completed_approved_project_cost = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            Sector='BT Road').filter(status='Completed').aggregate(project_cost=Sum('ApprovedProjectCost'))
        btroad_inprogress_count = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector='BT Road').filter(
            status='In Progress').count()
        btroad_inprogress_approved_project_cost = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            Sector='BT Road').filter(status='In Progress').aggregate(project_cost=Sum('ApprovedProjectCost'))
        btroad_tobecommenced_count = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector='BT Road').filter(~Q(Project_ID__in=final_list)).count()
        btroad_tobecommenced_project_cost = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector='BT Road').filter(~Q(Project_ID__in=final_list)).aggregate(project_cost=Sum('ApprovedProjectCost'))

        btroad_district = AgencyProgressModel.objects.values('District').order_by('District').filter(
            Scheme='KNMT').filter(Sector='BT Road').filter(
            status='In Progress').annotate(percent=Avg('percentageofworkdone'))

        ccroad_approved_project_count = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector='CC Road').count()
        ccroad_approved_project_cost = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector='CC Road').aggregate(project_cost=Sum('ApprovedProjectCost'))
        ccroad_completed_count = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector='CC Road').filter(
            status='Completed').count()
        ccroad_completed_approved_project_cost = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            Sector='CC Road').filter(status='Completed').aggregate(project_cost=Sum('ApprovedProjectCost'))
        ccroad_inprogress_count = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector='CC Road').filter(
            status='In Progress').count()
        ccroad_inprogress_approved_project_cost = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            Sector='CC Road').filter(status='In Progress').aggregate(project_cost=Sum('ApprovedProjectCost'))
        ccroad_tobecommenced_count = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector='CC Road').filter(~Q(Project_ID__in=final_list)).count()
        ccroad_tobecommenced_project_cost =MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector='CC Road').filter(~Q(Project_ID__in=final_list)).aggregate(project_cost=Sum('ApprovedProjectCost'))
        ccroad_district = AgencyProgressModel.objects.values('District').order_by('District').filter(
            Scheme='KNMT').filter(Sector='CC Road').filter(status='In Progress').annotate(
            percent=Avg('percentageofworkdone'))

        communityhall_approved_project_count = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector='Community Hall').count()
        communityhall_approved_project_cost = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector='Community Hall').aggregate(project_cost=Sum('ApprovedProjectCost'))
        communityhall_completed_count = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            Sector='Community Hall').filter(status='Completed').count()
        communityhall_completed_approved_project_cost = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            Sector='Community Hall').filter(status='Completed').aggregate(project_cost=Sum('ApprovedProjectCost'))
        communityhall_inprogress_count = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            Sector='Community Hall').filter(status='In Progress').count()
        communityhall_inprogress_approved_project_cost = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            Sector='Community Hall').filter(status='In Progress').aggregate(project_cost=Sum('ApprovedProjectCost'))
        communityhall_tobecommenced_count = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector='Community Hall').filter(~Q(Project_ID__in=final_list)).count()
        communityhall_tobecommenced_project_cost = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector='Community Hall').filter(~Q(Project_ID__in=final_list)).aggregate(project_cost=Sum('ApprovedProjectCost'))

        communityhall_district = AgencyProgressModel.objects.values('District').order_by('District').filter(
            Scheme='KNMT').filter(Sector='Community Hall').filter(status='In Progress').annotate(
            percent=Avg('percentageofworkdone'))

        crematorium_approved_project_count = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector='Crematorium').count()
        crematorium_approved_project_cost = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector='Crematorium').aggregate(project_cost=Sum('ApprovedProjectCost'))
        crematorium_completed_count = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            Sector='Crematorium').filter(status='Completed').count()
        crematorium_completed_approved_project_cost = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            Sector='Crematorium').filter(status='Completed').aggregate(project_cost=Sum('ApprovedProjectCost'))
        crematorium_inprogress_count = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            Sector='Crematorium').filter(status='In Progress').count()
        crematorium_inprogress_approved_project_cost = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            Sector='Crematorium').filter(status='In Progress').aggregate(project_cost=Sum('ApprovedProjectCost'))
        crematorium_tobecommenced_count = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector='Crematorium').filter(~Q(Project_ID__in=final_list)).count()
        crematorium_tobecommenced_project_cost = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector='Crematorium').filter(~Q(Project_ID__in=final_list)).aggregate(project_cost=Sum('ApprovedProjectCost'))

        crematorium_district = AgencyProgressModel.objects.values('District').order_by('District').filter(
            Scheme='KNMT').filter(Sector='Crematorium').filter(status='In Progress').annotate(
            percent=Avg('percentageofworkdone'))

        culvert_approved_project_count = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector='Culvert').count()
        culvert_approved_project_cost = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector='Culvert').aggregate(project_cost=Sum('ApprovedProjectCost'))
        culvert_completed_count = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector='Culvert').filter(
            status='Completed').count()
        culvert_completed_approved_project_cost = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            Sector='Culvert').filter(status='Completed').aggregate(project_cost=Sum('ApprovedProjectCost'))
        culvert_inprogress_count = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector='Culvert').filter(
            status='In Progress').count()
        culvert_inprogress_approved_project_cost = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            Sector='Culvert').filter(status='In Progress').aggregate(project_cost=Sum('ApprovedProjectCost'))
        culvert_tobecommenced_count = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector='Culvert').filter(~Q(Project_ID__in=final_list)).count()
        culvert_tobecommenced_project_cost = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector='Culvert').filter(~Q(Project_ID__in=final_list)).aggregate(project_cost=Sum('ApprovedProjectCost'))

        culvert_district = AgencyProgressModel.objects.values('District').order_by('District').filter(
            Scheme='KNMT').filter(Sector='Culvert').filter(status='In Progress').annotate(
            percent=Avg('percentageofworkdone'))

        Market_approved_project_count = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector='Market').count()
        Market_approved_project_cost = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector='Market').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Market_completed_count = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector='Market').filter(
            status='Completed').count()
        Market_completed_approved_project_cost = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            Sector='Market').filter(status='Completed').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Market_inprogress_count = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector='Market').filter(
            status='In Progress').count()
        Market_inprogress_approved_project_cost = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            Sector='Market').filter(status='In Progress').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Market_tobecommenced_count = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector='Market').filter(~Q(Project_ID__in=final_list)).count()
        Market_tobecommenced_project_cost = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector='Market').filter(~Q(Project_ID__in=final_list)).aggregate(project_cost=Sum('ApprovedProjectCost'))
        Market_district = AgencyProgressModel.objects.values('District').order_by('District').filter(
            Scheme='KNMT').filter(Sector='Market').filter(status='In Progress').annotate(
            percent=Avg('percentageofworkdone'))

        KnowledgeCentre_approved_project_count = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector='Knowledge Centre').count()
        KnowledgeCentre_approved_project_cost = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector='Knowledge Centre').aggregate(project_cost=Sum('ApprovedProjectCost'))
        KnowledgeCentre_completed_count = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            Sector='Knowledge Centre').filter(status='Completed').count()
        KnowledgeCentre_completed_approved_project_cost = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            Sector='Knowledge Centre').filter(status='Completed').aggregate(project_cost=Sum('ApprovedProjectCost'))
        KnowledgeCentre_inprogress_count = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            Sector='Knowledge Centre').filter(status='In Progress').count()
        KnowledgeCentre_inprogress_approved_project_cost = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            Sector='Knowledge Centre').filter(status='In Progress').aggregate(project_cost=Sum('ApprovedProjectCost'))
        KnowledgeCentre_tobecommenced_count =MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector='Knowledge Centre').filter(~Q(Project_ID__in=final_list)).count()
        KnowledgeCentre_tobecommenced_project_cost = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector='Knowledge Centre').filter(~Q(Project_ID__in=final_list)).aggregate(project_cost=Sum('ApprovedProjectCost'))

        KnowledgeCentre_district = AgencyProgressModel.objects.values('District').order_by('District').filter(
            Scheme='KNMT').filter(Sector='Knowledge Centre').filter(status='In Progress').annotate(
            percent=Avg('percentageofworkdone'))

        MetalBeamCrashBarriers_approved_project_count = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector='Metal Beam Crash Barriers').count()
        MetalBeamCrashBarriers_approved_project_cost = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector='Metal Beam Crash Barriers').aggregate(project_cost=Sum('ApprovedProjectCost'))
        MetalBeamCrashBarriers_completed_count = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            Sector='MetalBeam Crash Barriers').filter(
            status='Completed').count()
        MetalBeamCrashBarriers_completed_approved_project_cost = AgencyProgressModel.objects.filter(
            Scheme='KNMT').filter(
            Sector='Metal Beam Crash Barriers').filter(status='Completed').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        MetalBeamCrashBarriers_inprogress_count = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            Sector='Metal Beam Crash Barriers').filter(
            status='In Progress').count()
        MetalBeamCrashBarriers_inprogress_approved_project_cost = AgencyProgressModel.objects.filter(
            Scheme='KNMT').filter(
            Sector='Metal Beam Crash Barriers').filter(status='In Progress').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        MetalBeamCrashBarriers_tobecommenced_count = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector='Metal Beam Crash Barriers').filter(~Q(Project_ID__in=final_list)).count()
        MetalBeamCrashBarriers_tobecommenced_project_cost =MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector='Metal Beam Crash Barriers').filter(~Q(Project_ID__in=final_list)).aggregate(project_cost=Sum('ApprovedProjectCost'))
        MetalBeamCrashBarriers_district = AgencyProgressModel.objects.values('District').order_by('District').filter(
            Scheme='KNMT').filter(Sector='Metal Beam Crash Barriers').filter(status='In Progress').annotate(
            percent=Avg('percentageofworkdone'))


        Parks_approved_project_count = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector='Parks').count()
        Parks_approved_project_cost = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector='Parks').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Parks_completed_count = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            Sector='Parks').filter(
            status='Completed').count()
        Parks_completed_approved_project_cost = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            Sector='Parks').filter(status='Completed').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Parks_inprogress_count = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector='Parks').filter(
            status='In Progress').count()
        Parks_inprogress_approved_project_cost = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            Sector='Parks').filter(status='In Progress').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Parks_tobecommenced_count = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector='Parks').filter(~Q(Project_ID__in=final_list)).count()
        Parks_tobecommenced_project_cost = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector='Parks').filter(~Q(Project_ID__in=final_list)).aggregate(project_cost=Sum('ApprovedProjectCost'))

        Parks_district = AgencyProgressModel.objects.values('District').order_by('District').filter(
            Scheme='KNMT').filter(Sector='Parks').filter(status='In Progress').annotate(
            percent=Avg('percentageofworkdone'))

        PaverBlock_approved_project_count = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector='Paver Block').count()
        PaverBlock_approved_project_cost = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector='Paver Block').aggregate(project_cost=Sum('ApprovedProjectCost'))
        PaverBlock_completed_count = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            Sector='Paver Block').filter(
            status='Completed').count()
        PaverBlock_completed_approved_project_cost = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            Sector='Paver Block').filter(status='Completed').aggregate(project_cost=Sum('ApprovedProjectCost'))
        PaverBlock_inprogress_count = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            Sector='Paver Block').filter(
            status='In Progress').count()
        PaverBlock_inprogress_approved_project_cost = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            Sector='Paver Block').filter(status='In Progress').aggregate(project_cost=Sum('ApprovedProjectCost'))
        PaverBlock_tobecommenced_count = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector='Paver Block').filter(
            ~Q(Project_ID__in=final_list)).count()
        PaverBlock_tobecommenced_project_cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            ~Q(Project_ID__in=final_list)).aggregate(project_cost=Sum('ApprovedProjectCost'))

        PaverBlock_district = AgencyProgressModel.objects.values('District').order_by('District').filter(
            Scheme='KNMT').filter(Sector='Paver Block').filter(status='In Progress').annotate(
            percent=Avg('percentageofworkdone'))

        Retainingwall_approved_project_count = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector='Retaining wall').count()
        Retainingwall_approved_project_cost = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector='Retaining wall').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Retainingwall_completed_count = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            Sector='Retaining wall').filter(
            status='Completed').count()
        Retainingwall_completed_approved_project_cost = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            Sector='Retaining wall').filter(status='Completed').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Retainingwall_inprogress_count = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            Sector='Retaining wall').filter(
            status='In Progress').count()
        Retainingwall_inprogress_approved_project_cost = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            Sector='Retaining wall').filter(status='In Progress').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Retainingwall_tobecommenced_count = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector='Retaining wall').filter(
            ~Q(Project_ID__in=final_list)).count()
        Retainingwall_tobecommenced_project_cost = MasterSanctionForm.objects.filter(Sector='Retaining wall').filter(
            ~Q(Project_ID__in=final_list)).aggregate(project_cost=Sum('ApprovedProjectCost'))
        Retainingwall_district = AgencyProgressModel.objects.values('District').order_by('District').filter(
            Scheme='KNMT').filter(Sector='Retaining wall').filter(status='In Progress').annotate(
            percent=Avg('percentageofworkdone'))

        SolidWasteMgt_approved_project_count = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector='Solid Waste Mgt.').count()
        SolidWasteMgt_approved_project_cost = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector='Solid Waste Mgt.').aggregate(project_cost=Sum('ApprovedProjectCost'))
        SolidWasteMgt_completed_count = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            Sector=' Solid Waste Mgt.').filter(
            status='Completed').count()
        SolidWasteMgt_completed_approved_project_cost = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            Sector='Solid Waste Mgt.').filter(status='Completed').aggregate(project_cost=Sum('ApprovedProjectCost'))
        SolidWasteMgt_inprogress_count = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            Sector='Solid Waste Mgt.').filter(
            status='In Progress').count()
        SolidWasteMgt_inprogress_approved_project_cost = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            Sector='Solid Waste Mgt.').filter(status='In Progress').aggregate(project_cost=Sum('ApprovedProjectCost'))
        SolidWasteMgt_tobecommenced_count = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector='Solid Waste Mgt.').filter(
            ~Q(Project_ID__in=final_list)).count()
        SolidWasteMgt_tobecommenced_project_cost = MasterSanctionForm.objects.filter(Sector='Solid Waste Mgt.').filter(
            ~Q(Project_ID__in=final_list)).aggregate(project_cost=Sum('ApprovedProjectCost'))
        SolidWasteMgt_district = AgencyProgressModel.objects.values('District').order_by('District').filter(
            Scheme='KNMT').filter(Sector='Solid Waste Mgt.').filter(status='In Progress').annotate(
            percent=Avg('percentageofworkdone'))
        SWD_approved_project_count = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector='SWD').count()
        SWD_approved_project_cost = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector='SWD').aggregate(project_cost=Sum('ApprovedProjectCost'))
        SWD_completed_count = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector=' SWD').filter(
            status='Completed').count()
        SWD_completed_approved_project_cost = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            Sector='SWD').filter(status='Completed').aggregate(project_cost=Sum('ApprovedProjectCost'))
        SWD_inprogress_count = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector='SWD').filter(
            status='In Progress').count()
        SWD_inprogress_approved_project_cost = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            Sector='SWD').filter(status='In Progress').aggregate(project_cost=Sum('ApprovedProjectCost'))
        SWD_tobecommenced_count = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector='SWD').filter(
            ~Q(Project_ID__in=final_list)).count()
        SWD_tobecommenced_project_cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            ~Q(Project_ID__in=final_list)).aggregate(project_cost=Sum('ApprovedProjectCost'))

        SWD_district = AgencyProgressModel.objects.values('District').order_by('District').filter(
            Scheme='KNMT').filter(Sector='SWD').filter(status='In Progress').annotate(
            percent=Avg('percentageofworkdone'))
        WaterBodies_approved_project_count = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector='Water Bodies').count()
        WaterBodies_approved_project_cost = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector='Water Bodies').aggregate(project_cost=Sum('ApprovedProjectCost'))
        WaterBodies_completed_count = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            Sector='Water Bodies').filter(
            status='Completed').count()
        WaterBodies_completed_approved_project_cost = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            Sector='Water Bodies').filter(status='Completed').aggregate(project_cost=Sum('ApprovedProjectCost'))
        WaterBodies_inprogress_count = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            Sector='Water Bodies').filter(
            status='In Progress').count()
        WaterBodies_inprogress_approved_project_cost = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            Sector='Water Bodies').filter(status='In Progress').aggregate(project_cost=Sum('ApprovedProjectCost'))
        WaterBodies_tobecommenced_count = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector='Water Bodies').filter(
            ~Q(Project_ID__in=final_list)).count()
        WaterBodies_tobecommenced_project_cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            ~Q(Project_ID__in=final_list)).aggregate(project_cost=Sum('ApprovedProjectCost'))

        WaterBodies_district = AgencyProgressModel.objects.values('District').order_by('District').filter(
            Scheme='KNMT').filter(Sector='Water Bodies').filter(status='In Progress').annotate(
            percent=Avg('percentageofworkdone'))

        total_approved_project_count = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').count()
        total_approved_project_cost = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        total_completed_count = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            status='Completed').count()
        total_completed_approved_project_cost = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            status='Completed').aggregate(project_cost=Sum('ApprovedProjectCost'))
        total_inprogress_count = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            status='In Progress').count()
        total_inprogress_approved_project_cost = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            status='In Progress').aggregate(project_cost=Sum('ApprovedProjectCost'))
        total_tobecommenced_count = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            ~Q(Project_ID__in=final_list)).count()
        total_tobecommenced_project_cost = MasterSanctionForm.objects.filter(
            ~Q(Project_ID__in=final_list)).aggregate(project_cost=Sum('ApprovedProjectCost'))

        total_district = AgencyProgressModel.objects.values('District').order_by('District').filter(
            Scheme='KNMT').filter(status='In Progress').annotate(
            percent=Sum('percentageofworkdone'))
        extra_context = {
            'MetalBeamCrashBarriers_district': MetalBeamCrashBarriers_district,
            'CTPRW_pt': CTPRW_pt,
            'RWDMA_pt': RWDMA_pt,
            'rw_pt': rw_pt,
            'total_district': total_district,
            'total_tobecommenced_count': total_tobecommenced_count,
            'total_tobecommenced_project_cost': total_tobecommenced_project_cost,
            'total_inprogress_count': total_inprogress_count,
            'total_inprogress_approved_project_cost': total_inprogress_approved_project_cost,

            'total_approved_project_cost': total_approved_project_cost,
            'total_completed_approved_project_cost': total_completed_approved_project_cost,
            'total_approved_project_count': WaterBodies_approved_project_count,
            'total_completed_count': WaterBodies_completed_count,

            'WaterBodies_district': WaterBodies_district,
            'WaterBodies_tobecommenced_count': WaterBodies_tobecommenced_count,
            'WaterBodies_tobecommenced_project_cost': WaterBodies_tobecommenced_project_cost,
            'WaterBodies_inprogress_count': WaterBodies_inprogress_count,
            'WaterBodies_inprogress_approved_project_cost': WaterBodies_inprogress_approved_project_cost,

            'WaterBodies_approved_project_cost': WaterBodies_approved_project_cost,
            'WaterBodies_completed_approved_project_cost': WaterBodies_completed_approved_project_cost,
            'WaterBodies_approved_project_count': WaterBodies_approved_project_count,
            'WaterBodies_completed_count': WaterBodies_completed_count,
            'SWD_district': SWD_district,
            'SWD_tobecommenced_count': SWD_tobecommenced_count,
            'SWD_tobecommenced_project_cost': SWD_tobecommenced_project_cost,
            'SWD_inprogress_count': SWD_inprogress_count,
            'SWD_inprogress_approved_project_cost': SWD_inprogress_approved_project_cost,

            'SWD_approved_project_cost': SWD_approved_project_cost,
            'SWD_completed_approved_project_cost': SWD_completed_approved_project_cost,
            'SWD_approved_project_count': SWD_approved_project_count,
            'SWD_completed_count': SWD_completed_count,

            'SolidWasteMgt_district': SolidWasteMgt_district,
            'SolidWasteMgt_tobecommenced_count': SolidWasteMgt_tobecommenced_count,
            'SolidWasteMgt_tobecommenced_project_cost': SolidWasteMgt_tobecommenced_project_cost,
            'SolidWasteMgt_inprogress_count': SolidWasteMgt_inprogress_count,
            'SolidWasteMgt_inprogress_approved_project_cost': SolidWasteMgt_inprogress_approved_project_cost,

            'SolidWasteMgt_approved_project_cost': SolidWasteMgt_approved_project_cost,
            'SolidWasteMgt_completed_approved_project_cost': SolidWasteMgt_completed_approved_project_cost,
            'SolidWasteMgt_approved_project_count': SolidWasteMgt_approved_project_count,
            'SolidWasteMgt_completed_count': SolidWasteMgt_completed_count,

            'Retainingwall_district': Retainingwall_district,
            'Retainingwall_tobecommenced_count': Retainingwall_tobecommenced_count,
            'Retainingwall_tobecommenced_project_cost': Retainingwall_tobecommenced_project_cost,
            'Retainingwall_inprogress_count': Retainingwall_inprogress_count,
            'Retainingwall_inprogress_approved_project_cost': Retainingwall_inprogress_approved_project_cost,

            'Retainingwall_approved_project_cost': Retainingwall_approved_project_cost,
            'Retainingwall_completed_approved_project_cost': Retainingwall_completed_approved_project_cost,
            'Retainingwall_approved_project_count': Retainingwall_approved_project_count,
            'Retainingwall_completed_count': Retainingwall_completed_count,

            'PaverBlock_district': PaverBlock_district,
            'PaverBlock_tobecommenced_count': PaverBlock_tobecommenced_count,
            'PaverBlock_tobecommenced_project_cost': PaverBlock_tobecommenced_project_cost,
            'PaverBlock_inprogress_count': PaverBlock_inprogress_count,
            'PaverBlock_inprogress_approved_project_cost': PaverBlock_inprogress_approved_project_cost,

            'PaverBlock_approved_project_cost': PaverBlock_approved_project_cost,
            'PaverBlock_completed_approved_project_cost': PaverBlock_completed_approved_project_cost,
            'PaverBlock_approved_project_count': PaverBlock_approved_project_count,
            'PaverBlock_completed_count': PaverBlock_completed_count,

            'Parks_district': Parks_district,
            'Parks_tobecommenced_count': Parks_tobecommenced_count,
            'Parks_tobecommenced_project_cost': Parks_tobecommenced_project_cost,
            'Parks_inprogress_count': Parks_inprogress_count,
            'Parks_inprogress_approved_project_cost': Parks_inprogress_approved_project_cost,

            'Parks_approved_project_cost': Parks_approved_project_cost,
            'Parks_completed_approved_project_cost': Parks_completed_approved_project_cost,
            'Parks_approved_project_count': Parks_approved_project_count,
            'Parks_completed_count': Parks_completed_count,


            'MetalBeamCrashBarriers_tobecommenced_count': MetalBeamCrashBarriers_tobecommenced_count,
            'MetalBeamCrashBarriers_tobecommenced_project_cost': MetalBeamCrashBarriers_tobecommenced_project_cost,
            'MetalBeamCrashBarriers_inprogress_count': MetalBeamCrashBarriers_inprogress_count,
            'MetalBeamCrashBarriers_inprogress_approved_project_cost': MetalBeamCrashBarriers_inprogress_approved_project_cost,

            'MetalBeamCrashBarriers_approved_project_cost': MetalBeamCrashBarriers_approved_project_cost,
            'MetalBeamCrashBarriers_completed_approved_project_cost': MetalBeamCrashBarriers_completed_approved_project_cost,
            'MetalBeamCrashBarriers_approved_project_count': MetalBeamCrashBarriers_approved_project_count,
            'MetalBeamCrashBarriers_completed_count': MetalBeamCrashBarriers_completed_count,

            'Market_district': Market_district,
            'Market_tobecommenced_count': Market_tobecommenced_count,
            'Market_tobecommenced_project_cost': Market_tobecommenced_project_cost,
            'Market_inprogress_count': Market_inprogress_count,
            'Market_inprogress_approved_project_cost': Market_inprogress_approved_project_cost,

            'Market_approved_project_cost': Market_approved_project_cost,
            'Market_completed_approved_project_cost': Market_completed_approved_project_cost,
            'Market_approved_project_count': Market_approved_project_count,
            'Market_completed_count': Market_completed_count,

            'KnowledgeCentre_district': KnowledgeCentre_district,
            'KnowledgeCentre_tobecommenced_count': KnowledgeCentre_tobecommenced_count,
            'KnowledgeCentre_tobecommenced_project_cost': KnowledgeCentre_tobecommenced_project_cost,
            'KnowledgeCentre_inprogress_count': KnowledgeCentre_inprogress_count,
            'KnowledgeCentre_inprogress_approved_project_cost': KnowledgeCentre_inprogress_approved_project_cost,

            'KnowledgeCentre_approved_project_cost': KnowledgeCentre_approved_project_cost,
            'KnowledgeCentre_completed_approved_project_cost': KnowledgeCentre_completed_approved_project_cost,
            'KnowledgeCentre_approved_project_count': KnowledgeCentre_approved_project_count,
            'KnowledgeCentre_completed_count': KnowledgeCentre_completed_count,

            'culvert_district': culvert_district,
            'culvert_tobecommenced_count': culvert_tobecommenced_count,
            'culvert_tobecommenced_project_cost': culvert_tobecommenced_project_cost,
            'culvert_inprogress_count': culvert_inprogress_count,
            'culvert_inprogress_approved_project_cost': culvert_inprogress_approved_project_cost,

            'culvert_approved_project_cost': culvert_approved_project_cost,
            'culvert_completed_approved_project_cost': culvert_completed_approved_project_cost,
            'culvert_approved_project_count': culvert_approved_project_count,
            'culvert_completed_count': culvert_completed_count,

            'crematorium_district': crematorium_district,
            'crematorium_tobecommenced_count': crematorium_tobecommenced_count,
            'crematorium_tobecommenced_project_cost': crematorium_tobecommenced_project_cost,
            'crematorium_inprogress_count': crematorium_inprogress_count,
            'crematorium_inprogress_approved_project_cost': crematorium_inprogress_approved_project_cost,

            'crematorium_approved_project_cost': crematorium_approved_project_cost,
            'crematorium_completed_approved_project_cost': crematorium_completed_approved_project_cost,
            'crematorium_approved_project_count': crematorium_approved_project_count,
            'crematorium_completed_count': crematorium_completed_count,
            'communityhall_district': communityhall_district,
            'communityhall_tobecommenced_count': communityhall_tobecommenced_count,
            'communityhall_tobecommenced_project_cost': communityhall_tobecommenced_project_cost,
            'communityhall_inprogress_count': communityhall_inprogress_count,
            'communityhall_inprogress_approved_project_cost': communityhall_inprogress_approved_project_cost,

            'communityhall_approved_project_cost': communityhall_approved_project_cost,
            'communityhall_completed_approved_project_cost': communityhall_completed_approved_project_cost,
            'communityhall_approved_project_count': communityhall_approved_project_count,
            'communityhall_completed_count': communityhall_completed_count,
            'ccroad_district': ccroad_district,
            'ccroad_tobecommenced_count': ccroad_tobecommenced_count,
            'ccroad_tobecommenced_project_cost': ccroad_tobecommenced_project_cost,
            'ccroad_inprogress_count': ccroad_inprogress_count,
            'ccroad_inprogress_approved_project_cost': ccroad_inprogress_approved_project_cost,

            'ccroad_approved_project_cost': ccroad_approved_project_cost,
            'ccroad_completed_approved_project_cost': ccroad_completed_approved_project_cost,
            'ccroad_approved_project_count': ccroad_approved_project_count,
            'ccroad_completed_count': ccroad_completed_count,

            'btroad_district': btroad_district,
            'btroad_tobecommenced_count': btroad_tobecommenced_count,
            'btroad_tobecommenced_project_cost': btroad_tobecommenced_project_cost,
            'btroad_inprogress_count': btroad_inprogress_count,
            'btroad_inprogress_approved_project_cost': btroad_inprogress_approved_project_cost,
            'btroad_approved_project_cost': btroad_approved_project_cost,
            'btroad_completed_approved_project_cost': btroad_completed_approved_project_cost,
            'btroad_approved_project_count': btroad_approved_project_count,
            'btroad_completed_count': btroad_completed_count,

            'busstand_district': busstand_district,
            'busstand_tobecommenced_count': busstand_tobecommenced_count,
            'busstand_tobecommenced_project_cost': busstand_tobecommenced_project_cost,
            'busstand_inprogress_count': busstand_inprogress_count,
            'busstand_inprogress_approved_project_cost': busstand_inprogress_approved_project_cost,

            'busstand_approved_project_cost': busstand_approved_project_cost,
            'busstand_completed_approved_project_cost': busstand_completed_approved_project_cost,
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
            'RW': RW,
            'RW_total': RW_total,
            'RWDMA': RWDMA,
            'RWDMA_total': RWDMA_total,
            'RWCTP': RWCTP,
            'RWCTP_total': RWCTP_total,
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
