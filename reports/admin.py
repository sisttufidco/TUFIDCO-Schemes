from django.contrib import admin
from reports.models import *
from TUFIDCOapp.models import *
from django.db.models import Count, Sum, Avg, Func
from django.db.models import Q


# Register your models here.

@admin.register(ULBProgressIncompleted)
class ULBProgressIncompletedAdmin(admin.ModelAdmin):
    change_list_template = 'admin/ulbprogressincompleted.html'

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
            qs.values('ULBName', 'Project_ID', 'Sector').order_by('ULBName').order_by('Sector').filter(
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
                'Sector'
            ).order_by('ULBName').filter(Scheme='KNMT').filter(
                wd_awarded='0'
            ).filter(work_awarded_amount1=None).filter(work_awarded_amount2=None)
        )
        return response
