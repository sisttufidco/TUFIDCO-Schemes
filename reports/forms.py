from django import forms
from .models import AgencyName

def agency_name_list():
    return [(str(c), str(c)) for c in AgencyName.objects.values_list('AgencyName', flat=True).order_by('AgencyName').distinct()]

class FinancialYearForm(forms.Form):
    finyears = [
        #('--------','--------'),
        ('2021-2022','2021-2022'),
        ('2022-2023','2022-2023'),
    ]
    year = forms.ChoiceField(choices=finyears, required=True, initial=1)
    agencyname = forms.ChoiceField(choices=agency_name_list())