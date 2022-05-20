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
        abiramam_sector = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2).distinct()
        achanpudur_sector = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=3).distinct()
        Acharapakkam_sector = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1568).distinct()
        Adigaratty_sector = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1569).distinct()
        Adirampattinam_sector = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2221).distinct()
        Aduthurai_sector = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1570).distinct()
        Agaram_sector = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1571).distinct()
        Agasteeswaram_sector = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1572).distinct()
        Alagappapuram_sector = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1573).distinct()
        Alampalayam_sector = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1574).distinct()
        Alandurai_sector = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2204).distinct()
        Alanganallur_sector = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1575).distinct()
        Alangayam_sector = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1576).distinct()
        Alangudi_sector = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1577).distinct()
        Alangulam_sector = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1578).distinct()
        Aloor_sector = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1579).distinct()
        Alwarkurichi_sector = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1580).distinct()
        Alwarthirunagari_sector = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1581).distinct()
        Ambasamudram_sector = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2118).distinct()
        Ambur_sector = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1582).distinct()
        Ammapettai_sector = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1583).distinct()
        Ammayanaickanur_sector = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1584).distinct()
        Ammoor_sector = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1585).distinct()
        Anaimalai_sector = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1586).distinct()
        Anakaputhur_sector = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2065).distinct()
        Ananthapuram_sector = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1587).distinct()
        Andipatti_sector = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1588).distinct()
        Anjugramam_sector =  MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1589).distinct()
        Annavasal_sector = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1590).distinct()
        Annur_sector = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1591).distinct()
        Anthiyur_sector = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1592).distinct()
        Appakudal_sector = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1593).distinct()
        Arachalur_sector = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1594).distinct()
        Arakandanallur_sector = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1595).distinct()
        Arakkonam_sector = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2145).distinct()
        Aralvaimozhi_sector = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1596).distinct()
        Arani_sector = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1598).distinct()
        Aranthangi_sector = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2154).distinct()

        Aravakurichi_sector = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1599).distinct()
        Arcot_sector = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2122).distinct()
        Arimalam_sector = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1600).distinct()
        Ariyalur_sector = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2063).distinct()
        Ariyappampalayam_sector = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1601).distinct()
        Arumanai_sector = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1602).distinct()
        Arumbavur_sector = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1603).distinct()
        Arumuganeri_sector = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1604).distinct()
        Aruppukottai_sector = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2152).distinct()
        Athani_sector = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1605).distinct()
        Athanur_sector = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1606).distinct()
        Athur_sector = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1607).distinct()
        
        Attayampatty_sector = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1608).distinct()
        Attoor_sector = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1609).distinct()
        Attur_sector = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2123).distinct()
        Aundipatti_sector = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1610).distinct()
        Auralvaimozhi_sector = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2246).distinct()
        Authoor_sector = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1611).distinct()
        A_Vallalapatti = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1612).distinct()
        Avalpoondurai = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1613).distinct()
        Avinashi = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1614).distinct()
        Ayakudi = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2180).distinct()
        Ayikudy = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1616).distinct()
        Ayothiyapattanam = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1617).distinct()
        Ayyalur = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1618).distinct()
        Ayyampalayam = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1619).distinct()
        Ayyampettai = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1620).distinct()
        Ayyothiyapattanam = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1621).distinct()
        Azhagappapuram = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1622).distinct()
        Azhakiapandiyapuram = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1624).distinct()

        Balakrishnampatti = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1625).distinct()
        Balasamudram = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2229).distinct()
        Bargur = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1626).distinct()
        Batlagundu = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2230).distinct()
        Belur = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1627).distinct()
        Bhavani = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2081).distinct()
        Bhavanisagar = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1628).distinct()
        Bhuvanagiri = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1630).distinct()
        Bikkatti = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1620).distinct()
        B_Mallapuram = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1631).distinct()
        Bodinayakanur = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2149).distinct()
        Boothapandy = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1632).distinct()
        Boothipuram = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1633).distinct()

        Chengalpattu = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2066).distinct()
        Chengam = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1634).distinct()
        Chennasamudram = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1635).distinct()
        Chennimalai = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1636).distinct()
        Cheranmahadevi = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1637).distinct()
        Chetpet = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1638).distinct()
        Chettipalayam = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1639).distinct()
        Chettiyarpatti = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1640).distinct()
        Chidambaram = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2128).distinct()
        Chinnalapatti = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1641).distinct()
        Chinnamanur = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2150).distinct()
        Chithode = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1642).distinct()
        Coimbatore = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1643).distinct()
        Colachel = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2087).distinct()
        Coonoor = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2254).distinct()
        Courtallam = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1644).distinct()
        C_Pudupatti = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1645).distinct()
        Cuddalore = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2073).distinct()
        Cumbum = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2151).distinct()
        
        Denkanikottai = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1647).distinct()
        Desur = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1648).distinct()
        Devakottai = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2120).distinct()
        Devarshola = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2254).distinct()
        Devathanapatti = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1649).distinct()
        Devershola = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1650).distinct()
        Dhaliyur = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1651).distinct()
        Dharapuram = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2141).distinct()
        Dharmapuri = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2077).distinct()
        Dindigul = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2217).distinct()

        Edaicode = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1652).distinct()
        Edaikazhinadu = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1653).distinct()
        Elampillai = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1654).distinct()
        Elathur = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1655).distinct()
        Elumalai = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1656).distinct()
        Eral = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1657).distinct()
        Eraniel = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1658).distinct()
        Eriodu = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1659).distinct()
        Erode = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2211).distinct()
        Erumaipatti = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2196).distinct()
        Erumapatty = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1660).distinct()
        Eruvadi = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1661).distinct()
        Ettayapuram = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1662).distinct()
        Ettimadai = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1663).distinct()

        Ganapathipuram = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1664).distinct()
        Gangavalli = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1665).distinct()
        Genguvarpatti = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1667).distinct()
        Gingee = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1668).distinct()
        Gobichettipalayam = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2253).distinct()
        Gopalasamudram = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1669).distinct()
        Greater_Chennai = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2181).distinct()
        Gudalur = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2205).distinct()
        Gudalur_N = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2255).distinct()
        Gudiyatham = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2138).distinct()
        Gummidipoondi = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1671).distinct()

        Hanumanthampatti= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1672).distinct()
        Harur= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1673).distinct()
        Hulical= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1674).distinct()
        Idappadi= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2121).distinct()
        Idigarai= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1675).distinct()
        Ilanji= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1676).distinct()
        Ilayankudi= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1677).distinct()
        Illuppur= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1678).distinct()
        Irugur= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1680).distinct()
        Jalagandapuram= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1681).distinct()
        Jalakandapuram= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2191).distinct()
        Jambai= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1682).distinct()
        Jayankondam= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2064).distinct()
        Jegathala= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1683).distinct()
        Jolarpet = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2162).distinct()

        Kadambur = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1684).distinct()
        Kadathur = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1685).distinct()
        Kadayal = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1686).distinct()
        Kadayampatty = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1687).distinct()
        Kadayanallur = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2132).distinct()
        Kalakkad = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2237).distinct()
        Kalambur = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1688).distinct()
        Kalappanacikenpatty = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1689).distinct()
        Kalavai = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2188).distinct()
        Kaliyakkavilai = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1690).distinct()
        Kallakudi = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1691).distinct()
        Kallakurichi= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2085).distinct()
        Kallidaikurichi= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1692).distinct()
        Kallukuttam = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1695).distinct()
        Kalugumalai = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1696).distinct()
        
        Kamayagoundanpatti = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1697).distinct()
        Kambainallur = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1698).distinct()
        Kamuthi = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1699).distinct()
        Kanadukathan  = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1700).distinct()
        Kanam = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1701).distinct()
        Kancheepuram  = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2169).distinct()
        Kandanur  = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1702).distinct()
        Kangeyam = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2173).distinct()
        Kanjikoil  = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1703).distinct()
        Kannamangalam = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1704).distinct()
        Kannampalayam= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1705).distinct()
        Kannankurichi = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1706).distinct()
        Kannivadi = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1707).distinct()
        Kanniyakumari= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1708).distinct()
        Kappiyarai  = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1709).distinct()
        
        Karaikudi= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2164).distinct()
        Karambakkudi = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2227).distinct()
        Karambakudi = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1711).distinct()
        Karimangalam= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1712).distinct()
        Kariyapatti  = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1713).distinct()
        Karumandichellipalayam= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1714).distinct()
        Karumathampatti = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2206).distinct()
        Karungal = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1715).distinct()
        Karunguzhi= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1716).distinct()
        Karuppur  = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1717).distinct()
        Karupur = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2192).distinct()
        Karur = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2090).distinct()
        Kasipalayam_G = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1718).distinct()
        Kattumannarkoil = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1719).distinct()
        Kattuputhur  = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1721).distinct()
        
        Kaveripattinam= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1722).distinct()
        Kayalpattinam = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2259).distinct()
        Kayathar= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1723).distinct()
        Keelakarai = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2163).distinct()
        Keelapavoor = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1724).distinct()
        Keelvelur = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1730).distinct()
        Keeramangalam  = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1726).distinct()
        Keeramangkalam = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2228).distinct()
        Keeranur = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1727).distinct()
        Keeripatty = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1728).distinct()
        Keezhkulam = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1729).distinct()
        Kelamangalam= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1731).distinct()
        Kempanaickenpalayam  = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1733).distinct()
        Ketti = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1734).distinct()
        Kilambadi = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1735).distinct()
        
        Kilkundah = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1736).distinct()
        Killai = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1737).distinct()
        Killiyoor= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1738).distinct()
        Kilpennathur = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1739).distinct()
        Kinathukadavu = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2207).distinct()
        Kodaikanal  = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2078).distinct()
        Kodavasal= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1740).distinct()
        Kodumudi  = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1741).distinct()
        Kolappalur = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2199).distinct()
        Kolathupalayam  = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1742).distinct()
        Kolathur= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1743).distinct()
        Kollankoil = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1744).distinct()
        Kollemcode = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2245).distinct()
        Komarapalayam = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2099).distinct()
        Kombai= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1745).distinct()
        
        Konganapuram  = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2190).distinct()
        Koothanallur = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2161).distinct()
        Koothappar= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1747).distinct()
        Koradachery  = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1748).distinct()
        Kotagiri  = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1749).distinct()
        Kothanalloor= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1750).distinct()
        Kottaiyur  = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1751).distinct()
        Kottaram  = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1752).distinct()
        Kottur= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1753).distinct()
        Kovilpatti = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2269).distinct()
        Krishnagiri  = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2092).distinct()
        Krishnarayapuram = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1754).distinct()
        Kuchanur = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2233).distinct()
        Kuhalur  = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1755).distinct()
        Kulasekaram = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1756).distinct()
        
        Kulithalai = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2091).distinct()
        Kumarapuram = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1757).distinct()
        Kumbakonam= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2137).distinct()
        Kunnathur= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1758).distinct()
        Kurinjipadi= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1759).distinct()
        Kurumbalur= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1760).distinct()
        Kutchanur= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1761).distinct()
        Kuthalam = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1762).distinct()
        Kuzhithurai = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2088).distinct()

        Labbaikudikadu= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1763).distinct()
        Lakkampatti= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2200).distinct()
        Lalgudi= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2225).distinct()
        Lalpettai= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1764).distinct()

        Madhuranthagam= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2067).distinct()
        Madukkarai= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2208).distinct()
        Madukkur= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1765).distinct()
        Mallanginar= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1766).distinct()
        Mallasamudram= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1767).distinct()
        Mallur= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1768).distinct()
        Mamallapuram= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1769).distinct()
        Mamsapuram= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1771).distinct()
        Manalmedu= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1772).distinct()
        Manalurpet= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1773).distinct()
        Manamadurai= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2235).distinct()
        Manaparai= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2265).distinct()
        Manapparai= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2165).distinct()
        Manavalakurichi= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1774).distinct()
        Mandaikadu= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1775).distinct()
        Mandapam= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1776).distinct()
        Mangalampettai= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1777).distinct()
        Manimuthar= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1778).distinct()

        Mannachanallur= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1779).distinct()
        Mannargudi= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2160).distinct()
        Maraimalainagar= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2068).distinct()
        Marakkanam= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1781).distinct()
        Marandahalli= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1782).distinct()
        Marimalainagar= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2261).distinct()
        Markayankottai= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1783).distinct()
        Markkayankottai= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2234).distinct()
        Marudur= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1784).distinct()
        Marungoor= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1785).distinct()
        Mayiladuthurai= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2096).distinct()
        Mecheri= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1786).distinct()
        Melachokkanathapuram= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1787).distinct()
        Melagaram= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1788).distinct()
        Melaseval= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1789).distinct()
        Melattur= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1790).distinct()
        Melur= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2093).distinct()
        Melvisharam= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2175).distinct()

        Mettupalayam= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2071).distinct()
        Mettur= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2119).distinct()
        Minjur= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1791).distinct()
        Mohanur= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1792).distinct()
        Moolaikaraipatti= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1793).distinct()
        Mopperipalayam= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2209).distinct()
        Moppiripalayam= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1796).distinct()
        Mudukulathur= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1797).distinct()
        Mukkudal= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1798).distinct()
        Mulagumoodu= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1799).distinct()
        Mulanur= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1800).distinct()
        Musiri= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1801).distinct()
        Muthupettai= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1802).distinct()
        Muthur= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1804).distinct()
        Mylaudy= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1805).distinct()

        Naduvattam= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1806).distinct()
        Nagapattinam= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2098).distinct()
        Nagercoil= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2212).distinct()
        Nagojanahalli= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1807).distinct()
        Nallampatti= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1808).distinct()
        Nalloor= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1809).distinct()
        Namagiripettai= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1810).distinct()
        Namakkal= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2100).distinct()
        Nambiyur= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1811).distinct()
        Nangavalli= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2194).distinct()
        Nangavaram= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1812).distinct()
        Nanguneri= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1813).distinct()
        Nannilam= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1814).distinct()
        Naranammalpuram= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1815).distinct()
        Narasimmanaickenpalayam= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1816).distinct()
        Narasingapuram= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2134).distinct()
        Naravarikuppam= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1817).distinct()
        Nasiyanur= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1818).distinct()
        Natham= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1819).distinct()
        Natrampalli= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1820).distinct()
        Nattarasankottai= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1821).distinct()
        Nazareth= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1822).distinct()
        Needamangalam= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1823).distinct()
        Neikkarapatti= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1824).distinct()
        Nellikuppam= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2074).distinct()
        Nelliyalam= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2156).distinct()
        Nemili= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1825).distinct()
        Nerkuppai= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1826).distinct()
        Nerunjipettai= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2201).distinct()
        Neyyoor= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1827).distinct()
        Nilakottai= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1828).distinct()
        No_4_Veerapandi= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1830).distinct()
        Odaipatti= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1831).distinct()
        Odayakulam= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1832).distinct()
        oddanchatram= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2249).distinct()
        Oddanchatram= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2079).distinct()
        Odugathur= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1833).distinct()
        Omalur= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1834).distinct()
        Othakkalmandapam= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1835).distinct()

        Pacode = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1836).distinct()
        Padaiveedu= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2197).distinct()
        Padaveedu= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1837).distinct()
        Padmanabhapuram= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2089).distinct()
        Palacode= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1838).distinct()
        Palamedu= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1839).distinct()
        Palani= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2080).distinct()
        Palanichettipatti= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1840).distinct()
        Palapallam= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1842).distinct()
        Palayam= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1843).distinct()
        Palladam= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1844).distinct()
        Pallapalayam= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1845).distinct()
        Pallathur= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1846).distinct()
        Pallavapuram= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2069).distinct()
        Pallikonda= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1847).distinct()
        Pallipattu= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2185).distinct()
        Pallipet= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1848).distinct()
        Palugal= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1849).distinct()
        Pammal= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2176).distinct()
        Panagudi= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1850).distinct()
        Panamarathupatty= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1851).distinct()
        Panapakkam= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1852).distinct()
        Pandamangalam= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1853).distinct()
        Pannaikkadu= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1854).distinct()
        Panpoli= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1855).distinct()
        Panruti= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2075).distinct()
        Papanasam= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1856).distinct()
        Papparapatti= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1857).distinct()
        Pappireddipatti= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1858).distinct()
        Paramakudi= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2125).distinct()
        Paramathy= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1859).distinct()
        Parangipettai= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1860).distinct()
        Paravai= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1861).distinct()
        Pathamadai= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1862).distinct()
        Pattanam= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1863).distinct()
        Pattukottai= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2136).distinct()
        Pennadam= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1864).distinct()
        Pennagaram= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1865).distinct()
        
        Pennathur= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1866).distinct()
        Peraiyur= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1867).distinct()
        Perambalur= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2109).distinct()
        Peravoorani= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2222).distinct()
        Peravurani= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1868).distinct()
        Periyakodiveri= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2202).distinct()
        Periyakulam= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2166).distinct()
        Periyanaickenpalayam= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1870).distinct()
        Periyanegamam= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1871).distinct()
        Pernamallur= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1872).distinct()
        Pernambut= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2158).distinct()
        Perumagalur= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1873).distinct()
        Perumbalur= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2266).distinct()
        Perundurai= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1874).distinct()
        Perungulam= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1875).distinct()
        Pethampalayam= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1876).distinct()
        Pethanaickanpalayam= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1877).distinct()
        Pillanallur= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1878).distinct()
        PJCholapuram= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2182).distinct()
        P_Mettupalayam= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1881).distinct()
        P_N_Patty= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1882).distinct()
        Podhaturpet= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1883).distinct()
        Pollachi= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2072).distinct()
        Polur= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1884).distinct()
        Ponmanai= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1885).distinct()
        Ponnamaravathy= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1887).distinct()
        Ponnampatti= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1888).distinct()
        Poolambadi= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1889).distinct()
        Poolampatti= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1891).distinct()
        Poolampatty= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2193).distinct()
        Pooluvapatti= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1893).distinct()
        Poonamallee= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2167).distinct()
        Pothanur= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1894).distinct()
        Pudukkottai= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2110).distinct()
        Pudukottai= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2264).distinct()
        Pudupalayam= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1895).distinct()
        Pudupatti= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1896).distinct()
        Pudur= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1897).distinct()
        
        Pudur_S = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2239).distinct()
        Pudur_V= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2243).distinct()
        Puduvayal= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1899).distinct()
        Puliangudi= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2130).distinct()
        Puliyangudi= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2267).distinct()
        Puliyur= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1900).distinct()
        Pullambadi= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1901).distinct()
        PunjaiPugalur= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2231).distinct()
        Punjaipuliampatti= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2083).distinct()
        Punjaithottakurichi= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1903).distinct()
        Puthalam= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1905).distinct()
        Puthukadai= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1906).distinct()
        Puvalur= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1907).distinct()
        Rajapalayam= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2133).distinct()
        Ramanathapuram= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2107).distinct()
        Rameswaram= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2157).distinct()
        Ranipet= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2104).distinct()
        Rasipuram= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2101).distinct()
        Rayagiri= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1908).distinct()
        Reethapuram= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1909).distinct()
        R_Pudupatty= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1910).distinct()
        R_S_Mangalam= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1911).distinct()

        Salangapalayam = MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1912).distinct()
        Samalapuram= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1913).distinct()
        Sambavarvadakarai= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1914).distinct()
        Sambavar_vadakarai= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2240).distinct()
        Sangaramanallur= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1915).distinct()
        Sankagiri= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1916).distinct()
        Sankarankoil= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2268).distinct()
        Sankarankovil= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2103).distinct()
        Sankarapuram= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1917).distinct()
        Sankari= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1918).distinct()
        SankarNagar= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1920).distinct()
        Sarkarsamakulam= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1921).distinct()
        Sathankulam= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1922).distinct()
        Sathyamangalam= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2084).distinct()
        Sattur= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2127).distinct()
        Sawyerpuram= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1923).distinct()
        Sayalkudi= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1924).distinct()
        Seerapalli= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1926).distinct()
        Seithur= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1927).distinct()
        Sendamangalam= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1928).distinct()
        Sengottai= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2131).distinct()
        Sentharappatty= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1929).distinct()
        Sevugampatti= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1930).distinct()
        Sholapuram= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1931).distinct()
        Sholavandan= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1932).distinct()
        Sholingur= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2189).distinct()
        Sholur= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1933).distinct()
        Singampunari= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1934).distinct()
        Sirkali= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2097).distinct()
        Sirugamani= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1936).distinct()
        Sirumugai= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1937).distinct()
        Sithayankottai= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1938).distinct()
        Sivagangai= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2115).distinct()
        Sivagiri= MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2241).distinct()
        Sivagiri_Erode=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2184).distinct()
        Sivagiri_Tenkasi=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1939).distinct()
        Sivakasi=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2177).distinct()
        S_Kannanur=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1940).distinct()
        
        S_Kodikulam=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1941).distinct()
        Srimushnam=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1942).distinct()
        Sriperumbudur=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1944).distinct() 
        Sriramapuram=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1945).distinct()
        Srivaikuntam=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1946).distinct()
        Srivilliputhur=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2170).distinct()
        Suchindrum=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1947).distinct()
        Suleeswaranpatti=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1948).distinct()
        Suleswaranpatti=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2218).distinct()
        Sulur=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1949).distinct()
        Sundarapandiam=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1950).distinct()
        Sundarapandiapuram=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1951).distinct()
        Sundarapandiyapuram=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1952).distinct()
        Swamimalai=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1953).distinct()

        Tambaram=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2070).distinct()
        Tenkasi=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2126).distinct()
        Thadikombu=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1954).distinct()
        Thakkolam=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1955).distinct()
        Thalainayar=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2223).distinct()
        Thalanayar=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1956).distinct()
        Thamaraikulam=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1957).distinct()
        Thammampatty=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1958).distinct()
        Tharangambadi=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1959).distinct()
        Thathaiyangarpet=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1960).distinct()
        Thathayangarpet=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2226).distinct()
        Thazhakudy=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1964).distinct()
        Theni_Allinagaram=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2108).distinct()
        Thenkarai=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1965).distinct()
        Thenthamaraikulam=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1966).distinct()
        Theroor=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1967).distinct()
        Thevaram=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1968).distinct()
        Thevur=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1969).distinct()
        Thimiri=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1970).distinct()
        Thingalnagar=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1971).distinct()
        Thirubuvanam=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1972).distinct()
        Thirukalukundram=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2179).distinct()
        Thirukattupalli=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1973).distinct()
        Thirukazhukundram=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1974).distinct()
        Thirukkurungudi=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1975).distinct()
        Thirukurankudi=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2238).distinct()
        Thirumalayampalayam=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1976).distinct()
        Thirumazhisai=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1977).distinct()
        Thirumurugan_poondi=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2203).distinct()
        Thirunageswaram=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1979).distinct()
        Thiruninravur=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2186).distinct()
        Thiruparappu=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1980).distinct()
        Thirupathur=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2256).distinct()
        Thiruporur=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1983).distinct()
        Thiruppananthal=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1981).distinct()
        Thiruppathur=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1982).distinct()
        Thiruppuvanam=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1985).distinct()
        
        Thiruthangal=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2135).distinct()
        Thiruthani=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1986).distinct()
        Thiruthuraipoondi=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2159).distinct()
        Thiruvaiyaru=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1987).distinct()
        Thiruvalam=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1988).distinct()
        Thiruvallur=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2260).distinct()
        Thiruvannamalai=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2148).distinct()
        Thiruvannamalai1=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2112).distinct()
        Thiruvarur=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2111).distinct()
        Thiruvathipuram=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2144).distinct()
        Thiruvattar=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1989).distinct()
        Thiruvengadam=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1990).distinct()
        Thiruverkadu=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2139).distinct()
        Thiruvidaimaruthur=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1991).distinct()
        Thiruvithancode=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1992).distinct()
        Thisayanvilai=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1994).distinct()
        Thittacherry=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2224).distinct()
        Thittachery=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1995).distinct()
        Thittakudi=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1996).distinct()
        Thiyagadurgam=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1997).distinct()
        Thondamuthur=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1998).distinct()
        Thondi=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=1999).distinct()
        Thoothukudi=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2215).distinct()
        Thottiam=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2000).distinct()
        Thuraiyur=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2155).distinct()
        Thuvakudi=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2153).distinct()
        Tindivanam=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2146).distinct()
        Tiruchengode=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2129).distinct()
        Tirukalukundram=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2001).distinct()
        Tirumangalam=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2116).distinct()
        Tirunelveli=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2216).distinct()
        Tirupathur=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2236).distinct()
        Tirupattur=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2003).distinct()
        Tiruppur=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2210).distinct()
        Tiruvallur=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2113).distinct()
        Tiruvarur=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2263).distinct()
        T_Kallupatti=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2004).distinct()

        Udangudi=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2006).distinct()
        Udayarpalayam=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2007).distinct()
        Udayendiram=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2008).distinct()
        Udhagamandalam=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2105).distinct()
        Udumalaipet=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2168).distinct()
        Ulundurpet=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2220).distinct()
        Unnamalaikadai=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2011).distinct()
        Uppidamangalam=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2012).distinct()
        Uppiliapuram=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2013).distinct()
        Usilampatti=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2095).distinct()
        Uthamapalayam=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2014).distinct()
        Uthangarai=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2015).distinct()
        Uthayendram=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2187).distinct()
        Uthiramerur=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2016).distinct()
        Uthukottai=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2017).distinct()
        Uthukuli=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2018).distinct()
        Vadakarai_keelpidagai=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2242).distinct()
        Vadakarai_Keelpidagai=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2019).distinct()
        Vadakkanandal=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2020).distinct()
        Vadakkuvalliyur=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2022).distinct()
        Vadakkuvalliyur1=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2021).distinct()
        Vadalur=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2219).distinct()
        Vadamadurai=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2023).distinct()
        Vadipatti=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2024).distinct()
        Vadugapatti=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2025).distinct()
        Vaitheeswarankoil=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2026).distinct()
        Valangaiman=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2030).distinct()
        Valappady=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2027).distinct()
        Valavanur=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2028).distinct()
        Vallam=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2029).distinct()
        Valvachagostam=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2031).distinct()
        Vanavasi=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2195).distinct()
        Vandavasi=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2143).distinct()
        Vaniputhur=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2032).distinct()
        Vaniyambadi=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2147).distinct()
        Varadarajanpettai=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2033).distinct()
        Varatharajanpettai=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2034).distinct()

        Vasudevanallur=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2035).distinct()
        Vazhapadi=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2036).distinct()
        Vedapatti=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2037).distinct()
        Vedaranyam=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2262).distinct()
        Vedasandur=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2038).distinct()
        Veeraganur=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2039).distinct()
        Veerakkalpudur  =MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2040).distinct()
        Veerapandi=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2041).distinct()
        Veeravanallur=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2042).distinct()
        Velankanni=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2043).distinct()
        Vellakoil=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2252).distinct()
        Vellakovil=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2140).distinct()
        Vellalore=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2044).distinct()
        Vellimalai=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2045).distinct()
        Vellore=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2214).distinct()
        Velur=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2046).distinct()
        Vengampudur=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2047).distinct()
        Vengarai=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2048).distinct()
        Vennandur=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2049).distinct()
        Veppathur=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2050).distinct()
        Verkilambi=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2051).distinct()
        Vettaikaranpudur=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2052).distinct()
        Vettavalam=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2053).distinct()
        Vickramasingapuram=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2117).distinct()
        Vilapakkam=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2054).distinct()
        Vilathikulam=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2055).distinct()
        Vilavoor=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2056).distinct()
        Villuppuram=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2114).distinct()
        Villupuram=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2257).distinct()
        Virudhachalam=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2076).distinct()
        Virudhunagar=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2106).distinct()
        V_Pudur=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2057).distinct()
        Walajabad=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2058).distinct()
        Walajapet=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2124).distinct()
        Watrap=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2059).distinct()
        W_Pudupatti=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2060).distinct()
        ZaminUthukulam=MasterSanctionForm.objects.values_list('Sector', flat=True).order_by('Sector').filter(AgencyName=2062).distinct()


        a = MasterSanctionForm.objects.values_list('Project_ID', flat=True).order_by('Project_ID').filter(AgencyType=request.POST.get('AgencyType')).filter(AgencyName=request.POST.get('AgencyName')).filter(Sector=request.POST.get('Sector'))

        project_ids = MasterSanctionForm.objects.values('AgencyName', 'Sector', 'Project_ID').all()
        p = ReleaseRequestModel.objects.filter(id=obj_id)
        print(p)

        extra_context = {
            'p':p,
            'project_ids':project_ids,
            'ZaminUthukulam':ZaminUthukulam,
            'W_Pudupatti':W_Pudupatti,
            'Watrap':Watrap,
            'Walajapet':Walajapet,
            'Walajabad':Walajabad,
            'V_Pudur':V_Pudur,
            'Virudhunagar':Virudhunagar,
            'Virudhachalam':Virudhachalam,
            'Villupuram':Villupuram,
            'Villuppuram':Villuppuram,
            'Vilavoor':Vilavoor,
            'Vilathikulam':Vilathikulam,
            'Vilapakkam':Vilapakkam,
            'Vickramasingapuram':Vickramasingapuram,
            'Vettavalam':Vettavalam,
            'Vettaikaranpudur':Vettaikaranpudur,
            'Verkilambi':Verkilambi,
            'Veppathur':Veppathur,
            'Vennandur':Vennandur,
            'Vengarai':Vengarai,
            'Vengampudur':Vengampudur,
            'Velur':Velur,
            'Vellore':Vellore,
            'Vellimalai':Vellimalai,
            'Vellalore':Vellalore,
            'Vellakovil':Vellakovil,
            'Vellakoil':Vellakoil,
            'Velankanni':Velankanni,
            'Veeravanallur':Veeravanallur,
            'Veerapandi':Veerapandi,
            'Veerakkalpudur':Veerakkalpudur,
            'Veeraganur':Veeraganur,
            'Vedasandur':Vedasandur,
            'Vedaranyam':Vedaranyam,
            'Vedapatti':Vedapatti,
            'Vazhapadi':Vazhapadi,
            'Vasudevanallur':Vasudevanallur,
            'Varatharajanpettai':Varatharajanpettai,
            'Varadarajanpettai':Varadarajanpettai,
            'Vaniyambadi':Vaniyambadi,
            'Vaniputhur':Vaniputhur,
            'Vandavasi':Vandavasi,
            'Vanavasi':Vanavasi,
            'Valvachagostam':Valvachagostam,
            'Vallam':Vallam,
            'Valavanur':Valavanur,
            'Valappady':Valappady,
            'Valangaiman':Valangaiman,
            'Vaitheeswarankoil':Vaitheeswarankoil,
            'Vadugapatti':Vadugapatti,
            'Vadipatti':Vadipatti,
            'Vadamadurai':Vadamadurai,
            'Vadalur':Vadalur,
            'Vadakkuvalliyur1':Vadakkuvalliyur1,
            'Vadakkuvalliyur':Vadakkuvalliyur,
            'Vadakkanandal':Vadakkanandal,
            'Vadakarai_Keelpidagai':Vadakarai_Keelpidagai,
            'Vadakarai_keelpidagai':Vadakarai_keelpidagai,
            'Uthukuli':Uthukuli,
            'Uthukottai':Uthukottai,
            'Uthiramerur':Uthiramerur,
            'Uthayendram':Uthayendram,
            'Uthangarai':Uthangarai,
            'Uthamapalayam':Uthamapalayam,
            'Usilampatti':Usilampatti,
            'Uppiliapuram':Uppiliapuram,
            'Uppidamangalam':Uppidamangalam,
            'Unnamalaikadai':Unnamalaikadai,
            'Ulundurpet':Ulundurpet,
            'Udumalaipet':Udumalaipet,
            'Udhagamandalam':Udhagamandalam,
            'Udayendiram':Udayendiram,
            'Udayarpalayam':Udayarpalayam,
            'Udangudi':Udangudi,
            'T_Kallupatti':T_Kallupatti,
            'Tiruvarur':Tiruvarur,
            'Tiruvallur':Tiruvallur,
            'Tiruppur':Tiruppur,
            'Tirupattur':Tirupattur,
            'Tirupathur':Tirupathur,
            'Tirunelveli':Tirunelveli,
            'Tirumangalam':Tirumangalam,
            'Tirukalukundram':Tirukalukundram,
            'Tiruchengode':Tiruchengode,
            'Tindivanam':Tindivanam,
            'Thuvakudi':Thuvakudi,
            'Thuraiyur':Thuraiyur,
            'Thottiam':Thottiam,
            'Thoothukudi':Thoothukudi,
            'Thondi':Thondi,
            'Thondamuthur':Thondamuthur,
            'Thiyagadurgam':Thiyagadurgam,
            'Thittakudi':Thittakudi,
            'Thittachery':Thittachery,
            'Thittacherry':Thittacherry,
            'Thisayanvilai':Thisayanvilai,
            'Thiruvithancode':Thiruvithancode,
            'Thiruvidaimaruthur':Thiruvidaimaruthur,
            'Thiruverkadu':Thiruverkadu,
            'Thiruvengadam':Thiruvengadam,
            'Thiruvattar':Thiruvattar,
            'Thiruvathipuram':Thiruvathipuram,
            'Thiruvarur':Thiruvarur,
            'Thiruvannamalai1':Thiruvannamalai1,
            'Thiruvannamalai':Thiruvannamalai,
            'Thiruvallur':Thiruvallur,
            'Thiruvalam':Thiruvalam,
            'Thiruvaiyaru':Thiruvaiyaru,
            'Thiruthuraipoondi':Thiruthuraipoondi,
            'Thiruthani':Thiruthani,
            'Thiruthangal':Thiruthangal,
            'Thiruppuvanam':Thiruppuvanam,
            'Thiruppathur':Thiruppathur,
            'Thiruppananthal':Thiruppananthal,
            'Thiruporur':Thiruporur,
            'Thirupathur':Thirupathur,
            'Thiruparappu':Thiruparappu,
            'Thiruninravur':Thiruninravur,
            'Thirunageswaram':Thirunageswaram,
            'Thirumurugan_poondi':Thirumurugan_poondi,
            'Thirumazhisai':Thirumazhisai,
            'Thirumalayampalayam':Thirumalayampalayam,
            'Thirukurankudi':Thirukurankudi,
            'Thirukkurungudi':Thirukkurungudi,
            'Thirukazhukundram':Thirukazhukundram,
            'Thirukattupalli':Thirukattupalli,
            'Thirukalukundram':Thirukalukundram,
            'Thirubuvanam':Thirubuvanam,
            'Thingalnagar':Thingalnagar,
            'Thimiri':Thimiri,
            'Thevur':Thevur,
            'Thevaram':Thevaram,
            'Theroor':Theroor,
            'Thenthamaraikulam':Thenthamaraikulam,
            'Thenkarai':Thenkarai,
            'Theni_Allinagaram':Theni_Allinagaram,
            'Thazhakudy':Thazhakudy,
            'Thathayangarpet':Thathayangarpet,
            'Thathaiyangarpet':Thathaiyangarpet,
            'Tharangambadi':Tharangambadi,
            'Thammampatty':Thammampatty,
            'Thamaraikulam':Thamaraikulam,
            'Thalanayar':Thalanayar,
            'Thalainayar':Thalainayar,
            'Thakkolam':Thakkolam,
            'Thadikombu':Thadikombu,
            'Tenkasi':Tenkasi,
            'Tambaram':Tambaram,
            'Swamimalai':Swamimalai,
            'Sundarapandiyapuram':Sundarapandiyapuram,
            'Sundarapandiapuram':Sundarapandiapuram,
            'Sundarapandiam':Sundarapandiam,
            'Sulur':Sulur,
            'Suleswaranpatti':Suleswaranpatti,
            'Suleeswaranpatti':Suleeswaranpatti,
            'Suchindrum':Suchindrum,
            'Srivilliputhur':Srivilliputhur,
            'Srivaikuntam':Srivaikuntam,
            'Sriramapuram':Sriramapuram,
            'Sriperumbudur':Sriperumbudur,
            'Srimushnam':Srimushnam,
            'S_Kodikulam':S_Kodikulam,
            'S_Kannanur':S_Kannanur,
            'Sivakasi':Sivakasi,
            'Sivagiri_Tenkasi':Sivagiri_Tenkasi,
            'Sivagiri_Erode':Sivagiri_Erode,
            'Sivagangai':Sivagangai,
            'Sithayankottai':Sithayankottai,
            'Sirumugai':Sirumugai,
            'Sirugamani':Sirugamani,
            'Sirkali':Sirkali,
            'Singampunari':Singampunari,
            'Sholur':Sholur,
            'Sholingur':Sholingur,
            'Sholavandan':Sholavandan,
            'Sholapuram':Sholapuram,
            'Sevugampatti':Sevugampatti,
            'Sentharappatty':Sentharappatty,
            'Sengottai':Sengottai,
            'Sendamangalam':Sendamangalam,
            'Seithur':Seithur,
            'Seerapalli':Seerapalli,
            'Sayalkudi':Sayalkudi,
            'Sawyerpuram':Sawyerpuram,
            'Sattur':Sattur,
            'Sathyamangalam':Sathyamangalam,
            'Sathankulam':Sathankulam,
            'Sarkarsamakulam':Sarkarsamakulam,
            'SankarNagar':SankarNagar,
            'Sankari':Sankari,
            'Sankarapuram':Sankarapuram,
            'Sankarankovil':Sankarankovil,
            'Sankarankoil':Sankarankoil,
            'Sankagiri':Sankagiri,
            'Sangaramanallur':Sangaramanallur,
            'Sambavar_vadakarai':Sambavar_vadakarai,
            'Sambavarvadakarai':Sambavarvadakarai,
            'Samalapuram':Samalapuram,
            'Salangapalayam':Salangapalayam,
            'R_S_Mangalam':R_S_Mangalam,
            'R_Pudupatty':R_Pudupatty,
            'Reethapuram':Reethapuram,
            'Rayagiri':Rayagiri,
            'Rasipuram':Rasipuram,
            'Ranipet':Ranipet,
            'Rameswaram':Rameswaram,
            'Ramanathapuram':Ramanathapuram,
            'Rajapalayam':Rajapalayam,
            'Puvalur':Puvalur,
            'Puthukadai':Puthukadai,
            'Puthalam':Puthalam,
            'Punjaithottakurichi':Punjaithottakurichi,
            'Punjaipuliampatti':Punjaipuliampatti,
            'PunjaiPugalur':PunjaiPugalur,
            'Pullambadi':Pullambadi,
            'Puliyur':Puliyur,
            'Puliyangudi':Puliyangudi,
            'Puliangudi':Puliangudi,
            'Puduvayal':Puduvayal,
            'Pudur_V':Pudur_V,
            'Pudur_S':Pudur_S,
            'Pudur':Pudur,
            'Pudupatti':Pudupatti,
            'Pudupalayam':Pudupalayam,
            'Pudukottai':Pudukottai,
            'Pudukkottai':Pudukkottai,
            'Pothanur':Pothanur,
            'Poonamallee':Poonamallee,
            'Pooluvapatti':Pooluvapatti,
            'Poolampatty':Poolampatty,
            'Poolampatti':Poolampatti,
            'Poolambadi':Poolambadi,
            'Ponnampatti':Ponnampatti,
            'Ponnamaravathy':Ponnamaravathy,
            'Ponmanai':Ponmanai,
            'Polur':Polur,
            'Pollachi':Pollachi,
            'Podhaturpet':Podhaturpet,
            'P_N_Patty':P_N_Patty,
            'P_Mettupalayam':P_Mettupalayam,
            'PJCholapuram':PJCholapuram,
            'Pillanallur':Pillanallur,
            'Pethanaickanpalayam':Pethanaickanpalayam,
            'Pethampalayam':Pethampalayam,
            'Perungulam':Perungulam,
            'Perundurai':Perundurai,
            'Perumbalur':Perumbalur,
            'Perumagalur':Perumagalur,
            'Pernambut':Pernambut,
            'Pernamallur':Pernamallur,
            'Periyanegamam':Periyanegamam,
            'Periyanaickenpalayam':Periyanaickenpalayam,
            'Periyakulam':Periyakulam,
            'Periyakodiveri':Periyakodiveri,
            'Peravurani':Peravurani,
            'Peravoorani':Peravoorani,
            'Perambalur':Perambalur,
            'Peraiyur':Peraiyur,
            'Pennathur':Pennathur,
            'Pennagaram':Pennagaram,
            'Pennadam':Pennadam,
            'Pattukottai':Pattukottai,
            'Pattanam':Pattanam,
            'Pathamadai':Pathamadai,
            'Paravai':Paravai,
            'Parangipettai':Parangipettai,
            'Paramathy':Paramathy,
            'Paramakudi':Paramakudi,
            'Pappireddipatti':Pappireddipatti,
            'Papparapatti':Papparapatti,
            'Papanasam':Papanasam,
            'Panruti':Panruti,
            'Panpoli':Panpoli,
            'Pannaikkadu':Pannaikkadu,
            'Pandamangalam':Pandamangalam,
            'Panapakkam':Panapakkam,
            'Panamarathupatty':Panamarathupatty,
            'Panagudi':Panagudi,
            'Pammal':Pammal,
            'Palugal':Palugal,
            'Pallipet':Pallipet,
            'Pallipattu':Pallipattu,
            'Pallikonda':Pallikonda,
            'Pallavapuram':Pallavapuram,
            'Pallathur':Pallathur,
            'Pallapalayam':Pallapalayam,
            'Palladam':Palladam,
            'Palayam':Palayam,
            'Palapallam':Palapallam,
            'Palanichettipatti':Palanichettipatti,
            'Palani':Palani,
            'Palamedu':Palamedu,
            'Palacode':Palacode,
            'Padmanabhapuram':Padmanabhapuram,
            'Padaveedu':Padaveedu,
            'Padaiveedu':Padaiveedu,
            'Pacode':Pacode,
            'Othakkalmandapam':Othakkalmandapam,
            'Omalur':Omalur,
            'Odugathur':Odugathur,
            'Oddanchatram':Oddanchatram,
            'oddanchatram':oddanchatram,
            'Odayakulam':Odayakulam,
            'Odaipatti':Odaipatti,
            'No_4_Veerapandi':No_4_Veerapandi,
            'Nilakottai':Nilakottai,
            'Neyyoor':Neyyoor,
            'Nerunjipettai':Nerunjipettai,
            'Nerkuppai':Nerkuppai,
            'Nemili':Nemili,
            'Nelliyalam':Nelliyalam,
            'Nellikuppam':Nellikuppam,
            'Neikkarapatti':Neikkarapatti,
            'Needamangalam':Needamangalam,
            'Nazareth':Nazareth,
            'Nattarasankottai':Nattarasankottai,
            'Natrampalli':Natrampalli,
            'Natham':Natham,
            'Nasiyanur':Nasiyanur,
            'Naravarikuppam':Naravarikuppam,
            'Narasingapuram':Narasingapuram,
            'Narasimmanaickenpalayam':Narasimmanaickenpalayam,
            'Naranammalpuram':Naranammalpuram,
            'Nannilam':Nannilam,
            'Nanguneri':Nanguneri,
            'Nangavaram':Nangavaram,
            'Nangavalli':Nangavalli,
            'Nambiyur':Nambiyur,
            'Namakkal':Namakkal,
            'Namagiripettai':Namagiripettai,
            'Nalloor':Nalloor,
            'Nallampatti':Nallampatti,
            'Nagojanahalli':Nagojanahalli,
            'Nagercoil':Nagercoil,
            'Nagapattinam':Nagapattinam,
            'Naduvattam':Naduvattam,
            'Mylaudy':Mylaudy,
            'Muthur':Muthur,
            'Muthupettai':Muthupettai,
            'Musiri':Musiri,
            'Mulanur':Mulanur,
            'Mulagumoodu':Mulagumoodu,
            'Mukkudal':Mukkudal,
            'Mudukulathur':Mudukulathur,
            'Moppiripalayam':Moppiripalayam,
            'Mopperipalayam':Mopperipalayam,
            'Moolaikaraipatti':Moolaikaraipatti,
            'Mohanur':Mohanur,
            'Minjur':Minjur,
            'Mettur':Mettur,
            'Mettupalayam':Mettupalayam,
            'Melvisharam':Melvisharam,
            'Melur':Melur,
            'Melattur':Melattur,
            'Melaseval':Melaseval,
            'Melagaram':Melagaram,
            'Melachokkanathapuram':Melachokkanathapuram,
            'Mecheri':Mecheri,
            'Mayiladuthurai':Mayiladuthurai,
            'Marungoor':Marungoor,
            'Marudur':Marudur,
            'Markkayankottai':Markkayankottai,
            'Markayankottai':Markayankottai,
            'Marimalainagar':Marimalainagar,
            'Marandahalli':Marandahalli,
            'Marakkanam':Marakkanam,
            'Maraimalainagar':Maraimalainagar,
            'Mannargudi':Mannargudi,
            'Mannachanallur':Mannachanallur,
            'Manimuthar':Manimuthar,
            'Mangalampettai':Mangalampettai,
            'Mandapam':Mandapam,
            'Mandaikadu':Mandaikadu,
            'Manavalakurichi':Manavalakurichi,
            'Manapparai':Manapparai,
            'Manaparai':Manaparai,
            'Manamadurai':Manamadurai,
            'Manalurpet':Manalurpet,
            'Manalmedu':Manalmedu,
            'Mamsapuram':Mamsapuram,
            'Mamallapuram':Mamallapuram,
            'Mallur':Mallur,
            'Mallasamudram':Mallasamudram,
            'Mallanginar':Mallanginar,
            'Madukkur':Madukkur,
            'Madukkarai':Madukkarai,
            'Madhuranthagam':Madhuranthagam,
            'Lalpettai':Lalpettai,
            'Lalgudi':Lalgudi,
            'Lakkampatti':Lakkampatti,
            'Labbaikudikadu':Labbaikudikadu,
            'Kuzhithurai':Kuzhithurai,
            'Kuthalam':Kuthalam,
            'Kutchanur':Kutchanur,
            'Kurumbalur':Kurumbalur,
            'Kurinjipadi':Kurinjipadi,
            'Kunnathur':Kunnathur,
            'Kumbakonam':Kumbakonam,
            'Kumarapuram':Kumarapuram,
            'Kulithalai':Kulithalai,
            'Kulasekaram':Kulasekaram,
            'Kuhalur':Kuhalur,
            'Kuchanur':Kuchanur,
            'Krishnarayapuram':Krishnarayapuram,
            'Krishnagiri':Krishnagiri,
            'Kovilpatti':Kovilpatti,
            'Kottur':Kottur,
            'Kottaram':Kottaram,
            'Kottaiyur':Kottaiyur,
            'Kothanalloor':Kothanalloor,
            'Kotagiri':Kotagiri,
            'Koradachery':Koradachery,
            'Koothappar':Koothappar,
            'Koothanallur':Koothanallur,
            'Konganapuram':Konganapuram,
            'Kombai':Kombai,
            'Komarapalayam':Komarapalayam,
            'Kollemcode':Kollemcode,
            'Kollankoil':Kollankoil,
            'Kolathur':Kolathur,
            'Kolathupalayam':Kolathupalayam,
            'Kolappalur':Kolappalur,
            'Kodumudi':Kodumudi,
            'Kodavasal':Kodavasal,
            'Kodaikanal':Kodaikanal,
            'Kinathukadavu':Kinathukadavu,
            'Kilpennathur':Kilpennathur,
            'Killiyoor':Killiyoor,
            'Killai':Killai,
            'Kilkundah':Kilkundah,
            'Kilambadi':Kilambadi,
            'Ketti':Ketti,
            'Kempanaickenpalayam':Kempanaickenpalayam,
            'Kelamangalam':Kelamangalam,
            'Keezhkulam':Keezhkulam,
            'Keeripatty':Keeripatty,
            'Keeranur':Keeranur,
            'Keeramangkalam':Keeramangkalam,
            'Keeramangalam':Keeramangalam,
            'Keelvelur':Keelvelur,
            'Keelapavoor':Keelapavoor,
            'Keelakarai':Keelakarai,
            'Kayathar':Kayathar,
            'Kayalpattinam':Kayalpattinam,
            'Kaveripattinam':Kaveripattinam,
            'Kattuputhur':Kattuputhur,
            'Kattumannarkoil':Kattumannarkoil,
            'Kasipalayam_G':Kasipalayam_G,
            'Karur':Karur,
            'Karupur':Karupur,
            'Karuppur':Karuppur,
            'Karunguzhi':Karunguzhi,
            'Karungal':Karungal,
            'Karumathampatti':Karumathampatti,
            'Karumandichellipalayam':Karumandichellipalayam,
            'Kariyapatti':Kariyapatti,
            'Karimangalam':Karimangalam,
            'Karambakudi':Karambakudi,
            'Karambakkudi':Karambakkudi,
            'Karaikudi':Karaikudi,
            'Kappiyarai':Kappiyarai,
            'Kanniyakumari':Kanniyakumari,
            'Kannivadi':Kannivadi,
            'Kannankurichi':Kannankurichi,
            'Kannampalayam':Kannampalayam,
            'Kannamangalam':Kannamangalam,
            'Kanjikoil':Kanjikoil,
            'Kangeyam':Kangeyam,
            'Kandanur':Kandanur,
            'Kancheepuram':Kancheepuram,
            'Kanam':Kanam,
            'Kanadukathan':Kanadukathan,
            'Kamuthi':Kamuthi,
            'Kambainallur':Kambainallur,
            'Kamayagoundanpatti':Kamayagoundanpatti,
            'Kalugumalai':Kalugumalai,
            'Kallukuttam':Kallukuttam,
            'Kallidaikurichi':Kallidaikurichi,
            'Kallakurichi':Kallakurichi,
            'Kallakudi':Kallakudi,
            'Kaliyakkavilai':Kaliyakkavilai,
            'Kalavai':Kalavai,
            'Kalappanacikenpatty':Kalappanacikenpatty,
            'Kalambur':Kalambur,
            'Kalakkad':Kalakkad,
            'Kadayanallur':Kadayanallur,
            'Kadayampatty':Kadayampatty,
            'Kadayal':Kadayal,
            'Kadambur':Kadambur,
            'Kadathur':Kadathur,
            'Jolarpet':Jolarpet,
            'Jegathala':Jegathala,
            'Jayankondam':Jayankondam,
            'Jambai':Jambai,
            'Jalakandapuram':Jalakandapuram,
            'Jalagandapuram':Jalagandapuram,
            'Irugur':Irugur,
            'Illuppur':Illuppur,
            'Ilayankudi':Ilayankudi,
            'Ilanji':Ilanji,
            'Idigarai':Idigarai,
            'Idappadi':Idappadi,
            'Hulical':Hulical,
            'Harur':Harur,
            'Hanumanthampatti':Hanumanthampatti,
            'Gummidipoondi':Gummidipoondi,
            'Gudiyatham':Gudiyatham,
            'Gudalur_N':Gudalur_N,
            'Gudalur':Gudalur,
            'Greater_Chennai':Greater_Chennai,
            'Gopalasamudram':Gopalasamudram,
            'Gobichettipalayam':Gobichettipalayam,
            'Gingee':Gingee,
            'Genguvarpatti':Genguvarpatti,
            'Gangavalli':Gangavalli,
            'Ganapathipuram':Ganapathipuram,
            'Ettimadai':Ettimadai,
            'Ettayapuram':Ettayapuram,
            'Eruvadi':Eruvadi,
            'Erumapatty':Erumapatty,
            'Erumaipatti':Erumaipatti,
            'Erode':Erode,
            'Eriodu':Eriodu,
            'Eraniel':Eraniel,
            'Eral':Eral,
            'Elumalai':Elumalai,
            'Elathur':Elathur,
            'Elampillai':Elampillai,
            'Edaikazhinadu':Edaikazhinadu,
            'Edaicode':Edaicode,
            'Dindigul':Dindigul,
            'Dharmapuri':Dharmapuri,
            'Dharapuram':Dharapuram,
            'Dhaliyur':Dhaliyur,
            'Devershola':Devershola,
            'Devathanapatti':Devathanapatti,
            'Devarshola':Devarshola,
            'Devakottai':Devakottai,
            'Desur':Desur,
            'Denkanikottai':Denkanikottai,
            'Cumbum':Cumbum,
            'Cuddalore':Cuddalore,
            'C_Pudupatti':C_Pudupatti,
            'Courtallam':Courtallam,
            'Coonoor':Coonoor,
            'Colachel':Colachel,
            'Coimbatore':Coimbatore,
            'Chithode':Chithode,
            'Chinnamanur':Chinnamanur,
            'Chinnalapatti':Chinnalapatti,
            'Chidambaram':Chidambaram,
            'Chettiyarpatti':Chettiyarpatti,
            'Chettipalayam':Chettipalayam,
            'Chetpet':Chetpet,
            'Cheranmahadevi':Cheranmahadevi,
            'Chennimalai':Chennimalai,
            'Chennasamudram':Chennasamudram,
            'Chengam':Chengam,
            'Chengalpattu':Chengalpattu,
            'Boothipuram':Boothipuram,
            'Boothapandy':Boothapandy,
            'Bodinayakanur':Bodinayakanur,
            'B_Mallapuram':B_Mallapuram,
            'Bikkatti':Bikkatti,
            'Bhuvanagiri':Bhuvanagiri,
            'Bhavanisagar':Bhavanisagar,
            'Bhavani':Bhavani,
            'Belur':Belur,
            'Batlagundu':Batlagundu,
            'Balasamudram':Balasamudram,
            'Bargur':Bargur,
            'Balakrishnampatti':Balakrishnampatti,
            'Acharapakkam_sector':Acharapakkam_sector,
            'Adigaratty_sector':Adigaratty_sector,
            'Adirampattinam_sector':Adirampattinam_sector,
            'Aduthurai_sector':Aduthurai_sector,
            'Agaram_sector':Agaram_sector,
            'Agasteeswaram_sector':Agasteeswaram_sector,
            'Alagappapuram_sector':Alagappapuram_sector,
            'Alampalayam_sector':Alampalayam_sector,
            'Alandurai_sector':Alandurai_sector,
            'Alanganallur_sector':Alanganallur_sector,
            'Alangayam_sector':Alangayam_sector,
            'Alangudi_sector':Alangudi_sector,
            'Alangulam_sector':Alangulam_sector,
            'Aloor_sector':Aloor_sector,
            'Alwarkurichi_sector':Alwarkurichi_sector,
            'Alwarthirunagari_sector':Alwarthirunagari_sector,
            'Ambasamudram_sector':Ambasamudram_sector,
            'Ambur_sector':Ambur_sector,
            'Ammapettai_sector':Ammapettai_sector,
            'Ammayanaickanur_sector':Ammayanaickanur_sector,
            'Ammoor_sector':Ammoor_sector,
            'Anaimalai_sector':Anaimalai_sector, 
            'Anakaputhur_sector':Anakaputhur_sector,
            'Ananthapuram_sector':Ananthapuram_sector,
            'Andipatti_sector':Andipatti_sector,
            'Anjugramam_sector':Anjugramam_sector,
            'Annavasal_sector':Annavasal_sector,
            'Annur_sector':Annur_sector,
            'Anthiyur_sector':Anthiyur_sector,
            'Appakudal_sector':Appakudal_sector,
            'Arachalur_sector':Arachalur_sector,
            'Arakandanallur_sector':Arakandanallur_sector,
            'Arakkonam_sector':Arakkonam_sector,
            'Aralvaimozhi_sector':Aralvaimozhi_sector,
            'Arani_sector':Arani_sector,
            'Aranthangi_sector':Aranthangi_sector,
            'Aravakurichi_sector':Aravakurichi_sector,
            'Arcot_sector':Arcot_sector,
            'Arimalam_sector':Arimalam_sector,
            'Ariyalur_sector':Ariyalur_sector,
            'Ariyappampalayam_sector':Ariyappampalayam_sector,
            'Arumanai_sector':Arumanai_sector,
            'Arumbavur_sector':Arumbavur_sector,
            'Arumuganeri_sector':Arumuganeri_sector,
            'Aruppukottai_sector':Aruppukottai_sector,
            'Athani_sector':Athani_sector,
            'Athanur_sector':Athanur_sector,
            'Athur_sector':Athur_sector,
            'Attayampatty_sector':Attayampatty_sector,
            'Attoor_sector':Attoor_sector,
            'Attur_sector':Attur_sector,
            'Aundipatti_sector':Aundipatti_sector,
            'Auralvaimozhi_sector':Auralvaimozhi_sector,
            'Authoor_sector':Authoor_sector,
            'A_Vallalapatti':A_Vallalapatti,
            'Avalpoondurai':Avalpoondurai,
            'Avinashi':Avinashi,
            'Ayakudi':Ayakudi,
            'Ayikudy':Ayikudy,
            'Ayothiyapattanam':Ayothiyapattanam,
            'Ayyalur':Ayyalur,
            'Ayyampalayam':Ayyampalayam,
            'Ayyampettai':Ayyampettai,
            'Ayyothiyapattanam':Ayyothiyapattanam,
            'Azhagappapuram':Azhagappapuram,
            'Azhakiapandiyapuram':Azhakiapandiyapuram,
            'Acharapakkam_sector':Acharapakkam_sector,
            'corporation': corporation,
            'townPanchayat':townPanchayat,
            'municipality': municipality,
            'abiramam_sector':abiramam_sector,
            'achanpudur_sector':achanpudur_sector,
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
        if request.method=="POST":
            form = MonthForm(request.POST or None)
            if form.is_valid():
                form_month = get_month[form.cleaned_data['month']]
                m = form.cleaned_data['month']
        data1 = ReleaseRequestModel.objects.values('AgencyName__AgencyName', 'Sector', 'Project_ID', 'release1Amount', 'release1Date').filter(release1Date__month=form_month)
        data2 = ReleaseRequestModel.objects.values('AgencyName__AgencyName', 'Sector', 'Project_ID', 'release2Amount', 'release2Date').filter(release2Date__month=form_month)
        data3 = ReleaseRequestModel.objects.values('AgencyName__AgencyName', 'Sector', 'Project_ID', 'release3Amount', 'release3Date').filter(release3Date__month=form_month)
        data4 = ReleaseRequestModel.objects.values('AgencyName__AgencyName', 'Sector', 'Project_ID', 'release4Amount', 'release4Date').filter(release4Date__month=form_month)
        data5 = ReleaseRequestModel.objects.values('AgencyName__AgencyName', 'Sector', 'Project_ID', 'release5Amount', 'release5Date').filter(release5Date__month=form_month)
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
        'Sector'
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
