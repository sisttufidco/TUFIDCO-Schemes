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
    change_list_template = "admin/DMAcompletedreport.html"

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response
        
        return response
