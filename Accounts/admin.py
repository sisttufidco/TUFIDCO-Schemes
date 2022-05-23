from re import T
from django.contrib import admin
from .models import *
from ULBForms.models import AgencyBankDetails, AgencyProgressModel
from TUFIDCOapp.models import *
# Register your models here.
import time
from .forms import MonthForm

class ReceiptFormAdmin(admin.ModelAdmin):
    list_display = [
        'Scheme',
        'go_ref',
        'go_date',
        'purpose',
        'amount'
    ]


admin.site.register(ReceiptForm, ReceiptFormAdmin)

@admin.register(ReleaseRequestModel)
class ReleaseRequestAdmin(admin.ModelAdmin):
    change_form_template = 'admin/releaseRequestForm.html'
    list_display = [
        'AgencyName',
        'Scheme',
        'Sector',
        'Project_ID'
    ]
    list_filter= [
        'AgencyType',
        'Scheme',
        'purpose',
    ]
    readonly_fields = [
        'bank_name_ulb',
        'bank_branch_name',
        'bank_branch',
        'account_number',
        'ifsc_code'
    ]
    fieldsets = (
        (None, {
            'fields': (('Scheme', 'AgencyType', 'AgencyName'), ('Sector', 'purpose', 'Project_ID'))
        }),
        (
            'Bank Details', {
                'fields': ('bank_name_ulb',
                           'bank_branch_name',
                           'bank_branch',
                           'account_number',
                           'ifsc_code')
            }
        ),
        (
            'Fund Release Details', {
                'fields': (
                    (
                        'release1Date',
                        'release1Amount',
                    ), (
                        'release2Date',
                        'release2Amount',
                        'sqm_report2',
                    ), (
                        'release3Date',
                        'release3Amount',
                        'sqm_report3',
                    ), (
                        'release4Date',
                        'release4Amount',
                        'sqm_report4',
                    ), (
                        'release5Date',
                        'release5Amount',
                        'sqm_report5'
                    )
                )
            }
        )
    )
    def get_queryset(self, request):
        qs = super(ReleaseRequestAdmin, self).get_queryset(request)
        if not request.user.groups.filter(name__in=["Admin", ]).exists():
            return qs.filter(AgencyName__AgencyName=request.user.first_name)
        return qs
    def save_model(self, request, obj, form, change):
        obj.account_number = AgencyBankDetails.objects.values_list('account_number', flat=True).filter(
            user__first_name=form.cleaned_data['AgencyName'])
        obj.bank_name_ulb = AgencyBankDetails.objects.values_list('beneficiary_name', flat=True).filter(
            user__first_name=form.cleaned_data['AgencyName'])
        obj.bank_branch_name = AgencyBankDetails.objects.values_list('bank_name', flat=True).filter(
            user__first_name=form.cleaned_data['AgencyName'])
        obj.bank_branch = AgencyBankDetails.objects.values_list('branch', flat=True).filter(
            user__first_name=form.cleaned_data['AgencyName'])
        obj.ifsc_code = AgencyBankDetails.objects.values_list('IFSC_code', flat=True).filter(
            user__first_name=form.cleaned_data['AgencyName'])
        obj.save()

    

    def changeform_view(self, request, obj_id, form_url, extra_context=None): 
        
        municipality = MasterSanctionForm.objects.values_list('AgencyName', flat=True).order_by('AgencyName').filter(AgencyType__AgencyType='Municipality')
        townPanchayat = MasterSanctionForm.objects.values_list('AgencyName', flat=True).order_by('AgencyName').filter(AgencyType__AgencyType='Town Panchayat')
        corporation = MasterSanctionForm.objects.values_list('AgencyName', flat=True).order_by('AgencyName').filter(AgencyType__AgencyType='Corporation')
        ULB_Sector = []
        m = list(MasterSanctionForm.objects.values_list('AgencyName', flat=True).all().distinct())
        for i in m:
            sector = list(MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=i).distinct())
            dic = {
                "AgencyName":i,
                "Sector":sector
            }     
            ULB_Sector.append(dic)

        a = MasterSanctionForm.objects.values_list('Project_ID', flat=True).order_by('Project_ID').filter(AgencyType=request.POST.get('AgencyType')).filter(AgencyName=request.POST.get('AgencyName')).filter(Sector=request.POST.get('Sector'))
        project_ids = MasterSanctionForm.objects.values('AgencyName', 'Sector', 'Project_ID').all()
        p = ReleaseRequestModel.objects.filter(id=obj_id)

        extra_context = {
            'p':p,
            'project_ids':project_ids,
            'ULB_Sector':ULB_Sector,
            'corporation': corporation,
            'townPanchayat':townPanchayat,
            'municipality': municipality,

            'achanpudur_project':a,
        }

        return super(ReleaseRequestAdmin, self).changeform_view(request, obj_id, form_url, extra_context=extra_context)



