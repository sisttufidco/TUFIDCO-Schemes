from django.contrib import admin
from reports.models import *
from TUFIDCOapp.models import *
from django.db.models import Count, Sum, Avg, Func
from django.db.models import Q


# Register your models here.

@admin.register(ULBProgressReport)
class ULBProgressReportAdmin(admin.ModelAdmin):
    change_list_template = 'admin/progress_report.html'

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        a = AgencyProgressModel.objects.values_list('Project_ID', flat=True).filter(Scheme='KNMT')

        response.context_data['district_p'] = list(
            qs.values('District').order_by('District').filter(Scheme='KNMT').filter(
                Sector='Parks').filter(status='Not Commenced').annotate(count=Count('Project_ID'))
        )

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
        busstand_tobecommenced_count = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            Sector='Bus Stand').filter(status='Not Commenced').count()
        busstand_tobecommenced_project_cost = AgencyProgressModel.objects.filter(Sector='Bus Stand').filter(
            status='Not Commenced').aggregate(project_cost=Sum('ApprovedProjectCost'))

        busstand_district = AgencyProgressModel.objects.values('District').order_by('District').filter(
            Scheme='KNMT').filter(Sector='Bus Stand').filter(status='In Progress').annotate(
            percent=Sum('percentageofworkdone'))

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
        btroad_tobecommenced_count = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            Sector='BT Road').filter(status='Not Commenced').count()
        btroad_tobecommenced_project_cost = AgencyProgressModel.objects.filter(Sector='BT Road').filter(
            status='Not Commenced').aggregate(project_cost=Sum('ApprovedProjectCost'))

        btroad_district = AgencyProgressModel.objects.values('District').order_by('District').filter(
            Scheme='KNMT').filter(Sector='BT Road').filter(status='In Progress').annotate(
            percent=Sum('percentageofworkdone'))

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
        ccroad_tobecommenced_count = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            Sector='CC Road').filter(status='Not Commenced').count()
        ccroad_tobecommenced_project_cost = AgencyProgressModel.objects.filter(Sector='CC Road').filter(
            status='Not Commenced').aggregate(project_cost=Sum('ApprovedProjectCost'))
        ccroad_district = AgencyProgressModel.objects.values('District').order_by('District').filter(
            Scheme='KNMT').filter(Sector='CC Road').filter(status='In Progress').annotate(
            percent=Sum('percentageofworkdone'))

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
        communityhall_tobecommenced_count = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            Sector='Community Hall').filter(status='Not Commenced').count()
        communityhall_tobecommenced_project_cost = MasterSanctionForm.objects.filter(Sector='Community Hall').filter(
            ~Q(Project_ID__in=a)).aggregate(project_cost=Sum('ApprovedProjectCost'))

        communityhall_district = AgencyProgressModel.objects.values('District').order_by('District').filter(
            Scheme='KNMT').filter(Sector='Community Hall').filter(status='In Progress').annotate(
            percent=Sum('percentageofworkdone'))

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
        crematorium_tobecommenced_count = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            Sector='Crematorium').filter(status='Not Commenced').count()
        crematorium_tobecommenced_project_cost = MasterSanctionForm.objects.filter(Sector='Crematorium').filter(
            ~Q(Project_ID__in=a)).aggregate(project_cost=Sum('ApprovedProjectCost'))

        crematorium_district = AgencyProgressModel.objects.values('District').order_by('District').filter(
            Scheme='KNMT').filter(Sector='Crematorium').filter(status='In Progress').annotate(
            percent=Sum('percentageofworkdone'))

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
        culvert_tobecommenced_count = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            Sector='Culvert').filter(status='Not Commenced').count()
        culvert_tobecommenced_project_cost = MasterSanctionForm.objects.filter(Sector='Culvert').filter(
            ~Q(Project_ID__in=a)).aggregate(project_cost=Sum('ApprovedProjectCost'))

        culvert_district = AgencyProgressModel.objects.values('District').order_by('District').filter(
            Scheme='KNMT').filter(Sector='Culvert').filter(status='In Progress').annotate(
            percent=Sum('percentageofworkdone'))

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
        Market_tobecommenced_count = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            Sector='Market').filter(status='Not Commenced').count()
        Market_tobecommenced_project_cost = MasterSanctionForm.objects.filter(Sector='Market').filter(
            ~Q(Project_ID__in=a)).aggregate(project_cost=Sum('ApprovedProjectCost'))
        Market_district = AgencyProgressModel.objects.values('District').order_by('District').filter(
            Scheme='KNMT').filter(Sector='Market').filter(status='In Progress').annotate(
            percent=Sum('percentageofworkdone'))

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
        KnowledgeCentre_tobecommenced_count = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            Sector='Knowledge Centre').filter(status='Not Commenced').count()
        KnowledgeCentre_tobecommenced_project_cost = MasterSanctionForm.objects.filter(
            Sector='Knowledge Centre').filter(
            ~Q(Project_ID__in=a)).aggregate(project_cost=Sum('ApprovedProjectCost'))

        KnowledgeCentre_district = AgencyProgressModel.objects.values('District').order_by('District').filter(
            Scheme='KNMT').filter(Sector='Knowledge Centre').filter(status='In Progress').annotate(
            percent=Sum('percentageofworkdone'))
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
        MetalBeamCrashBarriers_tobecommenced_count = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            Sector='Metal Beam Crash Barriers').filter(status='Not Commenced').count()
        MetalBeamCrashBarriers_tobecommenced_project_cost = MasterSanctionForm.objects.filter(
            Sector='Metal Beam Crash Barriers').filter(
            ~Q(Project_ID__in=a)).aggregate(project_cost=Sum('ApprovedProjectCost'))
        MetalBeamCrashBarriers_district = AgencyProgressModel.objects.values('District').order_by('District').filter(
            Scheme='KNMT').filter(Sector='Metal Beam Crash Barriers').filter(status='In Progress').annotate(
            percent=Sum('percentageofworkdone'))

        Parks_approved_project_count = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector='Parks').count()
        Parks_approved_project_cost = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector='Parks').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Parks_completed_count = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            Sector='MetalBeam Crash Barriers').filter(
            status='Completed').count()
        Parks_completed_approved_project_cost = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            Sector='Parks').filter(status='Completed').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Parks_inprogress_count = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector='Parks').filter(
            status='In Progress').count()
        Parks_inprogress_approved_project_cost = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(
            Sector='Parks').filter(status='In Progress').aggregate(project_cost=Sum('ApprovedProjectCost'))
        Parks_tobecommenced_count = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector='Parks').filter(
            status='Not Commenced').count()
        Parks_tobecommenced_project_cost = MasterSanctionForm.objects.filter(Sector='Parks').filter(
            ~Q(Project_ID__in=a)).aggregate(project_cost=Sum('ApprovedProjectCost'))

        Parks_district = AgencyProgressModel.objects.values('District').order_by('District').filter(
            Scheme='KNMT').filter(Sector='Parks').filter(status='In Progress').annotate(
            percent=Sum('percentageofworkdone'))

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
            ~Q(Project_ID__in=a)).count()
        PaverBlock_tobecommenced_project_cost = MasterSanctionForm.objects.filter(Sector='Paver Block').filter(
            ~Q(Project_ID__in=a)).aggregate(project_cost=Sum('ApprovedProjectCost'))

        PaverBlock_district = AgencyProgressModel.objects.values('District').order_by('District').filter(
            Scheme='KNMT').filter(Sector='Paver Block').filter(status='In Progress').annotate(
            percent=Sum('percentageofworkdone'))

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
            ~Q(Project_ID__in=a)).count()
        Retainingwall_tobecommenced_project_cost = MasterSanctionForm.objects.filter(Sector='Retaining wall').filter(
            ~Q(Project_ID__in=a)).aggregate(project_cost=Sum('ApprovedProjectCost'))
        Retainingwall_district = AgencyProgressModel.objects.values('District').order_by('District').filter(
            Scheme='KNMT').filter(Sector='Retaining wall').filter(status='In Progress').annotate(
            percent=Sum('percentageofworkdone'))

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
            ~Q(Project_ID__in=a)).count()
        SolidWasteMgt_tobecommenced_project_cost = MasterSanctionForm.objects.filter(Sector='Solid Waste Mgt.').filter(
            ~Q(Project_ID__in=a)).aggregate(project_cost=Sum('ApprovedProjectCost'))
        SolidWasteMgt_district = AgencyProgressModel.objects.values('District').order_by('District').filter(
            Scheme='KNMT').filter(Sector='Solid Waste Mgt.').filter(status='In Progress').annotate(
            percent=Sum('percentageofworkdone'))
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
            ~Q(Project_ID__in=a)).count()
        SWD_tobecommenced_project_cost = MasterSanctionForm.objects.filter(Sector='SWD').filter(
            ~Q(Project_ID__in=a)).aggregate(project_cost=Sum('ApprovedProjectCost'))

        SWD_district = AgencyProgressModel.objects.values('District').order_by('District').filter(
            Scheme='KNMT').filter(Sector='SWD').filter(status='In Progress').annotate(
            percent=Sum('percentageofworkdone'))
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
            ~Q(Project_ID__in=a)).count()
        WaterBodies_tobecommenced_project_cost = MasterSanctionForm.objects.filter(Sector='Water Bodies').filter(
            ~Q(Project_ID__in=a)).aggregate(project_cost=Sum('ApprovedProjectCost'))

        WaterBodies_district = AgencyProgressModel.objects.values('District').order_by('District').filter(
            Scheme='KNMT').filter(Sector='Water Bodies').filter(status='In Progress').annotate(
            percent=Sum('percentageofworkdone'))

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
            ~Q(Project_ID__in=a)).count()
        total_tobecommenced_project_cost = MasterSanctionForm.objects.filter(
            ~Q(Project_ID__in=a)).aggregate(project_cost=Sum('ApprovedProjectCost'))

        total_district = AgencyProgressModel.objects.values('District').order_by('District').filter(
            Scheme='KNMT').filter(status='In Progress').annotate(
            percent=Sum('percentageofworkdone'))

        metrics = {

        }

        extra_context = {
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

            'MetalBeamCrashBarriers_district': MetalBeamCrashBarriers_district,
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

        }

        response.context_data.update(extra_context)
        return response
