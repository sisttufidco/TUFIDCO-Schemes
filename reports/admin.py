from django.contrib import admin
from .models import *
from TUFIDCOapp.models import *
from django.db.models import Count, Sum
from django.db.models import Q
from ULBForms.models import AgencyProgressModel


# Register your models here.

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

@admin.register(SRPAbstract)
class SRPAbstractAdmin(admin.ModelAdmin):
    change_list_template = 'admin/reports/srp/srp_abstract_report.html'
    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        metrics = {
            'AgencyName': Count('AgencyName', distinct=True),
            'ApprovedCost': Sum('ProjectCost'),
            'RevisedSrpShare': Sum('BalanceEligible'),
            'total_released': Sum('R_Total'),
            'dropped': Sum('Dropped'),
            'balance': Sum('Balance')
        }
        response.context_data['report_total'] = dict(
            qs.aggregate(**metrics)
        )
        response.context_data['report'] = list(
            qs.values('AgencyType__AgencyType').annotate(**metrics).order_by('AgencyType__AgencyType')
        )
        return response



@admin.register(PhysicalandFinancialReport)
class MasterReportAdmin(admin.ModelAdmin):
    change_list_template = 'admin/masterreport.html'

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response
     
        final_data = []
        sector_list = list(MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(Scheme__Scheme="KNMT").distinct())
        for sector in sector_list:
            Schemeshare = MasterSanctionForm.objects.filter(Scheme__Scheme="KNMT").filter(Sector=sector).aggregate(SchemeShare=Sum('SchemeShare'))
            ULBshare = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector=sector).aggregate(ULBShare=Sum('ULBShare'))
            total = Schemeshare['SchemeShare'] + ULBshare['ULBShare']
            approved = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector=sector).count()
            Amountspend = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector=sector).aggregate(sum=Sum('valueofworkdone'))
            Workorder  = AgencySanctionModel.objects.filter(Scheme='KNMT').filter(Sector=sector).aggregate(sum=Sum('work_awarded_amount1'))
            completed = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector=sector).filter(status='Completed').count()
            Value_work_done_completed  = AgencyProgressModel.objects.filter(Scheme="KNMT").filter(Sector=sector).filter(status='Completed').aggregate(sum=Sum('valueofworkdone'))
            Value_work_done_inprogress  = AgencyProgressModel.objects.filter(Scheme="KNMT").filter(Sector=sector).filter(status='In Progress').aggregate(sum=Sum('valueofworkdone'))
            Inprogress = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector=sector).filter(status='In Progress').count()
            Final = list(AgencyProgressModel.objects.values_list('Project_ID', flat=True).filter(Scheme='KNMT').filter(Sector=sector).filter(status='Not Commenced'))
            TS_awarded = AgencySanctionModel.objects.filter(Scheme='KNMT').filter(Sector=sector).filter(ts_awarded='Yes').filter(Q(Project_ID__in=Final)).count()
            WO_awarded = AgencySanctionModel.objects.filter(Scheme='KNMT').filter(Sector=sector).filter(wd_awarded='Yes').filter(Q(Project_ID__in=Final)).count()
            taken = Inprogress + completed
            toBeCommenced = approved - taken
            dic = {
                "Sector":sector,
                "SchemeShare": Schemeshare,
                "ULBShare": ULBshare,
                "Total": total,
                "Approved": approved,
                "amountspend": Amountspend,
                "workorder": Workorder,
                "Completed": completed,
                "value_work_done_completed":Value_work_done_completed,
                "value_work_done_inprogress":Value_work_done_inprogress,
                "inprogress":Inprogress,
                "TS_Awarded":TS_awarded,
                "WO_Awarded":WO_awarded,
                "Taken":taken,
                "ToBeCommenced":toBeCommenced
            }
            final_data.append(dic)

        SchemeShare = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').aggregate(SchemeShare=Sum('SchemeShare'))
        ULBShare = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').aggregate(ULBShare=Sum('ULBShare'))
        ProjectCost = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').aggregate(
            ProjectCost=Sum('ApprovedProjectCost'))
        work_approved_total = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').count()
        work_amountspend = AgencyProgressModel.objects.filter(Scheme='KNMT').aggregate(
            sum=Sum('valueofworkdone'))
        workorder_total = AgencySanctionModel.objects.filter(Scheme='KNMT').aggregate(
            sum=Sum('work_awarded_amount1'))
        works_inprogress_total = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(status='In Progress').count()
        works_completed_total = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(status='Completed').count()
        works_taken_total = works_inprogress_total + works_completed_total
        works_ToBeCommenced = work_approved_total-works_taken_total
        Overall_value_work_done_completed  = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(status='Completed').aggregate(sum=Sum('valueofworkdone'))
        Overall_value_work_done_inprogress  = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(status='In Progress').aggregate(sum=Sum('valueofworkdone'))
        Overall_final = list(AgencyProgressModel.objects.values_list('Project_ID', flat=True).filter(Scheme='KNMT').filter(
            status='Not Commenced'))
        Overall_TS_Awarded = AgencySanctionModel.objects.filter(Scheme='KNMT').filter(ts_awarded='Yes').filter(Q(Project_ID__in=Overall_final)).count()
        Overall_WO_Awarded = AgencySanctionModel.objects.filter(Scheme='KNMT').filter(wd_awarded='Yes').filter(Q(Project_ID__in=Overall_final)).count()
        extra_context = {
            'Overall_value_work_done_completed':Overall_value_work_done_completed,
            'Overall_value_work_done_inprogress':Overall_value_work_done_inprogress,
            'Overall_TS_Awarded':Overall_TS_Awarded,
            'Overall_WO_Awarded':Overall_WO_Awarded,
            'works_ToBeCommenced':works_ToBeCommenced,
            'work_amountspend':work_amountspend,
            'workorder_total':workorder_total,   
            'works_taken_total': works_taken_total,
            'works_inprogress_total': works_inprogress_total,
            'works_completed_total': works_completed_total,
            'work_approved_total': work_approved_total,
            'ProjectCost': ProjectCost,
            'ULBShare': ULBShare,
            'SchemeShare': SchemeShare,
            'final_data':final_data,
        }
        response.context_data.update(extra_context)
        return response

