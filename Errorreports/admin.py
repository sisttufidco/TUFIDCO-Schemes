from django.contrib import admin
from .models import *
from TUFIDCOapp.models import *
from django.db.models import Q

# Register your models here.

@admin.register(ULBProgressIncompleted)
class ULBProgressIncompletedAdmin(admin.ModelAdmin):
    change_list_template = 'admin/ulbprogressincompleted.html'

    list_filter = [
        'ULBType',
        'Sector',
    ]

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        response.context_data['report'] = list(
            qs.values('ULBName', 'Project_ID', 'Sector', 'ULBType').order_by('ULBName').order_by('Sector').filter(
                Scheme='KNMT').filter(status='In Progress').filter(valueofworkdone=0.0))
        return response


@admin.register(ULBSanctionReportError)
class ULBSanctionReportErrorAdmin(admin.ModelAdmin):
    change_list_template = 'admin/ulbSanctionReportError.html'

    list_filter = [
        'ULBType',
        'Sector'
    ]

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        response.context_data['report'] = list(
            qs.values(
                'ULBName',
                'Project_ID',
                'Sector',
                'ULBType'
            ).order_by('ULBName').filter(Scheme='KNMT').filter(
                wd_awarded='0'
            ).filter(work_awarded_amount1=None).filter(work_awarded_amount2=None)
        )
        return response

@admin.register(ProgressNotEntered)
class ProgressNotEnteredAdmin(admin.ModelAdmin):
    change_list_template = 'admin/progressnotentered.html'
    list_filter = [
        'AgencyType',
        'Sector'
    ]

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)

        agencyProgresslist = list(AgencyProgressModel.objects.values_list('Project_ID', flat=True).all())

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        response.context_data['report'] = list(
            qs.values(
                'AgencyName__AgencyName',
                'Project_ID',
                'Sector',
                'AgencyType__AgencyType'
            ).order_by('AgencyName__AgencyName').exclude(Sector='Solid Waste Mgt.').filter(
                ~Q(Project_ID__in=agencyProgresslist)).filter(Scheme__Scheme='KNMT')
        )
        return response

@admin.register(SanctionNotEntered)
class ProgressNotEnteredAdmin(admin.ModelAdmin):
    list_filter = [
        'AgencyType',
        'Sector'
    ]

    change_list_template = 'admin/sanctionnotentereddetails.html'

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)

        agencySanctionlist = list(AgencySanctionModel.objects.values_list('Project_ID', flat=True).all())

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        response.context_data['report'] = list(
            qs.values(
                'AgencyName__AgencyName',
                'Project_ID',
                'Sector',
                'AgencyType__AgencyType'
            ).order_by('AgencyName__AgencyName').exclude(Sector='Solid Waste Mgt.').filter(AgencyType__AgencyType='Town Panchayat').filter(
                ~Q(Project_ID__in=agencySanctionlist)).filter(Scheme__Scheme='KNMT')
        )
        return response