@admin.register(MonthWiseReport)
class MonthWiseReportAdmin(admin.ModelAdmin):
    change_list_template = 'admin/accounts/monthwisereport.html'
  
    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response
        form_month = 0
        m = None
        s = None
        get_month = {
            "--------":0,
            "January":1,
            "February":2,
            "March":3,
            "April":4,
            "May":5,
            "June":6,
            "July":7,
            "August":8,
            "September":9,
            "October":10,
            "November":11,
            "December":12
        }
        get_Scheme = {
            "--------":0,
            "KNMT":1,
            "Singara Chennai 2.0":2,
        }
        if request.method=="POST":
            form = MonthForm(request.POST or None)
            if form.is_valid():
                form_month = get_month[form.cleaned_data['month']]
                m = form.cleaned_data['month']
                s = get_Scheme[form.cleaned_data['Scheme']]
        data1 = ReleaseRequestModel.objects.values('AgencyName__AgencyName', 'Sector', 'Project_ID', 'release1Amount', 'release1Date').filter(release1Date__month=form_month).filter(Scheme=s)
        data2 = ReleaseRequestModel.objects.values('AgencyName__AgencyName', 'Sector', 'Project_ID', 'release2Amount', 'release2Date').filter(release2Date__month=form_month).filter(Scheme=s)
        data3 = ReleaseRequestModel.objects.values('AgencyName__AgencyName', 'Sector', 'Project_ID', 'release3Amount', 'release3Date').filter(release3Date__month=form_month).filter(Scheme=s)
        data4 = ReleaseRequestModel.objects.values('AgencyName__AgencyName', 'Sector', 'Project_ID', 'release4Amount', 'release4Date').filter(release4Date__month=form_month).filter(Scheme=s)
        data5 = ReleaseRequestModel.objects.values('AgencyName__AgencyName', 'Sector', 'Project_ID', 'release5Amount', 'release5Date').filter(release5Date__month=form_month).filter(Scheme=s)
        extra_context = {
            'form_month': m,
            'data1':data1,
            'data2':data2,
            'data3':data3,
            'data4':data4,
            'data5':data5,
            'form': MonthForm
        }
        response.context_data.update(extra_context)
        return response

@admin.register(SectorWiseReport)
class SectorWiseReportAdmin(admin.ModelAdmin):
    change_list_template = 'admin/accounts/sectorwisereport.html'
    list_filter = [
        'Scheme',
        'AgencyType',
        'Sector',
    ]
  
    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response
        
        response.context_data['data1'] = list(qs.values('AgencyName__AgencyName', 'Sector', 'Project_ID', 'release1Amount', 'release1Date').exclude(release1Date=None))
        response.context_data['data2'] = list(qs.values('AgencyName__AgencyName', 'Sector', 'Project_ID', 'release2Amount', 'release2Date').exclude(release2Date=None))
        response.context_data['data3'] = list(qs.values('AgencyName__AgencyName', 'Sector', 'Project_ID', 'release3Amount', 'release3Date').exclude(release3Date=None))
        response.context_data['data4'] = list(qs.values('AgencyName__AgencyName', 'Sector', 'Project_ID', 'release4Amount', 'release4Date').exclude(release4Date=None))
        response.context_data['data5'] = list(qs.values('AgencyName__AgencyName', 'Sector', 'Project_ID', 'release5Amount', 'release5Date').exclude(release5Date=None))
        return response