@admin.register(SingaraChennaiPhysicalandFinancialReport)
class SingaraChennaiPhysicalandFinancialReportAdmin(admin.ModelAdmin):
    change_list_template = 'admin/SingaraMasterReport.html'

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response
     
        final_data = []
        sector_list = list(MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(Scheme__Scheme="Singara Chennai 2.0").distinct())
        for sector in sector_list:
            Schemeshare = MasterSanctionForm.objects.filter(Scheme__Scheme="Singara Chennai 2.0").filter(Sector=sector).aggregate(SchemeShare=Sum('SchemeShare'))
            ULBshare = MasterSanctionForm.objects.filter(Scheme__Scheme='Singara Chennai 2.0').filter(Sector=sector).aggregate(ULBShare=Sum('ULBShare'))
            total = Schemeshare['SchemeShare'] + ULBshare['ULBShare']
            approved = MasterSanctionForm.objects.filter(Scheme__Scheme='Singara Chennai 2.0').filter(Sector=sector).count()
            Amountspend = AgencyProgressModel.objects.filter(Scheme='Singara Chennai 2.0').filter(Sector=sector).aggregate(sum=Sum('valueofworkdone'))
            Workorder  = AgencySanctionModel.objects.filter(Scheme='Singara Chennai 2.0').filter(Sector=sector).aggregate(sum=Sum('work_awarded_amount1'))
            completed = AgencyProgressModel.objects.filter(Scheme='Singara Chennai 2.0').filter(Sector=sector).filter(status='Completed').count()
            Value_work_done_completed  = AgencyProgressModel.objects.filter(Scheme="Singara Chennai 2.0").filter(Sector=sector).filter(status='Completed').aggregate(sum=Sum('valueofworkdone'))
            Value_work_done_inprogress  = AgencyProgressModel.objects.filter(Scheme="Singara Chennai 2.0").filter(Sector=sector).filter(status='In Progress').aggregate(sum=Sum('valueofworkdone'))
            Inprogress = AgencyProgressModel.objects.filter(Scheme='Singara Chennai 2.0').filter(Sector=sector).filter(status='In Progress').count()
            Final = list(AgencyProgressModel.objects.values_list('Project_ID', flat=True).filter(Scheme='Singara Chennai 2.0').filter(Sector=sector).filter(status='Not Commenced'))
            TS_awarded = AgencySanctionModel.objects.filter(Scheme='Singara Chennai 2.0').filter(Sector=sector).filter(ts_awarded='Yes').filter(Q(Project_ID__in=Final)).count()
            WO_awarded = AgencySanctionModel.objects.filter(Scheme='Singara Chennai 2.0').filter(Sector=sector).filter(wd_awarded='Yes').filter(Q(Project_ID__in=Final)).count()
            taken = Inprogress + completed
            toBeCommenced = approved - taken
            dic = {
                "Sector":sector,
                "SchemeShare": Schemeshare,
                "ULBShare": ULBshare,
                "Total": total,
                "Approved": approved,
                "amountspend": Amountspend,
                "workorder": Workorder,
                "Completed": completed,
                "value_work_done_completed":Value_work_done_completed,
                "value_work_done_inprogress":Value_work_done_inprogress,
                "inprogress":Inprogress,
                "TS_Awarded":TS_awarded,
                "WO_Awarded":WO_awarded,
                "Taken":taken,
                "ToBeCommenced":toBeCommenced
            }
            final_data.append(dic)

        SchemeShare = MasterSanctionForm.objects.filter(Scheme__Scheme='Singara Chennai 2.0').aggregate(SchemeShare=Sum('SchemeShare'))
        ULBShare = MasterSanctionForm.objects.filter(Scheme__Scheme='Singara Chennai 2.0').aggregate(ULBShare=Sum('ULBShare'))
        ProjectCost = MasterSanctionForm.objects.filter(Scheme__Scheme='Singara Chennai 2.0').aggregate(
            ProjectCost=Sum('ApprovedProjectCost'))
        work_approved_total = MasterSanctionForm.objects.filter(Scheme__Scheme='Singara Chennai 2.0').count()
        work_amountspend = AgencyProgressModel.objects.filter(Scheme='Singara Chennai 2.0').aggregate(
            sum=Sum('valueofworkdone'))
        workorder_total = AgencySanctionModel.objects.filter(Scheme='Singara Chennai 2.0').aggregate(
            sum=Sum('work_awarded_amount1'))
        works_inprogress_total = AgencyProgressModel.objects.filter(Scheme='Singara Chennai 2.0').filter(status='In Progress').count()
        works_completed_total = AgencyProgressModel.objects.filter(Scheme='Singara Chennai 2.0').filter(status='Completed').count()
        works_taken_total = works_inprogress_total + works_completed_total
        works_ToBeCommenced = work_approved_total-works_taken_total
        Overall_value_work_done_completed  = AgencyProgressModel.objects.filter(Scheme='Singara Chennai 2.0').filter(status='Completed').aggregate(sum=Sum('valueofworkdone'))
        Overall_value_work_done_inprogress  = AgencyProgressModel.objects.filter(Scheme='Singara Chennai 2.0').filter(status='In Progress').aggregate(sum=Sum('valueofworkdone'))
        Overall_final = list(AgencyProgressModel.objects.values_list('Project_ID', flat=True).filter(Scheme='Singara Chennai 2.0').filter(
            status='Not Commenced'))
        Overall_TS_Awarded = AgencySanctionModel.objects.filter(Scheme='Singara Chennai 2.0').filter(ts_awarded='Yes').filter(Q(Project_ID__in=Overall_final)).count()
        Overall_WO_Awarded = AgencySanctionModel.objects.filter(Scheme='Singara Chennai 2.0').filter(wd_awarded='Yes').filter(Q(Project_ID__in=Overall_final)).count()
        extra_context = {
            'Overall_value_work_done_completed':Overall_value_work_done_completed,
            'Overall_value_work_done_inprogress':Overall_value_work_done_inprogress,
            'Overall_TS_Awarded':Overall_TS_Awarded,
            'Overall_WO_Awarded':Overall_WO_Awarded,
            'works_ToBeCommenced':works_ToBeCommenced,
            'work_amountspend':work_amountspend,
            'workorder_total':workorder_total,   
            'works_taken_total': works_taken_total,
            'works_inprogress_total': works_inprogress_total,
            'works_completed_total': works_completed_total,
            'work_approved_total': work_approved_total,
            'ProjectCost': ProjectCost,
            'ULBShare': ULBShare,
            'SchemeShare': SchemeShare,
            'final_data':final_data,
        }
        response.context_data.update(extra_context)
        return response

