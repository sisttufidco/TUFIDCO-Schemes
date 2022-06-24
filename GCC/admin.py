from django.contrib import admin
from TUFIDCOapp.models import *
from GCC.models import *
from ULBForms.models import *
from django.contrib import admin
from django.db.models import Count, Sum,  Func
from import_export.admin import ImportExportModelAdmin
from django.db.models import Q
#from .models import DistrictWiseReport
from .resources import GCCDetailsResource


class GCCDetailsAdmin(ImportExportModelAdmin, admin.AdminSite):
    resource_class = GCCDetailsResource
    exclude = ['user']

    search_fields = [
        'corporation_name',
        'district',
        'region'
    ]
    
    list_display = [
        'corporation_name',
        'district',
        'region',
        'mc',
        'me',
        'email_id1',
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
        qs = super(GCCDetailsAdmin, self).get_queryset(request)
        if not request.user.groups.filter(name__in=["Admin", ]).exists():
            return qs.filter(user=request.user)
        return qs

    def has_add_permission(self, request, *args, **kwargs):
        return not GCCDetails.objects.filter(user=request.user).exists() and not request.user.groups.filter(
            name__in=[
                "Admin", "CMD_DGM"]).exists()
                
admin.site.register(GCCDetails, GCCDetailsAdmin)