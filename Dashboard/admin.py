from django.contrib import admin
from .models import *
from django.db.models import Count, Sum, Avg, Func
from django.db.models import Q
from TUFIDCOapp.models import *
from ULBForms.models import *

# Register your models here.
class Round(Func):
    function = "ROUND"
    arity = 2


@admin.register(SingaraChennaiDashboard)
class DashboardSingaraAdmin(admin.ModelAdmin):
    change_list_template = "admin/dashboard2.html"

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        a = AgencyProgressModel.objects.values_list('Project_ID', flat=True).filter(Scheme='Singara Chennai 2.0').filter(status='Completed')
        b = AgencyProgressModel.objects.values_list('Project_ID', flat=True).filter(Scheme='Singara Chennai 2.0').filter(status='In Progress')

        total_projects = MasterSanctionForm.objects.filter(Scheme__Scheme='Singara Chennai 2.0').count()
        project_cost = MasterSanctionForm.objects.filter(Scheme__Scheme='Singara Chennai 2.0').aggregate(project_cost=Sum('ApprovedProjectCost'))
        singara = MasterSanctionForm.objects.filter(Scheme__Scheme='Singara Chennai 2.0').aggregate(singara_share=Sum('SchemeShare'))
        ulb_share = MasterSanctionForm.objects.filter(Scheme__Scheme='Singara Chennai 2.0').aggregate(ulb_share=Sum('ULBShare'))

        list_agency_progress = list(AgencyProgressModel.objects.values_list('Project_ID', flat=True).filter(Scheme='Singara Chennai 2.0').filter(status='In Progress'))
        list_agency_completed = list(AgencyProgressModel.objects.values_list('Project_ID', flat=True).filter(Scheme='Singara Chennai 2.0').filter(status='Completed'))
        final_list = list_agency_progress + list_agency_completed


        progress_report = []
        sector_list = list(MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(Scheme__Scheme='Singara Chennai 2.0').distinct())
        for sector in sector_list:
            total_project_sector = MasterSanctionForm.objects.filter(Scheme__Scheme='Singara Chennai 2.0').filter(Sector=sector).count()
            total_approved_project_cost_sector = MasterSanctionForm.objects.filter(Scheme__Scheme='Singara Chennai 2.0').filter(Sector=sector).aggregate(project_cost=Sum('ApprovedProjectCost'))
            completed_count =  AgencyProgressModel.objects.filter(Scheme='Singara Chennai 2.0').filter(Sector=sector).filter(status='Completed').count()
            completed_approved_project_cost = AgencyProgressModel.objects.filter(Scheme='Singara Chennai 2.0').filter(Sector=sector).filter(status='Completed').aggregate(project_cost=Sum('ApprovedProjectCost'))
            inprogress_count = AgencyProgressModel.objects.filter(Scheme='Singara Chennai 2.0').filter(Sector=sector).filter(status='In Progress').count()
            inprogress_approved_project_cost = AgencyProgressModel.objects.filter(Scheme='Singara Chennai 2.0').filter(Sector=sector).filter(status='In Progress').aggregate(project_cost=Sum('ApprovedProjectCost'))
            tobecommenced_count = MasterSanctionForm.objects.filter(Scheme__Scheme='Singara Chennai 2.0').filter(Sector=sector).filter(~Q(Project_ID__in=final_list)).count()
            tobecommenced_project_cost = MasterSanctionForm.objects.filter(Scheme__Scheme='Singara Chennai 2.0').filter(Sector=sector).filter(~Q(Project_ID__in=final_list)).aggregate(project_cost=Sum('ApprovedProjectCost'))
            modal_data = list(MasterSanctionForm.objects.values('zone', 'Project_ID').order_by('zone').filter(Scheme__Scheme='Singara Chennai 2.0').filter(Sector=sector).filter(~Q(Project_ID__in=a)).filter(~Q(Project_ID__in=b)))
            in_progress = list(MasterSanctionForm.objects.values('zone', 'Project_ID').order_by('zone').filter(Scheme__Scheme='Singara Chennai 2.0').filter(Sector=sector).filter(Q(Project_ID__in=b)))
            
            dic = {
                "in_progress":in_progress,
                "Sector": sector,
                "total_project_sector": total_project_sector,
                "total_approved_project_cost_sector": total_approved_project_cost_sector,
                "completed_count": completed_count,
                "completed_approved_project_cost": completed_approved_project_cost,
                "inprogress_count": inprogress_count,
                "inprogress_approved_project_cost":inprogress_approved_project_cost,
                "tobecommenced_count":tobecommenced_count,
                "tobecommenced_project_cost":tobecommenced_project_cost,
                "modal_data":modal_data,
            }
            progress_report.append(dic)
  
        total_approved_project_count = MasterSanctionForm.objects.filter(Scheme__Scheme='Singara Chennai 2.0').count()
        total_approved_project_cost = MasterSanctionForm.objects.filter(Scheme__Scheme='Singara Chennai 2.0').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        total_completed_count = AgencyProgressModel.objects.filter(Scheme='Singara Chennai 2.0').filter(
            status='Completed').count()
        total_completed_approved_project_cost = AgencyProgressModel.objects.filter(Scheme='Singara Chennai 2.0').filter(
            status='Completed').aggregate(project_cost=Sum('ApprovedProjectCost'))
        total_inprogress_count = AgencyProgressModel.objects.filter(Scheme='Singara Chennai 2.0').filter(
            status='In Progress').count()
        total_inprogress_approved_project_cost = AgencyProgressModel.objects.filter(
            Scheme='Singara Chennai 2.0').filter(
            status='In Progress').aggregate(project_cost=Sum('ApprovedProjectCost'))
        total_tobecommenced_count = MasterSanctionForm.objects.filter(Scheme__Scheme='Singara Chennai 2.0').filter(
            ~Q(Project_ID__in=final_list)).count()
        total_tobecommenced_project_cost = MasterSanctionForm.objects.filter(
            Scheme__Scheme='Singara Chennai 2.0').filter(
            ~Q(Project_ID__in=final_list)).aggregate(project_cost=Sum('ApprovedProjectCost'))

        extra_context = {
            'progress_report':progress_report,
            'total_tobecommenced_project_cost': total_tobecommenced_project_cost,
            'total_tobecommenced_count': total_tobecommenced_count,
            'total_inprogress_approved_project_cost': total_inprogress_approved_project_cost,
            'total_inprogress_count': total_inprogress_count,
            'total_completed_approved_project_cost': total_completed_approved_project_cost,
            'total_completed_count': total_completed_count,
            'total_approved_project_cost': total_approved_project_cost,
            'total_approved_project_count': total_approved_project_count,
            'total_projects': total_projects,
            'project_cost': project_cost,
            'singara': singara,
            'ulb_share': ulb_share,
        }
        metrics = {
            'Sector_total': Sum('ApprovedProjectCost'),
            'Sector_count': Count('Project_ID'),
        }

        response.context_data['pie_chart_sector'] = list(
            qs.values('Sector').filter(Scheme__Scheme='Singara Chennai 2.0').annotate(**metrics).order_by('Sector'))
    
        response.context_data.update(extra_context)
        return response


