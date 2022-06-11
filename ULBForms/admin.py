import functools
from django.contrib import admin
from .models import *
from .forms import *
from import_export.admin import ImportExportModelAdmin
from .resources import *


# Register your models here.
@admin.register(ProjectDetails)
class ProjectDetailsAdmin(admin.ModelAdmin):
    change_list_template = 'admin/projectDetailsReport.html'

    list_filter = [
        'Sector'
    ]

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        response.context_data['report'] = list(
            qs.values('Sector', 'Project_ID', 'ProjectName', 'ApprovedProjectCost').order_by('Sector').filter(
                Scheme__Scheme='Singara Chennai 2.0'))
        return response


class AgencyBankDetailsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = AgencyBankDetailsResources
    change_form_template = 'admin/bankdetails.html'
    exclude = ['user', 'date_and_time', 'ULBType']
    readonly_fields = ['passbook_preview']
    list_display = [
        'user',
        'beneficiary_name',
        'bank_name',
        'branch',
        'account_number',
        'IFSC_code',
        'date_and_time'
    ]
    ordering = [
        'user__first_name',
    ]
    list_filter = [
        'ULBType',
    ]
    search_fields = [
        'user__first_name',
        'beneficiary_name',
        'bank_name',
        'branch',
    ]

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.date_and_time = datetime.now()
        if request.user.groups.filter(name__in=["Municipality", ]).exists():
            obj.ULBType = "Municipality"
        if request.user.groups.filter(name__in=["Town Panchayat", ]).exists():
            obj.ULBType = "Town Panchayat"
        if request.user.groups.filter(name__in=["Corporation", ]).exists():
            obj.ULBType = "Corporation"
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


class ULBPANDetailsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = ULBPanCardResources
    change_form_template = 'admin/ULBpandetails.html'
    exclude = ['user', 'date_and_time', 'ULBType']
    readonly_fields = ['pan_preview']
    list_filter = [
        'ULBType',
    ]
    list_display = [
        'user',
        'PANno',
        'name',
        'date_and_time'
    ]
    search_fields = [
        'user__first_name',
        'name',
    ]
    ordering = [
        'date_and_time',
    ]

    def save_model(self, request, obj, form, change):
        if request.user.groups.filter(name__in=['Agency',]).exists():
            obj.user = request.user
        obj.date_and_time = datetime.now()
        if request.user.groups.filter(name__in=["Municipality", ]).exists():
            obj.ULBType = "Municipality"
        if request.user.groups.filter(name__in=["Town Panchayat", ]).exists():
            obj.ULBType = "Town Panchayat"
        if request.user.groups.filter(name__in=["Corporation", ]).exists():
            obj.ULBType = "Corporation"
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


def Decimal(x):
    return float(x)


class AgencyProgressAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = AgencyProgressResource
    change_form_template = 'admin/ulbprogress.html'
    form = AgencyProgressForm
    fields = (('ApprovedProjectCost', 'SchemeShare', 'ULBShare'), ('total_release'),('Scheme', 'Sector', 'Project_ID'), 'ProjectName', ('Latitude', 'Longitude'), 'location',
              'PhysicalProgress', 'status','nc_choices', 'nc_status', 'upload1',  'valueofworkdone','FundRelease','Expenditure', 'upload2')
    readonly_fields = ('ApprovedProjectCost', 'SchemeShare', 'ULBShare', 'total_release','ProjectName')
    list_filter = [
        'ULBType',
        'status',
        'Scheme',
        'Sector',

    ]
    list_display = [
        'Project_ID',
        'Sector',
        'ProjectName',
        'ULBName',
        'District',
        'ApprovedProjectCost',
        'status',
        'percentageofworkdone',
        'date_and_time',

    ]

    search_fields = [
        'Scheme',
        'ULBName',
        'ProjectName',
        'Project_ID',
        'Sector',
    ]

    def save_model(self, request, obj, form, change):
        if request.user.groups.filter(name__in=['Agency']).exists():
            obj.user = request.user
            obj.ProjectName = MasterSanctionForm.objects.values_list('ProjectName', flat=True).filter(
                Project_ID=form.cleaned_data['Project_ID'])
            obj.save()

    def get_queryset(self, request):
        qs = super(AgencyProgressAdmin, self).get_queryset(request)
        if not request.user.groups.filter(name__in=["Admin", "progressdetails"]).exists():
            return qs.filter(user=request.user)
        return qs

    def get_form(self, request, obj=None, **kwargs):
        Form = super().get_form(request, obj=None, **kwargs)
        return functools.partial(Form, request)

    


admin.site.register(AgencyProgressModel, AgencyProgressAdmin)


class AgencySanctionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = AgencySanctionResource
    form = AgencySanctionForm
    search_fields = [
        'Scheme',
        'Project_ID',
        'ProjectName',
        'user__first_name',
        'Sector'
    ]

    fields = (('ApprovedProjectCost', 'SchemeShare', 'ULBShare'),
        ('Scheme', 'Sector', 'Project_ID'), 'ProjectName', 'ts_awarded', 'tsrefno', 'tsdate', 'tr_awarded', 'tawddate',
        'wd_awarded', 'wdawddate', 'work_awarded_amount2', 'work_awarded_amount1')
    readonly_fields = ('ApprovedProjectCost', 'SchemeShare', 'ULBShare', 'ProjectName')
    list_display = [
        'Project_ID',
        'Sector',
        'ProjectName',
        'ULBName',
        'date_and_time'
    ]

    list_filter = [
        'ULBType',
        'Scheme',
        'Sector',
        'ts_awarded',
        'tr_awarded',
        'wd_awarded',
    ]

    def save_model(self, request, obj, form, change):
        if request.user.groups.filter(name__in=['Agency']).exists():
            obj.user = request.user
            obj.ProjectName = MasterSanctionForm.objects.values_list('ProjectName', flat=True).filter(
                Project_ID=form.cleaned_data['Project_ID'])
            obj.save()

    def get_queryset(self, request):
        qs = super(AgencySanctionAdmin, self).get_queryset(request)
        if not request.user.groups.filter(name__in=["Admin", ]).exists():
            return qs.filter(user=request.user)
        return qs

    def get_form(self, request, obj=None, **kwargs):
        formset = super().get_form(request, obj, **kwargs)
        return functools.partial(formset, request)


admin.site.register(AgencySanctionModel, AgencySanctionAdmin)

