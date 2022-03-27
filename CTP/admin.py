from django.contrib import admin
from CTP.models import *
from django.db.models import Count, Sum, Avg, Func

# Register your models here.

@admin.register(TownPanchayatDetails)
class TownPanchayatDetailsAdmin(admin.ModelAdmin):
    exclude = ['user', 'date_and_time']

    search_fields = [
        'user__first_name',
        'district',
        'date_and_time'
    ]

    list_display = [
        'name_tp',
        'district',
        'zone',
        'cell1',
        'email',
        'date_and_time'
    ]

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.date_and_time = datetime.now()
        obj.save()

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context.update({
            'show_save': True,
            'show_save_and_add_another': False,
        })
        return super().render_change_form(request, context, add, change, form_url, obj)

    def get_queryset(self, request):
        qs = super(TownPanchayatDetailsAdmin, self).get_queryset(request)
        if not request.user.groups.filter(name__in=["Admin", ]).exists():
            return qs.filter(user=request.user)
        return qs

    def has_add_permission(self, request, *args, **kwargs):
        return not TownPanchayatDetails.objects.filter(user=request.user).exists() and not request.user.groups.filter(
            name__in=[
                "Admin", "CMD_DGM"]).exists()


@admin.register(MasterReport)
class MasterReportAdmin(admin.ModelAdmin):
    change_list_template = 'admin/CTPPhysicalAndFinancialReport.html'

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
        BT_Road_SchemeShare = MasterSanctionForm.objects.filter(Scheme__Scheme="KNMT").filter(AgencyType__AgencyType='Town Panchayat').filter(
            Sector="BT Road").aggregate(BT_Road_SchemeShare=Sum('SchemeShare'))
        BT_Road_ULBShare = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').filter(Sector='BT Road').aggregate(
            BT_Road_ULBShare=Sum('ULBShare'))
        BT_Road_Total = BT_Road_SchemeShare['BT_Road_SchemeShare'] + BT_Road_ULBShare['BT_Road_ULBShare']
        BT_Road_Approved = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector='BT Road').filter(AgencyType__AgencyType='Town Panchayat').count()
        BT_Road_amountspend = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(ULBType='Town Panchayat').filter(Sector='BT Road').aggregate(sum=Sum('valueofworkdone'))
        BT_Road_workorder  = AgencySanctionModel.objects.filter(Scheme='KNMT').filter(ULBType='Town Panchayat').filter(Sector='BT Road').aggregate(sum=Sum('work_awarded_amount1'))
        BT_Road_Completed = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(ULBType='Town Panchayat').filter(Sector='BT Road').filter(
            status='Completed').count()
        BT_Road_inprogress = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(ULBType='Town Panchayat').filter(Sector='BT Road').filter(
            status='In Progress').count()
        BT_Road_Taken = BT_Road_inprogress + BT_Road_Completed
        BT_Road_ToBeCommenced = BT_Road_Approved - BT_Road_Taken

        Bus_Stand_SchemeShare = MasterSanctionForm.objects.filter(Scheme__Scheme="KNMT").filter(AgencyType__AgencyType='Town Panchayat').filter(
            Sector="Bus Stand").aggregate(Bus_Stand_SchemeShare=Sum('SchemeShare'))
        Bus_Stand_ULBShare = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').filter(
            Sector='Bus Stand').aggregate(Bus_Stand_ULBShare=Sum('ULBShare'))

        Bus_Stand_Total = Bus_Stand_SchemeShare['Bus_Stand_SchemeShare'] + Bus_Stand_ULBShare['Bus_Stand_ULBShare']
        Bus_Stand_Approved = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').filter(Sector='Bus Stand').count()
        Bus_Stand_Completed = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(ULBType='Town Panchayat').filter(Sector='Bus Stand').filter(
            status='Completed').count()
        Bus_Stand_inprogress = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(ULBType='Town Panchayat').filter(Sector='Bus Stand').filter(
            status='In Progress').count()

        Bus_Stand_Taken = Bus_Stand_inprogress + Bus_Stand_Completed
        Bus_Stand_amountspend = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(ULBType='Town Panchayat').filter(Sector='Bus Stand').aggregate(sum=Sum('valueofworkdone'))
        Bus_Stand_workorder = AgencySanctionModel.objects.filter(Scheme='KNMT').filter(ULBType='Town Panchayat').filter(Sector='Bus Stand').aggregate(
            sum=Sum('work_awarded_amount1'))
        Bus_Stand_TobeCommenced = Bus_Stand_Approved-Bus_Stand_Taken

        CC_Road_SchemeShare = MasterSanctionForm.objects.filter(Scheme__Scheme="KNMT").filter(AgencyType__AgencyType='Town Panchayat').filter(
            Sector="CC Road").aggregate(CC_Road_SchemeShare=Sum('SchemeShare'))
        CC_Road_ULBShare = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').filter(Sector='CC Road').aggregate(
            CC_Road_ULBShare=Sum('ULBShare'))
        CC_Road_Total = CC_Road_SchemeShare['CC_Road_SchemeShare'] + CC_Road_ULBShare['CC_Road_ULBShare']
        CC_Road_Approved = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').filter(Sector='CC Road').count()
        CC_Road_Completed = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(ULBType='Town Panchayat').filter(Sector='CC Road').filter(
            status='Completed').count()
        CC_Road_inprogress = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(ULBType='Town Panchayat').filter(Sector='CC Road').filter(
            status='In Progress').count()
        CC_Road_amountspend = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(ULBType='Town Panchayat').filter(Sector='CC Road').aggregate(
            sum=Sum('valueofworkdone'))
        CC_Road_workorder = AgencySanctionModel.objects.filter(Scheme='KNMT').filter(ULBType='Town Panchayat').filter(Sector='CC Road').aggregate(
            sum=Sum('work_awarded_amount1'))
        CC_Road_Taken = CC_Road_inprogress + CC_Road_Completed
        CC_Road_ToBeCommenced = CC_Road_Approved-CC_Road_Taken
        # Community Hall
        Community_Hall_SchemeShare = MasterSanctionForm.objects.filter(Scheme__Scheme="KNMT").filter(
            Sector="Community Hall").filter(AgencyType__AgencyType='Town Panchayat').aggregate(Community_Hall_SchemeShare=Sum('SchemeShare'))
        Community_Hall_ULBShare = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(
            Sector='Community Hall').filter(AgencyType__AgencyType='Town Panchayat').aggregate(Community_Hall_ULBShare=Sum('ULBShare'))
        Community_Hall_Total = Community_Hall_SchemeShare['Community_Hall_SchemeShare'] + Community_Hall_ULBShare[
                'Community_Hall_ULBShare']
        Community_Hall_Approved = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').filter(
            Sector='Community Hall').count()
        Community_Hall_Completed = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(ULBType='Town Panchayat').filter(
            Sector='Community Hall').filter(status='Completed').count()
        Community_Hall_inprogress = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(ULBType='Town Panchayat').filter(
            Sector='Community Hall').filter(status='In Progress').count()
        Community_Hall_amountspend = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(ULBType='Town Panchayat').filter(Sector='Community Hall').aggregate(
            sum=Sum('valueofworkdone'))
        Community_Hall_workorder = AgencySanctionModel.objects.filter(Scheme='KNMT').filter(ULBType='Town Panchayat').filter(Sector='Community Hall').aggregate(
            sum=Sum('work_awarded_amount1'))
        Community_Hall_Taken = Community_Hall_inprogress + Community_Hall_Completed
        Community_Hall_ToBeCommenced = Community_Hall_Approved-Community_Hall_Taken
        # Crematorium
        Crematorium_SchemeShare = MasterSanctionForm.objects.filter(Scheme__Scheme="KNMT").filter(AgencyType__AgencyType='Town Panchayat').filter(
            Sector="Crematorium").aggregate(Crematorium_SchemeShare=Sum('SchemeShare'))
        Crematorium_ULBShare = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').filter(
            Sector='Crematorium').aggregate(Crematorium_ULBShare=Sum('ULBShare'))
        Crematorium_Total = Crematorium_SchemeShare['Crematorium_SchemeShare'] + Crematorium_ULBShare[
            'Crematorium_ULBShare']
        Crematorium_Approved = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').filter(
            Sector='Crematorium').count()
        Crematorium_Completed = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(ULBType='Town Panchayat').filter(Sector='Crematorium').filter(
            status='Completed').count()
        Crematorium_inprogress = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(ULBType='Town Panchayat').filter(Sector='Crematorium').filter(
            status='In Progress').count()
        Crematorium_amountspend = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(ULBType='Town Panchayat').filter(
            Sector='Crematorium').aggregate(
            sum=Sum('valueofworkdone'))
        Crematorium_workorder = AgencySanctionModel.objects.filter(Scheme='KNMT').filter(ULBType='Town Panchayat').filter(
            Sector='Crematorium').aggregate(
            sum=Sum('work_awarded_amount1'))
        Crematorium_Taken = Crematorium_inprogress + Crematorium_Completed
        Crematorium_ToBeCommenced = Crematorium_Approved - Crematorium_Taken
        #	Culvert
        Culvert_SchemeShare = MasterSanctionForm.objects.filter(Scheme__Scheme="KNMT").filter(AgencyType__AgencyType='Town Panchayat').filter(
            Sector="Culvert").aggregate(Culvert_SchemeShare=Sum('SchemeShare'))
        Culvert_ULBShare = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').filter(Sector='Culvert').aggregate(
            Culvert_ULBShare=Sum('ULBShare'))
        Culvert_Total = Culvert_SchemeShare['Culvert_SchemeShare'] + Culvert_ULBShare['Culvert_ULBShare']
        Culvert_Approved = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').filter(Sector='Culvert').count()
        Culvert_Completed = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(ULBType='Town Panchayat').filter(Sector='Culvert').filter(
            status='Completed').count()
        Culvert_inprogress = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(ULBType='Town Panchayat').filter(Sector='Culvert').filter(
            status='In Progress').count()
        Culvert_amountspend = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(ULBType='Town Panchayat').filter(
            Sector='Culvert').aggregate(
            sum=Sum('valueofworkdone'))
        Culvert_workorder = AgencySanctionModel.objects.filter(Scheme='KNMT').filter(ULBType='Town Panchayat').filter(
            Sector='Culvert').aggregate(
            sum=Sum('work_awarded_amount1'))
        Culvert_Taken = Culvert_inprogress + Culvert_Completed
        Culvert_ToBeCommenced = Culvert_Approved - Culvert_Taken
        # Knowledge Centre
        Knowledge_Centre_SchemeShare = MasterSanctionForm.objects.filter(Scheme__Scheme="KNMT").filter(AgencyType__AgencyType='Town Panchayat').filter(
            Sector="Knowledge Centre").aggregate(Knowledge_Centre_SchemeShare=Sum('SchemeShare'))
        Knowledge_Centre_ULBShare = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').filter(
            Sector='Knowledge Centre').aggregate(Knowledge_Centre_ULBShare=Sum('ULBShare'))
        Knowledge_Centre_Total = Knowledge_Centre_SchemeShare['Knowledge_Centre_SchemeShare'] + \
                                 Knowledge_Centre_ULBShare['Knowledge_Centre_ULBShare']
        Knowledge_Centre_Approved = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').filter(
            Sector='Knowledge Centre').count()
        Knowledge_Centre_Completed = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(ULBType='Town Panchayat').filter(
            Sector='Knowledge Centre').filter(status='Completed').count()
        Knowledge_Centre_inprogress = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(ULBType='Town Panchayat').filter(
            Sector='Knowledge Centre').filter(status='In Progress').count()
        Knowledge_centre_amountspend = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(ULBType='Town Panchayat').filter(
            Sector='Knowledge Centre').aggregate(
            sum=Sum('valueofworkdone'))
        Knowledge_centre_workorder = AgencySanctionModel.objects.filter(Scheme='KNMT').filter(ULBType='Town Panchayat').filter(
            Sector='Knowledge Centre').aggregate(
            sum=Sum('work_awarded_amount1'))
        Knowledge_Centre_Taken = Knowledge_Centre_inprogress + Knowledge_Centre_Completed
        Knowledge_Centre_ToBeCommenced = Knowledge_Centre_Approved-Knowledge_Centre_Taken
        # Market
        Market_SchemeShare = MasterSanctionForm.objects.filter(Scheme__Scheme="KNMT").filter(AgencyType__AgencyType='Town Panchayat').filter(Sector="Market").aggregate(
            Market_SchemeShare=Sum('SchemeShare'))
        Market_ULBShare = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').filter(Sector='Market').aggregate(
            Market_ULBShare=Sum('ULBShare'))
        Market_Total = Market_SchemeShare['Market_SchemeShare'] + Market_ULBShare['Market_ULBShare']
        Market_Approved = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').filter(Sector='Market').count()
        Market_Completed = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(ULBType='Town Panchayat').filter(Sector='Market').filter(
            status='Completed').count()
        Market_inprogress = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(ULBType='Town Panchayat').filter(Sector='Market').filter(
            status='In Progress').count()
        Market_amountspend = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(ULBType='Town Panchayat').filter(
            Sector='Market').aggregate(
            sum=Sum('valueofworkdone'))
        Market_workorder = AgencySanctionModel.objects.filter(Scheme='KNMT').filter(ULBType='Town Panchayat').filter(
            Sector='Market').aggregate(
            sum=Sum('work_awarded_amount1'))
        Market_Taken = Market_inprogress + Market_Completed
        Market_ToBeCommenced = Market_Approved-Market_Taken
        # Metal Beam Crash Barriers
        M_B_C_B_SchemeShare = MasterSanctionForm.objects.filter(Scheme__Scheme="KNMT").filter(AgencyType__AgencyType='Town Panchayat').filter(
            Sector="Metal Beam Crash Barriers").aggregate(M_B_C_B_SchemeShare=Sum('SchemeShare'))
        M_B_C_B_ULBShare = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').filter(
            Sector='Metal Beam Crash Barriers').aggregate(M_B_C_B_ULBShare=Sum('ULBShare'))

        M_B_C_B_Total = M_B_C_B_SchemeShare['M_B_C_B_SchemeShare'] + M_B_C_B_ULBShare['M_B_C_B_ULBShare']
        M_B_C_B_Approved = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').filter(
            Sector='Metal Beam Crash Barriers').count()
        M_B_C_B_Completed = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(ULBType='Town Panchayat').filter(
            Sector='Metal Beam Crash Barriers').filter(status='Completed').count()
        M_B_C_B_inprogress = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(ULBType='Town Panchayat').filter(
            Sector='Metal Beam Crash Barriers').filter(status='In Progress').count()
        MBCB_amountspend = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(ULBType='Town Panchayat').filter(
            Sector='Metal Beam Crash Barriers').aggregate(
            sum=Sum('valueofworkdone'))
        MBCB_workorder = AgencySanctionModel.objects.filter(Scheme='KNMT').filter(ULBType='Town Panchayat').filter(
            Sector='Metal Beam Crash Barriers').aggregate(
            sum=Sum('work_awarded_amount1'))
        M_B_C_B_Taken = M_B_C_B_inprogress + M_B_C_B_Completed
        MBCB_ToBeCommenced = M_B_C_B_Approved-M_B_C_B_Taken

        # Parks
        Parks_SchemeShare = MasterSanctionForm.objects.filter(Scheme__Scheme="KNMT").filter(AgencyType__AgencyType='Town Panchayat').filter(Sector="Parks").aggregate(
            Parks_SchemeShare=Sum('SchemeShare'))
        Parks_ULBShare = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').filter(Sector='Parks').aggregate(
            Parks_ULBShare=Sum('ULBShare'))
        Parks_Total = Parks_SchemeShare['Parks_SchemeShare'] + Parks_ULBShare['Parks_ULBShare']
        Parks_Approved = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').filter(Sector='Parks').count()
        Parks_Completed = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(ULBType='Town Panchayat').filter(Sector='Parks').filter(
            status='Completed').count()
        Parks_inprogress = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(ULBType='Town Panchayat').filter(Sector='Parks').filter(
            status='In Progress').count()
        Parks_amountspend = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(ULBType='Town Panchayat').filter(
            Sector='Parks').aggregate(
            sum=Sum('valueofworkdone'))
        Parks_workorder = AgencySanctionModel.objects.filter(Scheme='KNMT').filter(ULBType='Town Panchayat').filter(
            Sector='Parks').aggregate(
            sum=Sum('work_awarded_amount1'))
        Parks_Taken = Parks_inprogress + Parks_Completed
        Parks_ToBeCommenced = Parks_Approved-Parks_Taken

        # Paver Block
        Paver_Block_SchemeShare = MasterSanctionForm.objects.filter(Scheme__Scheme="KNMT").filter(AgencyType__AgencyType='Town Panchayat').filter(
            Sector="Paver Block").aggregate(Paver_Block_SchemeShare=Sum('SchemeShare'))
        Paver_Block_ULBShare = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').filter(
            Sector='Paver Block').aggregate(Paver_Block_ULBShare=Sum('ULBShare'))
        Paver_Block_Total = Paver_Block_SchemeShare['Paver_Block_SchemeShare'] + Paver_Block_ULBShare[
            'Paver_Block_ULBShare']
        Paver_Block_Approved = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').filter(
            Sector='Paver Block').count()
        Paver_Block_Completed = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(ULBType='Town Panchayat').filter(Sector='Paver Block').filter(
            status='Completed').count()
        Paver_Block_inprogress = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(ULBType='Town Panchayat').filter(Sector='Paver Block').filter(
            status='In Progress').count()
        Paver_Block_amountspend = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(ULBType='Town Panchayat').filter(
            Sector='Paver Block').aggregate(
            sum=Sum('valueofworkdone'))
        Paver_Block_workorder = AgencySanctionModel.objects.filter(Scheme='KNMT').filter(ULBType='Town Panchayat').filter(
            Sector='Paver Block').aggregate(
            sum=Sum('work_awarded_amount1'))
        Paver_Block_Taken = Paver_Block_inprogress + Paver_Block_Completed
        Paver_Block_ToBeCommenced = Paver_Block_Approved-Paver_Block_Taken

        # Retaining wall
        Retaining_wall_SchemeShare = MasterSanctionForm.objects.filter(Scheme__Scheme="KNMT").filter(AgencyType__AgencyType='Town Panchayat').filter(
            Sector="Retaining wall").aggregate(Retaining_wall_SchemeShare=Sum('SchemeShare'))
        Retaining_wall_ULBShare = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').filter(
            Sector='Retaining wall').aggregate(Retaining_wall_ULBShare=Sum('ULBShare'))
        Retaining_wall_Total = Retaining_wall_SchemeShare['Retaining_wall_SchemeShare'] + Retaining_wall_ULBShare[
                'Retaining_wall_ULBShare']
        Retaining_wall_Approved = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').filter(
            Sector='Retaining wall').count()
        Retaining_wall_Completed = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(ULBType='Town Panchayat').filter(
            Sector='Retaining wall').filter(status='Completed').count()
        Retaining_wall_inprogress = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(ULBType='Town Panchayat').filter(
            Sector='Retaining wall').filter(status='In Progress').count()
        Retaining_wall_amountspend = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(ULBType='Town Panchayat').filter(
            Sector='Retaining wall').aggregate(
            sum=Sum('valueofworkdone'))
        Retaining_wall_workorder = AgencySanctionModel.objects.filter(Scheme='KNMT').filter(ULBType='Town Panchayat').filter(
            Sector='Retaining wall').aggregate(
            sum=Sum('work_awarded_amount1'))
        Retaining_wall_Taken = Retaining_wall_inprogress + Retaining_wall_Completed
        Retaining_wall_ToBeCommenced = Retaining_wall_Approved-Retaining_wall_Taken

        # Solid Waste Mgt. SWM
        SWM_SchemeShare = MasterSanctionForm.objects.filter(Scheme__Scheme="KNMT").filter(AgencyType__AgencyType='Town Panchayat').filter(
            Sector="Solid Waste Mgt.").aggregate(SWM_SchemeShare=Sum('SchemeShare'))
        SWM_ULBShare = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').filter(
            Sector='Solid Waste Mgt.').aggregate(SWM_ULBShare=Sum('ULBShare'))

        SWM_Total = SWM_SchemeShare['SWM_SchemeShare'] + SWM_ULBShare['SWM_ULBShare']
        SWM_Approved = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').filter(
            Sector='Solid Waste Mgt.').count()
        SWM_Completed = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(ULBType='Town Panchayat').filter(Sector='Solid Waste Mgt.').filter(
            status='Completed').count()
        SWM_inprogress = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(ULBType='Town Panchayat').filter(Sector='Solid Waste Mgt.').filter(
            status='In Progress').count()
        SWM_amountspend = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(ULBType='Town Panchayat').filter(
            Sector='Solid Waste Mgt.').aggregate(
            sum=Sum('valueofworkdone'))
        SWM_workorder = AgencySanctionModel.objects.filter(Scheme='KNMT').filter(ULBType='Town Panchayat').filter(
            Sector='Solid Waste Mgt.').aggregate(
            sum=Sum('work_awarded_amount1'))
        SWM_Taken = SWM_inprogress + SWM_Completed
        SWM_ToBeCommenced = SWM_Approved-SWM_Taken
        # SWD
        SWD_SchemeShare = MasterSanctionForm.objects.filter(Scheme__Scheme="KNMT").filter(AgencyType__AgencyType='Town Panchayat').filter(Sector="SWD").aggregate(
            SWD_SchemeShare=Sum('SchemeShare'))
        SWD_ULBShare = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').filter(Sector='SWD').aggregate(
            SWD_ULBShare=Sum('ULBShare'))
        SWD_Total = SWD_SchemeShare['SWD_SchemeShare'] + SWD_ULBShare['SWD_ULBShare']
        SWD_Approved = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').filter(Sector='SWD').count()
        SWD_Completed = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(ULBType='Town Panchayat').filter(Sector='SWD').filter(
            status='Completed').count()
        SWD_inprogress = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(ULBType='Town Panchayat').filter(Sector='SWD').filter(
            status='In Progress').count()
        SWD_amountspend = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(ULBType='Town Panchayat').filter(
            Sector='SWD').aggregate(
            sum=Sum('valueofworkdone'))
        SWD_workorder = AgencySanctionModel.objects.filter(Scheme='KNMT').filter(ULBType='Town Panchayat').filter(
            Sector='SWD').aggregate(
            sum=Sum('work_awarded_amount1'))
        SWD_Taken = SWD_inprogress + SWD_Completed
        SWD_ToBeCommenced = SWD_Approved-SWD_Taken

        # Water Bodies
        Water_Bodies_SchemeShare = MasterSanctionForm.objects.filter(Scheme__Scheme="KNMT").filter(AgencyType__AgencyType='Town Panchayat').filter(
            Sector="Water Bodies").aggregate(Water_Bodies_SchemeShare=Sum('SchemeShare'))
        Water_Bodies_ULBShare = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').filter(
            Sector='Water Bodies').aggregate(Water_Bodies_ULBShare=Sum('ULBShare'))
        Water_Bodies_Total = Water_Bodies_SchemeShare['Water_Bodies_SchemeShare'] + Water_Bodies_ULBShare[
            'Water_Bodies_ULBShare']
        Water_Bodies_Approved = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').filter(
            Sector='Water Bodies').count()
        Water_Bodies_Completed = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(ULBType='Town Panchayat').filter(Sector='Water Bodies').filter(
            status='Completed').count()
        Water_Bodies_amountspend = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(ULBType='Town Panchayat').filter(
            Sector='Water Bodies').aggregate(
            sum=Sum('valueofworkdone'))
        Water_Bodies_workorder = AgencySanctionModel.objects.filter(Scheme='KNMT').filter(ULBType='Town Panchayat').filter(
            Sector='Water Bodies').aggregate(
            sum=Sum('work_awarded_amount1'))
        Water_Bodies_inprogress = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(ULBType='Town Panchayat').filter(
            Sector='Water Bodies').filter(status='In Progress').count()
        Water_Bodies_Taken = Water_Bodies_inprogress + Water_Bodies_Completed
        Water_Bodies_ToBeCommenced = Water_Bodies_Approved-Water_Bodies_Taken

        SchemeShare = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(SchemeShare=Sum('SchemeShare'))
        ULBShare = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(ULBShare=Sum('ULBShare'))
        ProjectCost = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').aggregate(
            ProjectCost=Sum('ApprovedProjectCost'))
        work_approved_total = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(AgencyType__AgencyType='Town Panchayat').count()
        work_amountspend = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(ULBType='Town Panchayat').aggregate(
            sum=Sum('valueofworkdone'))
        workorder_total = AgencySanctionModel.objects.filter(Scheme='KNMT').filter(ULBType='Town Panchayat').aggregate(
            sum=Sum('work_awarded_amount1'))
        works_inprogress_total = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(ULBType='Town Panchayat').filter(status='In Progress').count()
        works_completed_total = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(ULBType='Town Panchayat').filter(status='Completed').count()
        works_taken_total = works_inprogress_total + works_completed_total
        works_ToBeCommenced = work_approved_total-works_taken_total
        extra_context = {
            'works_ToBeCommenced':works_ToBeCommenced,
            'Water_Bodies_ToBeCommenced':Water_Bodies_ToBeCommenced,
            'SWD_ToBeCommenced':SWD_ToBeCommenced,
            'SWM_ToBeCommenced':SWM_ToBeCommenced,
            'Retaining_wall_ToBeCommenced':Retaining_wall_ToBeCommenced,
            'Paver_Block_ToBeCommenced':Paver_Block_ToBeCommenced,
            'Parks_ToBeCommenced':Parks_ToBeCommenced,
            'MBCB_ToBeCommenced':MBCB_ToBeCommenced,
            'Market_ToBeCommenced':Market_ToBeCommenced,
            'Knowledge_Centre_ToBeCommenced':Knowledge_Centre_ToBeCommenced,
            'Culvert_ToBeCommenced':Culvert_ToBeCommenced,
            'Crematorium_ToBeCommenced':Crematorium_ToBeCommenced,
            'Community_Hall_ToBeCommenced':Community_Hall_ToBeCommenced,
            'BT_Road_ToBeCommenced':BT_Road_ToBeCommenced,
            'Bus_Stand_TobeCommenced':Bus_Stand_TobeCommenced,
            'CC_Road_ToBeCommenced': CC_Road_ToBeCommenced,
            'work_amountspend':work_amountspend,
            'workorder_total':workorder_total,
            'SWM_workorder':SWM_workorder,
            'SWM_amountspend':SWM_amountspend,
            'Bus_Stand_workorder':Bus_Stand_workorder,
            'Bus_Stand_amountspend':Bus_Stand_amountspend,
            'CC_Road_workorder':CC_Road_workorder,
            'CC_Road_amountspend':CC_Road_amountspend,
            'Community_Hall_workorder':Community_Hall_workorder,
            'Community_Hall_amountspend':Community_Hall_amountspend,
            'Crematorium_amountspend':Crematorium_amountspend,
            'Crematorium_workorder':Crematorium_workorder,
            'Culvert_workorder':Culvert_workorder,
            'Culvert_amountspend':Culvert_amountspend,
            'Knowledge_centre_workorder':Knowledge_centre_workorder,
            'Knowledge_centre_amountspend':Knowledge_centre_amountspend,
            'Market_workorder':Market_workorder,
            'Market_amountspend':Market_amountspend,
            'MBCB_workorder':MBCB_workorder,
            'MBCB_amountspend':MBCB_amountspend,
            'Parks_workorder':Parks_workorder,
            'Parks_amountspend':Parks_amountspend,
            'Paver_Block_workorder':Paver_Block_workorder,
            'Paver_Block_amountspend':Paver_Block_amountspend,
            'Retaining_wall_workorder':Retaining_wall_workorder,
            'Retaining_wall_amountspend':Retaining_wall_amountspend,
            'SWD_workorder':SWD_workorder,
            'SWD_amountspend':SWD_amountspend,
            'Water_Bodies_amountspend':Water_Bodies_amountspend,
            'Water_Bodies_workorder':Water_Bodies_workorder,
            'BT_Road_workorder':BT_Road_workorder,
            'BT_Road_amountspend':BT_Road_amountspend,
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