@admin.register(KNMTDashboard)
class DashboardAdmin(admin.ModelAdmin):
    change_list_template = "admin/dashboard.html"

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response
        
        total_projects = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').count()
        project_cost = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').aggregate(project_cost=Sum('ApprovedProjectCost'))
        dmp_project_cost = MasterSanctionForm.objects.filter(AgencyType__AgencyType='Municipality').filter(Scheme__Scheme='KNMT').aggregate(dmp_project_cost=Sum('ApprovedProjectCost'))
        ctp_project_cost = MasterSanctionForm.objects.filter(AgencyType__AgencyType='Town Panchayat').filter(Scheme__Scheme='KNMT').aggregate(ctp_project_cost=Sum('ApprovedProjectCost'))

        sector_list = list(MasterSanctionForm.objects.values_list('Sector', flat=True).all().distinct().filter(Scheme__Scheme='KNMT').exclude(Sector__in=['BT Road', 'CC Road', 'Retaining wall', 'Paver Block', 'SWD', 'Culvert',
                        'Metal Beam Crash Barriers']))
        swps_final_list = []
        
        for sector in sector_list:
            sector_total = MasterSanctionForm.objects.filter(Sector=sector).filter(Scheme__Scheme='KNMT').count()
            sector_cost = MasterSanctionForm.objects.filter(Sector=sector).filter(Scheme__Scheme='KNMT').aggregate(project_cost=Sum('ApprovedProjectCost'))
            try:
                sector_percentage = "{:.2f}".format((sector_cost['project_cost']) / (project_cost['project_cost']) * 100)
            except TypeError:
                sector_percentage = 0.0
            DMA_total = MasterSanctionForm.objects.filter(Sector=sector).filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType="Municipality").count()
            DMA_cost = MasterSanctionForm.objects.filter(Sector=sector).filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType="Municipality").aggregate(project_cost=Sum('ApprovedProjectCost'))
            try:
                DMA_percentage = "{:.2f}".format((DMA_cost['project_cost']) / (dmp_project_cost['dmp_project_cost']) * 100)
            except TypeError:
                DMA_percentage = 0.0
            CTP_total = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector=sector).filter(AgencyType__AgencyType="Town Panchayat").count()
            CTP_cost = MasterSanctionForm.objects.filter(Sector=sector).filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType="Town Panchayat").aggregate(project_cost=Sum('ApprovedProjectCost'))
            try:
                CTP_percentage = "{:.2f}".format((CTP_cost['project_cost']) / (ctp_project_cost['ctp_project_cost']) * 100)
            except TypeError:
                CTP_percentage = 0.0
            dic = {
                "sector_total":sector_total,
                "sector_cost":sector_cost,
                "sector_percentage":sector_percentage,
                "DMA_total":DMA_total,
                "DMA_cost":DMA_cost,
                "DMA_percentage":DMA_percentage,
                "CTP_total":CTP_total,
                "CTP_cost":CTP_cost,
                "CTP_percentage":CTP_percentage,
                "sector":sector
            }
            swps_final_list.append(dic)

        road = MasterSanctionForm.objects.filter(Sector__in=['BT Road', 'CC Road', 'Retaining wall', 'Paver Block', 'SWD', 'Culvert','Metal Beam Crash Barriers']).filter(Scheme__Scheme='KNMT').aggregate(project_cost=Sum('ApprovedProjectCost'))
        road_total = MasterSanctionForm.objects.filter(Sector__in=['BT Road', 'CC Road', 'Retaining wall', 'Paver Block', 'SWD', 'Culvert','Metal Beam Crash Barriers']).filter(Scheme__Scheme='KNMT').count()
        road_pt = "{:.2f}".format((road['project_cost']) / (project_cost['project_cost']) * 100)
        roadDMA = MasterSanctionForm.objects.filter(Sector__in=['BT Road', 'CC Road', 'Retaining wall', 'Paver Block', 'SWD', 'Culvert','Metal Beam Crash Barriers']).filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType="Municipality").aggregate(project_cost=Sum('ApprovedProjectCost'))
        roadDMA_total = MasterSanctionForm.objects.filter(Sector__in=['BT Road', 'CC Road', 'Retaining wall', 'Paver Block', 'SWD', 'Culvert','Metal Beam Crash Barriers']).filter(AgencyType__AgencyType="Municipality").filter(Scheme__Scheme='KNMT').count()
        DMAroad_percentage = "{:.2f}".format((roadDMA['project_cost']) / (dmp_project_cost['dmp_project_cost']) * 100)
        roadCTP = MasterSanctionForm.objects.filter(Sector__in=['BT Road', 'CC Road', 'Retaining wall', 'Paver Block', 'SWD', 'Culvert', 'Metal Beam Crash Barriers']).filter(AgencyType__AgencyType="Town Panchayat").filter(Scheme__Scheme='KNMT').aggregate(project_cost=Sum('ApprovedProjectCost'))
        roadCTP_total = MasterSanctionForm.objects.filter(Sector__in=['BT Road', 'CC Road', 'Retaining wall', 'Paver Block', 'SWD', 'Culvert', 'Metal Beam Crash Barriers']).filter(AgencyType__AgencyType="Town Panchayat").filter(Scheme__Scheme='KNMT').count()
        CTProad_percentage = "{:.2f}".format((roadCTP['project_cost']) / (ctp_project_cost['ctp_project_cost']) * 100)
        dic2 = {
            "sector_total":road_total,
            "sector_cost":road,
            "sector_percentage":road_pt,
            "DMA_total":roadDMA_total,
            "DMA_cost":roadDMA,
            "DMA_percentage":DMAroad_percentage,
            "CTP_total": roadCTP_total,
            "CTP_cost":roadCTP,
            "CTP_percentage":CTProad_percentage,
            "sector": "Road Works",
        }
        swps_final_list.append(dic2)
        newlist = sorted(swps_final_list, key=lambda d: d['sector']) 

        sector_progress = []
        sector_progress_list = list(MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').all().distinct().filter(Scheme__Scheme='KNMT'))

        list_agency_progress = list(AgencyProgressModel.objects.values_list('Project_ID', flat=True).filter(Scheme='KNMT').filter(status='In Progress'))
        list_agency_completed = list(AgencyProgressModel.objects.values_list('Project_ID', flat=True).filter(Scheme='KNMT').filter(status='Completed'))
        final_list = list_agency_progress + list_agency_completed

        for sector in sector_progress_list:
            approved_project_count = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector=sector).count()
            approved_project_cost = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector=sector).aggregate(project_cost=Sum('ApprovedProjectCost'))
            completed_count = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector=sector).filter(status='Completed').count()
            completed_approved_project_cost = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector=sector).filter(status='Completed').aggregate(project_cost=Sum('ApprovedProjectCost'))
            inprogress_count = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector=sector).filter(status='In Progress').count()
            inprogress_approved_project_cost = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector=sector).filter(status='In Progress').aggregate(project_cost=Sum('ApprovedProjectCost'))
            tobecommenced_count = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector=sector).filter(~Q(Project_ID__in=final_list)).count()
            tobecommenced_project_cost = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector=sector).filter(~Q(Project_ID__in=final_list)).aggregate(project_cost=Sum('ApprovedProjectCost'))
            awarded_cost = AgencySanctionModel.objects.filter(Scheme='KNMT').filter(Sector=sector).aggregate(project_cost=Sum('work_awarded_amount1'))
            modal_data = list(MasterSanctionForm.objects.values('AgencyName__AgencyName', 'Project_ID').order_by('AgencyName__AgencyName').filter(Scheme__Scheme='KNMT').filter(Sector=sector).filter(~Q(Project_ID__in=final_list)))
            in_progress = list(AgencyProgressModel.objects.values('ULBName', 'Project_ID', 'percentageofworkdone').order_by('ULBName').filter(Scheme='KNMT').filter(Sector=sector).filter(status='In Progress').annotate(percent=Avg('percentageofworkdone')))
           


            progress_dic = {
                "approved_project_count":approved_project_count,
                "approved_project_cost":approved_project_cost,
                "completed_count":completed_count,
                "completed_approved_project_cost":completed_approved_project_cost,
                "inprogress_count":inprogress_count,
                "inprogress_approved_project_cost":inprogress_approved_project_cost,
                "tobecommenced_count":tobecommenced_count,
                "tobecommenced_project_cost":tobecommenced_project_cost,
                "awarded_cost":awarded_cost,
                "Sector":sector,
                "modal_data":modal_data,
                "in_progress":in_progress,
            }    

            sector_progress.append(progress_dic)

        DMAsector_progress = []
        DMAsector_progress_list = list(MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').all().distinct().filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType="Municipality"))
        
        for sector in DMAsector_progress_list:
            approved_project_count = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType="Municipality").filter(Sector=sector).count()
            approved_project_cost = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType="Municipality").filter(Sector=sector).aggregate(project_cost=Sum('ApprovedProjectCost'))
            completed_count = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector=sector).filter(ULBType="Municipality").filter(status='Completed').count()
            completed_approved_project_cost = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(ULBType="Municipality").filter(Sector=sector).filter(status='Completed').aggregate(project_cost=Sum('ApprovedProjectCost'))
            inprogress_count = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(ULBType="Municipality").filter(Sector=sector).filter(status='In Progress').count()
            inprogress_approved_project_cost = AgencyProgressModel.objects.filter(ULBType="Municipality").filter(Scheme='KNMT').filter(Sector=sector).filter(status='In Progress').aggregate(project_cost=Sum('ApprovedProjectCost'))
            tobecommenced_count = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType="Municipality").filter(Sector=sector).filter(~Q(Project_ID__in=final_list)).count()
            tobecommenced_project_cost = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType="Municipality").filter(Sector=sector).filter(~Q(Project_ID__in=final_list)).aggregate(project_cost=Sum('ApprovedProjectCost'))
            awarded_cost = AgencySanctionModel.objects.filter(Scheme='KNMT').filter(Sector=sector).filter(ULBType="Municipality").aggregate(project_cost=Sum('work_awarded_amount1'))
            modal_data = list(MasterSanctionForm.objects.values('AgencyName__AgencyName', 'Project_ID').order_by('AgencyName__AgencyName').filter(AgencyType__AgencyType="Municipality").filter(Scheme__Scheme='KNMT').filter(Sector=sector).filter(~Q(Project_ID__in=final_list)))
            in_progress = list(AgencyProgressModel.objects.values('ULBName', 'Project_ID', 'percentageofworkdone').order_by('ULBName').filter(ULBType="Municipality").filter(Scheme='KNMT').filter(Sector=sector).filter(status='In Progress').annotate(percent=Avg('percentageofworkdone')))

            progress_dic = {
                "approved_project_count":approved_project_count,
                "approved_project_cost":approved_project_cost,
                "completed_count":completed_count,
                "completed_approved_project_cost":completed_approved_project_cost,
                "inprogress_count":inprogress_count,
                "inprogress_approved_project_cost":inprogress_approved_project_cost,
                "tobecommenced_count":tobecommenced_count,
                "tobecommenced_project_cost":tobecommenced_project_cost,
                "awarded_cost":awarded_cost,
                "Sector":sector,
                "modal_data":modal_data,
                "in_progress":in_progress,
            }    

            DMAsector_progress.append(progress_dic)
        
        CTPsector_progress = []
        CTPsector_progress_list = list(MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').all().distinct().filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType="Town Panchayat"))
        
        for sector in CTPsector_progress_list:
            approved_project_count = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType="Town Panchayat").filter(Sector=sector).count()
            approved_project_cost = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType="Town Panchayat").filter(Sector=sector).aggregate(project_cost=Sum('ApprovedProjectCost'))
            completed_count = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector=sector).filter(ULBType="Town Panchayat").filter(status='Completed').count()
            completed_approved_project_cost = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(ULBType="Town Panchayat").filter(Sector=sector).filter(status='Completed').aggregate(project_cost=Sum('ApprovedProjectCost'))
            inprogress_count = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(ULBType="Town Panchayat").filter(Sector=sector).filter(status='In Progress').count()
            inprogress_approved_project_cost = AgencyProgressModel.objects.filter(ULBType="Town Panchayat").filter(Scheme='KNMT').filter(Sector=sector).filter(status='In Progress').aggregate(project_cost=Sum('ApprovedProjectCost'))
            tobecommenced_count = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType="Town Panchayat").filter(Sector=sector).filter(~Q(Project_ID__in=final_list)).count()
            tobecommenced_project_cost = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType="Town Panchayat").filter(Sector=sector).filter(~Q(Project_ID__in=final_list)).aggregate(project_cost=Sum('ApprovedProjectCost'))
            awarded_cost = AgencySanctionModel.objects.filter(Scheme='KNMT').filter(Sector=sector).filter(ULBType="Town Panchayat").aggregate(project_cost=Sum('work_awarded_amount1'))
            modal_data = list(MasterSanctionForm.objects.values('AgencyName__AgencyName', 'Project_ID').order_by('AgencyName__AgencyName').filter(AgencyType__AgencyType="Town Panchayat").filter(Scheme__Scheme='KNMT').filter(Sector=sector).filter(~Q(Project_ID__in=final_list)))
            in_progress = list(AgencyProgressModel.objects.values('ULBName', 'Project_ID', 'percentageofworkdone').order_by('ULBName').filter(ULBType="Town Panchayat").filter(Scheme='KNMT').filter(Sector=sector).filter(status='In Progress').annotate(percent=Avg('percentageofworkdone')))

            progress_dic = {
                "approved_project_count":approved_project_count,
                "approved_project_cost":approved_project_cost,
                "completed_count":completed_count,
                "completed_approved_project_cost":completed_approved_project_cost,
                "inprogress_count":inprogress_count,
                "inprogress_approved_project_cost":inprogress_approved_project_cost,
                "tobecommenced_count":tobecommenced_count,
                "tobecommenced_project_cost":tobecommenced_project_cost,
                "awarded_cost":awarded_cost,
                "Sector":sector,
                "modal_data":modal_data,
                "in_progress":in_progress,
            }    

            CTPsector_progress.append(progress_dic)

        district_list = MasterSanctionForm.objects.values_list('District__District', flat=True).order_by('District__District').filter(Scheme__Scheme='KNMT').distinct()
        district_map = []
        for district in district_list:
            District_project_cost = MasterSanctionForm.objects.filter(District__District=district).aggregate(project_cost=Sum('ApprovedProjectCost'))
            District_total_projects = MasterSanctionForm.objects.filter(District__District=district).count()
            DMA_project_cost = MasterSanctionForm.objects.filter(District__District=district).filter(AgencyType__AgencyType='Municipality').aggregate(project_cost=Sum('ApprovedProjectCost'))
            DMA_total_projects = MasterSanctionForm.objects.filter(District__District=district).filter(AgencyType__AgencyType='Municipality').count()
            CTP_project_cost = MasterSanctionForm.objects.filter(District__District=district).filter(AgencyType__AgencyType='Town Panchayat').aggregate(project_cost=Sum('ApprovedProjectCost'))
            CTP_total_projects = MasterSanctionForm.objects.filter(District__District=district).filter(AgencyType__AgencyType='Town Panchayat').count()
            Latitude = list(District.objects.values_list('Latitude', flat=True).filter(District=district))[0]
            Longitude = list(District.objects.values_list('Longitude', flat=True).filter(District=district))[0]

            district_dic = {
                'district':district,
                'project_cost':District_project_cost,
                'total_projects':District_total_projects,
                'DMA_project_cost':DMA_project_cost,
                'DMA_total_projects':DMA_total_projects,
                'CTP_project_cost':CTP_project_cost,
                'CTP_total_projects':CTP_total_projects,
                'Latitude':Latitude,
                'Longitude':Longitude,
            }
            district_map.append(district_dic)

        
        
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
        
        total_awarded_cost = AgencySanctionModel.objects.filter(Scheme='KNMT').aggregate(
            project_cost=Sum('work_awarded_amount1'))
        total_ap_project_count = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').count()
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
        total_tobecommenced_project_cost = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            ~Q(Project_ID__in=final_list)).aggregate(project_cost=Sum('ApprovedProjectCost'))

        DMAtotal_awarded_cost = AgencySanctionModel.objects.filter(Scheme='KNMT').filter(
            ULBType='Municipality').aggregate(
            project_cost=Sum('work_awarded_amount1'))
        DMAtotal_approved_project_count = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').count()
        DMAtotal_approved_project_cost = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        DMAtotal_completed_count = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            ULBType='Municipality').filter(
            status='Completed').count()
        DMAtotal_completed_approved_project_cost = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            ULBType='Municipality').filter(
            status='Completed').aggregate(project_cost=Sum('ApprovedProjectCost'))
        DMAtotal_inprogress_count = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            ULBType='Municipality').filter(
            status='In Progress').count()
        DMAtotal_inprogress_approved_project_cost = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            ULBType='Municipality').filter(
            status='In Progress').aggregate(project_cost=Sum('ApprovedProjectCost'))
        DMAtotal_tobecommenced_count = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').filter(
            ~Q(Project_ID__in=final_list)).count()
        DMAtotal_tobecommenced_project_cost = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Municipality').filter(
            ~Q(Project_ID__in=final_list)).aggregate(project_cost=Sum('ApprovedProjectCost'))

        CTPtotal_awarded_cost = AgencySanctionModel.objects.filter(Scheme='KNMT').filter(
            ULBType='Town Panchayat').aggregate(
            project_cost=Sum('work_awarded_amount1'))
        CTPtotal_approved_project_count = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').count()
        CTPtotal_approved_project_cost = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').aggregate(
            project_cost=Sum('ApprovedProjectCost'))
        CTPtotal_completed_count = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            ULBType='Town Panchayat').filter(
            status='Completed').count()
        CTPtotal_completed_approved_project_cost = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            ULBType='Town Panchayat').filter(
            status='Completed').aggregate(project_cost=Sum('ApprovedProjectCost'))
        CTPtotal_inprogress_count = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            ULBType='Town Panchayat').filter(
            status='In Progress').count()
        CTPtotal_inprogress_approved_project_cost = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            ULBType='Town Panchayat').filter(
            status='In Progress').aggregate(project_cost=Sum('ApprovedProjectCost'))
        CTPtotal_tobecommenced_count = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').filter(
            ~Q(Project_ID__in=final_list)).count()
        CTPtotal_tobecommenced_project_cost = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            AgencyType__AgencyType='Town Panchayat').filter(
            ~Q(Project_ID__in=final_list)).aggregate(project_cost=Sum('ApprovedProjectCost'))

        

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

        

       
        district_info = District.objects.exclude(District='Chennai').all()

        

      
        extra_context = {
            'CTPsector_progress':CTPsector_progress,
            'DMAsector_progress':DMAsector_progress,
            'sector_progress':sector_progress,
            'swps_final_list':newlist,
            'district_map':district_map,
            'CTPRW_pt': CTPRW_pt,
            'RWDMA_pt': RWDMA_pt,
            'rw_pt': rw_pt,
            'total_awarded_cost':total_awarded_cost,
            'total_ap_project_count':total_ap_project_count,
            'total_approved_project_cost':total_approved_project_cost,
            'total_completed_count':total_completed_count,
            'total_completed_approved_project_cost':total_completed_approved_project_cost,
            'total_inprogress_count':total_inprogress_count,
            'total_inprogress_approved_project_cost':total_inprogress_approved_project_cost,
            'total_tobecommenced_count':total_tobecommenced_count,
            'total_tobecommenced_project_cost':total_tobecommenced_project_cost,
            'DMAtotal_awarded_cost':DMAtotal_awarded_cost,
            'DMAtotal_approved_project_count':DMAtotal_approved_project_count,
            'DMAtotal_approved_project_cost':DMAtotal_approved_project_cost,
            'DMAtotal_completed_count':DMAtotal_completed_count,
            'DMAtotal_completed_approved_project_cost':DMAtotal_completed_approved_project_cost,
            'DMAtotal_inprogress_count':DMAtotal_inprogress_count,
            'DMAtotal_inprogress_approved_project_cost':DMAtotal_inprogress_approved_project_cost,
            'DMAtotal_tobecommenced_count':DMAtotal_tobecommenced_count,
            'DMAtotal_tobecommenced_project_cost':DMAtotal_tobecommenced_project_cost,
            'CTPtotal_awarded_cost':CTPtotal_awarded_cost,
            'CTPtotal_approved_project_count':CTPtotal_approved_project_count,
            'CTPtotal_approved_project_cost':CTPtotal_approved_project_cost,
            'CTPtotal_completed_count':CTPtotal_completed_count,
            'CTPtotal_completed_approved_project_cost':CTPtotal_completed_approved_project_cost,
            'CTPtotal_inprogress_count':CTPtotal_inprogress_count,
            'CTPtotal_inprogress_approved_project_cost':CTPtotal_inprogress_approved_project_cost,
            'CTPtotal_tobecommenced_count':CTPtotal_tobecommenced_count,
            'CTPtotal_tobecommenced_project_cost':CTPtotal_tobecommenced_project_cost,

            
            'district_info': district_info,
            

            'pie_chart_CTP': pie_chart_CTP,
            'donut_chart_CTP': donut_chart_CTP,
            'donut_chart_sectorDMA': donut_chart_sectorDMA,
            'pie_chart_sectorDMA': pie_chart_sectorDMA,
            'ulb_share_ulb': ulb_share_ulb,
            'ulb_knmt_share': ulb_knmt_share,
            'ulb_project_cost': ulb_project_cost,
            'ulb_total_project': ulb_total_project,
           
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
           
        }

        response.context_data.update(extra_context)
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
        return response
