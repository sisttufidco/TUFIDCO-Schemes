from django.contrib import admin
from .models import *
from ULBForms.models import AgencyBankDetails, AgencyProgressModel, AgencySanctionModel
from TUFIDCOapp.models import *
from TUFIDCO.settings import EMAIL_HOST_USER
from django.core.mail import EmailMessage
from .forms import MonthForm, DMASector, CTPSector
from CTP.models import TownPanchayatDetails
from DMA.models import MunicipalityDetails
from django.db.models import Sum

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
        'ifsc_code',
        'ApprovedProjectCost',
        'SchemeShare',
        'ULBShare'
    ]
    search_fields = [
        'AgencyName__AgencyName',
        'Project_ID',
        'Sector',

    ]
    fieldsets = (
        (None, {
            'fields': (('ApprovedProjectCost', 'SchemeShare', 'ULBShare'),('Scheme', 'AgencyType', 'AgencyName'), ('Sector', 'purpose', 'Project_ID'))
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
        if (form.cleaned_data['purpose'] == 'Project'):
            obj.ApprovedProjectCost = MasterSanctionForm.objects.values_list('ApprovedProjectCost', flat=True).filter(Project_ID = form.cleaned_data['Project_ID'])
            obj.SchemeShare = MasterSanctionForm.objects.values_list('SchemeShare', flat=True).filter(Project_ID = form.cleaned_data['Project_ID'])
            obj.ULBShare = MasterSanctionForm.objects.values_list('ULBShare', flat=True).filter(Project_ID = form.cleaned_data['Project_ID'])
        flag = 0
        amount = ""
        if (form.cleaned_data['purpose'] == 'Project') and (form.cleaned_data['release1Amount'] is not None) and (form.cleaned_data['release2Amount'] is None) and (form.cleaned_data['release3Amount'] is None) and (form.cleaned_data['release4Amount'] is None) and (form.cleaned_data['release5Amount'] is None): 
            amount += str(form.cleaned_data['release1Amount'])
            flag=1
        if (form.cleaned_data['purpose'] == 'Project') and (form.cleaned_data['release2Amount'] is not None) and (form.cleaned_data['release3Amount'] is None) and (form.cleaned_data['release4Amount'] is None) and (form.cleaned_data['release5Amount'] is None): 
            amount += str(form.cleaned_data['release2Amount'])
            flag=1
        if (form.cleaned_data['purpose'] == 'Project') and  (form.cleaned_data['release3Amount'] is not None) and (form.cleaned_data['release4Amount'] is None) and (form.cleaned_data['release5Amount'] is None): 
            amount += str(form.cleaned_data['release3Amount'])
            flag=1
        if (form.cleaned_data['purpose'] == 'Project') and  (form.cleaned_data['release4Amount'] is not None) and (form.cleaned_data['release5Amount'] is None): 
            amount += str(form.cleaned_data['release4Amount'])
            flag=1
        if (form.cleaned_data['purpose'] == 'Project')  and (form.cleaned_data['release5Amount'] is not None): 
            amount += str(form.cleaned_data['release5Amount'])
            flag=1
        if flag==1:
            district = MasterSanctionForm.objects.values_list('District__District', flat=True).filter(Project_ID = form.cleaned_data['Project_ID'])[0]
            subject = str(form.cleaned_data['Scheme'])+" - "+str(form.cleaned_data['Sector'])+" - "+str(form.cleaned_data['Project_ID']) + " - Release of Funds"
            message = """
                    To<br>The Commissioner / Executive officer,<br>
                    %s %s<br>
                    %s District<br>
                    <br><br>
                    Sir/Madam
                    <br><br>
                    We would like to inform you that an amount of Rs %s lakhs released to %s Sector, %s Project ID.
                    <br><br>
                    Please check the web page progress portal through your login and Bank account.
                    <br><br>
                    Please make necessary entries in your Progress portal and send stamped receipt.
                    <br><br>
                    Thanking you,<br>
                    For TUFIDCO
                    <br>
                    <br>
                    SD/-<br>
                    For ACS / CMD
                """%(form.cleaned_data['AgencyName'], form.cleaned_data['AgencyType'], district, amount, form.cleaned_data['Sector'], form.cleaned_data['Project_ID'])
            email = []  
           
            try:
                if str(form.cleaned_data['AgencyType']) == "Municipality":
                    email_detail = MunicipalityDetails.objects.values_list('email_id1', flat=True).filter(user__first_name=form.cleaned_data['AgencyName'])[0]
                    email.append(email_detail)
          
                if str(form.cleaned_data['AgencyType']) == "Town Panchayat":
                    email_detail = TownPanchayatDetails.objects.values_list('email', flat=True).filter(user__first_name=form.cleaned_data['AgencyName'])[0]
                    email.append(email_detail)
            except IndexError:
                subject=str(form.cleaned_data['AgencyType'])+" Details Not Filled - "+str(form.cleaned_data['AgencyName'])
                message = """
                        Hello,<br><br>
                        %s %s, %s District did not filled %s details.<br>
                        <br>
                        Please ask them to do so.<br><br>
                        Thank You.
                        """%(form.cleaned_data['AgencyName'], form.cleaned_data['AgencyType'], district, form.cleaned_data['AgencyType'])
                email.append('tufidcoschemes@gmail.com')    
            mail = EmailMessage(subject, message, str(EMAIL_HOST_USER), email)  
            mail.content_subtype = "html"
            mail.send()      
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

@admin.register(DMAinstallmentReport)
class DMAinstallmentReportAdmin(admin.ModelAdmin):
    change_list_template="admin/accounts/release_installment_report.html"
    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response
        town = "Municipality"
        form_sector = None
        sec = list(AgencyProgressModel.objects.values_list('Sector', flat=True).filter(ULBType="Municipality").filter(status="In Progress").distinct())
        if request.method=="POST":
            form = DMASector(request.POST or None)
            if form.is_valid():
                form_sector = form.cleaned_data['sector']
                
        Project_ID_progress = list(AgencyProgressModel.objects.values_list('Project_ID', flat=True).order_by('ULBName').filter(Sector=form_sector).filter(ULBType="Municipality"))
        final_list = []
        for project_id in Project_ID_progress:
            Sector = AgencyProgressModel.objects.values_list('Sector', flat=True).filter(Project_ID=project_id)[0]
            ULBName = AgencyProgressModel.objects.values_list('ULBName', flat=True).filter(Project_ID=project_id)[0]
            ApprovedProjectCost = MasterSanctionForm.objects.values_list('ApprovedProjectCost', flat=True).filter(Project_ID=project_id)[0]
            KNMTShare = MasterSanctionForm.objects.values_list('SchemeShare', flat=True).filter(Project_ID=project_id)[0]
            try:
                WO_amount = AgencySanctionModel.objects.values_list('work_awarded_amount1', flat=True).filter(Project_ID=project_id)[0]
            except IndexError:
                WO_amount = 0.00
            VO_WD = AgencyProgressModel.objects.values_list('valueofworkdone', flat=True).filter(Project_ID=project_id)[0]
            eligible_amount = KNMTShare/2
            status = AgencyProgressModel.objects.values_list('status', flat=True).filter(Project_ID=project_id)[0]
            dic = {
                "Sector":Sector,
                "ULBName": ULBName,
                "project_id": project_id,
                "ApprovedProjectCost": str(ApprovedProjectCost),
                "KNMTShare": str(KNMTShare),
                "WO_amount": str(WO_amount),
                "VO_WD": str(VO_WD),
                "eligible_amount": str(eligible_amount),
                "status":status,
            }
            final_list.append(dic)
        OverallSchemeshare = MasterSanctionForm.objects.filter(Scheme__Scheme="KNMT").filter(Sector=form_sector).filter(AgencyType__AgencyType='Municipality').aggregate(SchemeShare=Sum('SchemeShare'))
        OverallApprovedProjectCost = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector=form_sector).filter(AgencyType__AgencyType='Municipality').aggregate(ULBShare=Sum('ApprovedProjectCost'))
        OverallWO_amount = AgencySanctionModel.objects.filter(Scheme='KNMT').filter(ULBType='Municipality').filter(Sector=form_sector).aggregate(sum=Sum('work_awarded_amount1'))
        OverallVO_WD = AgencyProgressModel.objects.filter(Scheme="KNMT").filter(ULBType='Municipality').filter(Sector=form_sector).aggregate(sum=Sum('valueofworkdone'))
        Overalleligible_amount=None
        try:
            Overalleligible_amount = OverallSchemeshare['SchemeShare']/2
        except TypeError:
            pass
        
        extra_context = {
            "DMASector":DMASector,
            "sec":sec,
            'town':town,
            'final_list':final_list,
            "OverallSchemeshare":OverallSchemeshare,
            "OverallApprovedProjectCost":OverallApprovedProjectCost,
            "OverallWO_amount":OverallWO_amount,
            "OverallVO_WD":OverallVO_WD,
            "Overalleligible_amount":Overalleligible_amount,
        }
        response.context_data.update(extra_context)
        return response

@admin.register(CTPinstallmentReport)
class CTPinstallmentReportAdmin(admin.ModelAdmin):
    change_list_template="admin/accounts/release_installment_report.html"
    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response
        town = "Town Panchayat"
        form_sector = None
        sec = list(AgencyProgressModel.objects.values_list('Sector', flat=True).filter(ULBType="Town Panchayat").filter(status="In Progress").distinct())
        if request.method=="POST":
            form = CTPSector(request.POST or None)
            if form.is_valid():
                form_sector = form.cleaned_data['sector']
                
        Project_ID_progress = list(AgencyProgressModel.objects.values_list('Project_ID', flat=True).order_by('ULBName').filter(Sector=form_sector).filter(ULBType="Town Panchayat"))
        final_list = []
        for project_id in Project_ID_progress:
            Sector = AgencyProgressModel.objects.values_list('Sector', flat=True).filter(Project_ID=project_id)[0]
            ULBName = AgencyProgressModel.objects.values_list('ULBName', flat=True).filter(Project_ID=project_id)[0]
            ApprovedProjectCost = MasterSanctionForm.objects.values_list('ApprovedProjectCost', flat=True).filter(Project_ID=project_id)[0]
            KNMTShare = MasterSanctionForm.objects.values_list('SchemeShare', flat=True).filter(Project_ID=project_id)[0]
            try:
                WO_amount = AgencySanctionModel.objects.values_list('work_awarded_amount1', flat=True).filter(Project_ID=project_id)[0]
            except IndexError:
                WO_amount = 0.00
            VO_WD = AgencyProgressModel.objects.values_list('valueofworkdone', flat=True).filter(Project_ID=project_id)[0]
            eligible_amount = KNMTShare/2
            status = AgencyProgressModel.objects.values_list('status', flat=True).filter(Project_ID=project_id)[0]
            dic = {
                "Sector":Sector,
                "ULBName": ULBName,
                "project_id": project_id,
                "ApprovedProjectCost": str(ApprovedProjectCost),
                "KNMTShare": str(KNMTShare),
                "WO_amount": str(WO_amount),
                "VO_WD": str(VO_WD),
                "eligible_amount": str(eligible_amount),
                "status":status,
            }
            final_list.append(dic)
        OverallSchemeshare = MasterSanctionForm.objects.filter(Scheme__Scheme="KNMT").filter(Sector=form_sector).filter(AgencyType__AgencyType='Town Panchayat').aggregate(SchemeShare=Sum('SchemeShare'))
        OverallApprovedProjectCost = MasterSanctionForm.objects.filter(Scheme__Scheme='KNMT').filter(Sector=form_sector).filter(AgencyType__AgencyType='Town Panchayat').aggregate(ULBShare=Sum('ApprovedProjectCost'))
        OverallWO_amount = AgencySanctionModel.objects.filter(Scheme='KNMT').filter(ULBType='Town Panchayat').filter(Sector=form_sector).aggregate(sum=Sum('work_awarded_amount1'))
        OverallVO_WD = AgencyProgressModel.objects.filter(Scheme="KNMT").filter(ULBType='Town Panchayat').filter(Sector=form_sector).aggregate(sum=Sum('valueofworkdone'))
        Overalleligible_amount=None
        try:
            Overalleligible_amount = OverallSchemeshare['SchemeShare']/2
        except TypeError:
            pass
        
        extra_context = {
            "DMASector":CTPSector,
            "sec":sec,
            'town':town,
            'final_list':final_list,
            "OverallSchemeshare":OverallSchemeshare,
            "OverallApprovedProjectCost":OverallApprovedProjectCost,
            "OverallWO_amount":OverallWO_amount,
            "OverallVO_WD":OverallVO_WD,
            "Overalleligible_amount":Overalleligible_amount,
        }
        response.context_data.update(extra_context)
        return response