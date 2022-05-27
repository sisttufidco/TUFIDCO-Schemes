from django.contrib import admin
from .models import *
from ULBForms.models import AgencyProgressModel, AgencySanctionModel
# Register your models here.

@admin.register(MunicipalityCompletedProjects)
class MunicipalityCompletedProjectsAdmin(admin.ModelAdmin):
    change_list_template = "admin/completedreport.html"

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        response.context_data['report'] = list(
            qs.values('ULBName', 'Sector','Project_ID').order_by('ULBName').filter(Scheme='KNMT').filter(status="Completed").filter(ULBType="Municipality")
        )
        type = "Municipality"
        extra_context = {
            "type": type
        }
        response.context_data.update(extra_context)
        return response

@admin.register(TownPanchayatCompletedProjects)
class TownPanchayatCompletedProjectsAdmin(admin.ModelAdmin):
    change_list_template = "admin/completedreport.html"

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        response.context_data['report'] = list(
            qs.values('ULBName', 'Sector','Project_ID').order_by('ULBName').filter(Scheme='KNMT').filter(status="Completed").filter(ULBType="Town Panchayat")
        )
        type = "Town Panchayat"
        extra_context = {
            "type": type
        }
        response.context_data.update(extra_context)
        return response

@admin.register(MunicipalityInProgressProjects)
class MunicipalityInProgressProjectsAdmin(admin.ModelAdmin):
    change_list_template = "admin/inprogress.html"

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        response.context_data['report'] = list(
            qs.values('ULBName', 'Sector','Project_ID').order_by('ULBName').filter(Scheme='KNMT').filter(status="In Progress").filter(ULBType="Municipality")
        )
        type = "Municipality"
        extra_context = {
            "type": type
        }
        response.context_data.update(extra_context)
        return response

@admin.register(TownPanchayatInProgressProjects)
class TownPanchayatInProgressProjectsAdmin(admin.ModelAdmin):
    change_list_template = "admin/inprogress.html"

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        response.context_data['report'] = list(
            qs.values('ULBName', 'Sector','Project_ID').order_by('ULBName').filter(Scheme='KNMT').filter(status="In Progress").filter(ULBType="Town Panchayat")
        )
        type = "Town Panchayat"
        extra_context = {
            "type": type
        }
        response.context_data.update(extra_context)
        return response

@admin.register(MunicipalityNotCommencedProjects)
class MunicipalityNotCommencedProjectsAdmin(admin.ModelAdmin):
    change_list_template = "admin/reports/not_commenced.html"

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

    
        response.context_data['data'] = list(qs.values('ULBType', 'ULBName', 'Sector', 'Project_ID', 'nc_choices').filter(status="Not Commenced").filter(ULBType="Municipality"))

        type = "Municipality"
        extra_context = {
            "type": type
        }
        response.context_data.update(extra_context)
        return response

@admin.register(TownPanchayatNotCommencedProjects)
class TownPanchayatNotCommencedProjectsAdmin(admin.ModelAdmin):
    change_list_template = "admin/reports/not_commenced.html"

    list_filter = [
        'Scheme',
        'ULBType',
        'nc_choices'
    ]

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response
        response.context_data['data'] = list(qs.values('ULBType', 'ULBName', 'Sector', 'Project_ID', 'nc_choices').filter(status="Not Commenced").filter(ULBType="Town Panchayat"))
        type = "Town Panchayat"
        extra_context = {
            "type": type
        }
        response.context_data.update(extra_context)
        return response