@admin.register(DistrictWiseReport)
class DistrictWiseReportAdmin(admin.ModelAdmin):
    change_list_template = "admin/districtreport.html"

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

        final_data = []
        district_list = list(MasterSanctionForm.objects.values_list('District__District', flat=True).order_by('District__District').filter(Scheme__Scheme='KNMT').all().distinct())
    
        for district in district_list:
            BTRoadNo = MasterSanctionForm.objects.filter(Sector='BT Road').filter(District__District=district).filter(Scheme__Scheme='KNMT').count()
            BTRoadCost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(District__District=district).filter(Scheme__Scheme='KNMT').aggregate(project_cost=Sum('ApprovedProjectCost'))
            BusStandNo = MasterSanctionForm.objects.filter(Sector='Bus Stand').filter(District__District=district).filter(Scheme__Scheme='KNMT').count()
            BusStandCost = MasterSanctionForm.objects.filter(Sector='Bus Stand').filter(District__District=district).filter(Scheme__Scheme='KNMT').aggregate(project_cost=Sum('ApprovedProjectCost'))
            CCRoadNo = MasterSanctionForm.objects.filter(Sector='CC Road').filter(District__District=district).filter(Scheme__Scheme='KNMT').count()
            CCRoadCost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(District__District=district).filter(Scheme__Scheme='KNMT').aggregate(project_cost=Sum('ApprovedProjectCost'))
            ClNo = MasterSanctionForm.objects.filter(Sector='Community Hall').filter(District__District=district).filter(Scheme__Scheme='KNMT').count()
            ClCost =  MasterSanctionForm.objects.filter(Sector='Community Hall').filter(District__District=district).filter(Scheme__Scheme='KNMT').aggregate(project_cost=Sum('ApprovedProjectCost'))
            CrematoriumNo = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(District__District=district).filter(Scheme__Scheme='KNMT').count()
            CrematoriumCost =  MasterSanctionForm.objects.filter(Sector='Crematorium').filter(District__District=district).filter(Scheme__Scheme='KNMT').aggregate(project_cost=Sum('ApprovedProjectCost'))
            CulvertNo =MasterSanctionForm.objects.filter(Sector='Culvert').filter(District__District=district).filter(Scheme__Scheme='KNMT').count()
            CulvertCost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(District__District=district).filter(Scheme__Scheme='KNMT').aggregate(project_cost=Sum('ApprovedProjectCost'))
            KC_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(District__District=district).filter(Scheme__Scheme='KNMT').count()
            KC_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(District__District=district).filter(Scheme__Scheme='KNMT').aggregate(project_cost=Sum('ApprovedProjectCost'))
            MarketNo = MasterSanctionForm.objects.filter(Sector='Market').filter(District__District=district).filter(Scheme__Scheme='KNMT').count()
            MarketCost = MasterSanctionForm.objects.filter(Sector='Market').filter(District__District=district).filter(Scheme__Scheme='KNMT').aggregate(project_cost=Sum('ApprovedProjectCost'))
            mbcbNo  = MasterSanctionForm.objects.filter(Sector='Metal Beam Crash Barriers').filter(District__District=district).filter(Scheme__Scheme='KNMT').count()
            mbcbCost = MasterSanctionForm.objects.filter(Sector='Metal Beam Crash Barriers').filter(District__District=district).filter(Scheme__Scheme='KNMT').aggregate(project_cost=Sum('ApprovedProjectCost'))
            ParksNo = MasterSanctionForm.objects.filter(Sector='Parks').filter(District__District=district).filter(Scheme__Scheme='KNMT').count()
            ParksCost = MasterSanctionForm.objects.filter(Sector='Parks').filter(District__District=district).filter(Scheme__Scheme='KNMT').aggregate(project_cost=Sum('ApprovedProjectCost'))
            PBno = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(District__District=district).filter(Scheme__Scheme='KNMT').count()
            PBCost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(District__District=district).filter(Scheme__Scheme='KNMT').aggregate(project_cost=Sum('ApprovedProjectCost'))
            RWno = MasterSanctionForm.objects.filter(Sector='Retaining wall').filter(District__District=district).filter(Scheme__Scheme='KNMT').count()
            RWCost = MasterSanctionForm.objects.filter(Sector='Retaining wall').filter(District__District=district).filter(Scheme__Scheme='KNMT').aggregate(project_cost=Sum('ApprovedProjectCost'))
            SWDno = MasterSanctionForm.objects.filter(Sector='SWD').filter(District__District=district).filter(Scheme__Scheme='KNMT').count()
            SWDCost = MasterSanctionForm.objects.filter(Sector='SWD').filter(District__District=district).filter(Scheme__Scheme='KNMT').aggregate(project_cost=Sum('ApprovedProjectCost'))
            SWMno = MasterSanctionForm.objects.filter(Sector='Solid Waste Mgt.').filter(District__District=district).filter(Scheme__Scheme='KNMT').count()
            SWMCost = MasterSanctionForm.objects.filter(Sector='Solid Waste Mgt.').filter(District__District=district).filter(Scheme__Scheme='KNMT').aggregate(project_cost=Sum('ApprovedProjectCost'))
            WBno = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(District__District=district).filter(Scheme__Scheme='KNMT').count()
            WBCost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(District__District=district).filter(Scheme__Scheme='KNMT').aggregate(project_cost=Sum('ApprovedProjectCost'))
            totalno = MasterSanctionForm.objects.filter(District__District=district).filter(Scheme__Scheme='KNMT').count()
            totalcost = MasterSanctionForm.objects.filter(District__District=district).filter(Scheme__Scheme='KNMT').aggregate(project_cost=Sum('ApprovedProjectCost'))
            
            dic = {
                "SWMno":SWMno,
                "SWMCost":SWMCost,
                "BusStandNo": BusStandNo,
                "BusStandCost": BusStandCost,
                "ClNo": ClNo,
                "ClCost": ClCost,
                "district": district,
                "BTRoadNo": BTRoadNo,
                "BTRoadCost": BTRoadCost,
                "CCRoadNo": CCRoadNo,
                "CCRoadCost": CCRoadCost,
                "CrematoriumNo": CrematoriumNo,
                "CrematoriumCost": CrematoriumCost,
                "CulvertNo": CulvertNo,
                "CulvertCost": CulvertCost,
                "mbcbNo":mbcbNo,
                "mbcbCost":mbcbCost,
                "RWno":RWno,
                "RWCost":RWCost,
                "KC_No": KC_No,
                "KC_Cost": KC_Cost,
                "MarketNo": MarketNo,
                "MarketCost": MarketCost,
                "ParksNo": ParksNo,
                "ParksCost": ParksCost,
                "PBno": PBno,
                "PBCost": PBCost,
                "SWDno": SWDno,
                "SWDCost": SWDCost,
                "WBno": WBno,
                "WBCost": WBCost,
                "totalno": totalno,
                "totalcost": totalcost,
            }
            final_data.append(dic)

        DMA_BT_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='BT Road').filter(Scheme__Scheme='KNMT').count()
        DMA_BT_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='BT Road').filter(Scheme__Scheme='KNMT').aggregate(project_cost=Sum('ApprovedProjectCost'))
        DMABusStandNo = MasterSanctionForm.objects.filter(Sector='Bus Stand').filter(Scheme__Scheme='KNMT').count()
        DMABusStandCost = MasterSanctionForm.objects.filter(Sector='Bus Stand').filter(Scheme__Scheme='KNMT').aggregate(project_cost=Sum('ApprovedProjectCost'))
        DMA_CC_RoadDMA_No = MasterSanctionForm.objects.filter(Sector='CC Road').filter(Scheme__Scheme='KNMT').count()
        DMA_CC_RoadDMA_Cost = MasterSanctionForm.objects.filter(Sector='CC Road').filter(Scheme__Scheme='KNMT').aggregate(project_cost=Sum('ApprovedProjectCost'))
        DMAClNo = MasterSanctionForm.objects.filter(Sector='Community Hall').filter(Scheme__Scheme='KNMT').count()
        DMAClCost =  MasterSanctionForm.objects.filter(Sector='Community Hall').filter(Scheme__Scheme='KNMT').aggregate(project_cost=Sum('ApprovedProjectCost'))
        DMA_CrematoriumDMA_No = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(Scheme__Scheme='KNMT').count()
        DMA_CrematoriumDMA_Cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(Scheme__Scheme='KNMT').aggregate(project_cost=Sum('ApprovedProjectCost'))
        DMA_CulvertDMA_No = MasterSanctionForm.objects.filter(Sector='Culvert').filter( Scheme__Scheme='KNMT').count()
        DMA_CulvertDMA_Cost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(Scheme__Scheme='KNMT').aggregate(project_cost=Sum('ApprovedProjectCost'))
        DMA_KnowledgeDMA_Centre_No = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(Scheme__Scheme='KNMT').count()
        DMA_KnowledgeDMA_Centre_Cost = MasterSanctionForm.objects.filter(Sector='Knowledge Centre').filter(Scheme__Scheme='KNMT').aggregate(project_cost=Sum('ApprovedProjectCost'))
        DMA_MarketDMA_No = MasterSanctionForm.objects.filter(Sector='Market').filter(Scheme__Scheme='KNMT').count()
        DMA_MarketDMA_Cost = MasterSanctionForm.objects.filter(Sector='Market').filter(Scheme__Scheme='KNMT').aggregate(project_cost=Sum('ApprovedProjectCost'))
        DMAmbcbNo  = MasterSanctionForm.objects.filter(Sector='Metal Beam Crash Barriers').filter(Scheme__Scheme='KNMT').count()
        DMAmbcbCost = MasterSanctionForm.objects.filter(Sector='Metal Beam Crash Barriers').filter(Scheme__Scheme='KNMT').aggregate(project_cost=Sum('ApprovedProjectCost'))
        DMA_ParksDMA_No = MasterSanctionForm.objects.filter(Sector='Parks').filter(Scheme__Scheme='KNMT').count()
        DMA_ParksDMA_Cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(Scheme__Scheme='KNMT').aggregate(project_cost=Sum('ApprovedProjectCost'))
        DMA_PaverBlockDMA_No = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(Scheme__Scheme='KNMT').count()
        DMA_PaverBlockDMA_Cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(Scheme__Scheme='KNMT').aggregate(project_cost=Sum('ApprovedProjectCost'))
        DMARWno = MasterSanctionForm.objects.filter(Sector='Retaining wall').filter(Scheme__Scheme='KNMT').count()
        DMARWCost = MasterSanctionForm.objects.filter(Sector='Retaining wall').filter(Scheme__Scheme='KNMT').aggregate(project_cost=Sum('ApprovedProjectCost'))
        DMASWMno = MasterSanctionForm.objects.filter(Sector='Solid Waste Mgt.').filter(Scheme__Scheme='KNMT').count()
        DMASWMCost = MasterSanctionForm.objects.filter(Sector='Solid Waste Mgt.').filter(Scheme__Scheme='KNMT').aggregate(project_cost=Sum('ApprovedProjectCost'))
        DMA_SWDDMA_No = MasterSanctionForm.objects.filter(Sector='SWD').filter(Scheme__Scheme='KNMT').count()
        DMA_SWDDMA_Cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(Scheme__Scheme='KNMT').aggregate(project_cost=Sum('ApprovedProjectCost'))
        DMA_WBDMA_No = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(Scheme__Scheme='KNMT').count()
        DMA_WBDMA_Cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(Scheme__Scheme='KNMT').aggregate(project_cost=Sum('ApprovedProjectCost'))
        DMA_total_no = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').count()
        DMA_total_cost = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').aggregate(project_cost=Sum('ApprovedProjectCost'))
        
        extra_context = {
            "DMARWno":DMARWno,
            "DMARWCost":DMARWCost,
            "DMASWMno":DMASWMno,
            "DMASWMCost":DMASWMCost,
            "DMABusStandNo":DMABusStandNo,
            "DMABusStandCost":DMABusStandCost,
            "DMAClNo":DMAClNo,
            "DMAClCost":DMAClCost,
            "DMAmbcbNo":DMAmbcbNo,
            "DMAmbcbCost":DMAmbcbCost,
            "final_data": final_data,
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
        }
        response.context_data.update(extra_context)
        response.context_data['KNMT_Sector'] = list(qs.values('Sector').filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').annotate(**metrics).order_by('Sector'))
        return response
