from django import forms
from ULBForms.models import AgencyProgressModel
class MonthForm(forms.Form):
    months = [
        ('--------','--------'),
        ('January','January'),
                  ('February','February'),
                  ('March','March'),
                  ('April','April'),
                  ('May','May'),
                  ('June','June'),
                  ('July','July'),
                  ('August','August'),
                  ('September','September'),
                  ('October','October'),
                  ('November','November'),
                  ('December','December'),]
    scheme = [ 
        ("--------","--------"),
        ('KNMT', 'KNMT'),
        ('Singara Chennai 2.0','Singara Chennai 2.0')
    ]
    month = forms.ChoiceField(choices=months)
    Scheme = forms.ChoiceField(choices=scheme)

def sector_make_choices():
    return [(str(c), str(c)) for c in AgencyProgressModel.objects.values_list('Sector', flat=True).order_by('Sector').filter(ULBType="Municipality").distinct()]

def CTPsector_make_choices():
    return [(str(c), str(c)) for c in AgencyProgressModel.objects.values_list('Sector', flat=True).order_by('Sector').filter(ULBType="Town Panchayat").distinct()]

class DMASector(forms.Form):
    sector = forms.ChoiceField(choices=sector_make_choices())    

class CTPSector(forms.Form):
    sector = forms.ChoiceField(choices=CTPsector_make_choices())  

