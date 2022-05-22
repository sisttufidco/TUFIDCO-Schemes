from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput
from .models import *
from TUFIDCOapp.models import *

class AgencyProgressForm(forms.ModelForm):
    class Meta:
        model = AgencyProgressModel
        fields = ('Sector', 'status')
        widgets = {
            'status': forms.RadioSelect(),
            'nc_choices': forms.RadioSelect(),
        }

    def __init__(self, request, *args, **kwargs):
        super(AgencyProgressForm, self).__init__(*args, **kwargs)
        if not request.user.groups.filter(name__in=["Admin", 'progressdetails']).exists():
            if request.user.groups.filter(name__in=['Corporation', ]).exists():
                self.fields['Scheme'].widget = forms.Select(choices=[(str(c), str(c)) for c in
                                                                     MasterSanctionForm.objects.values_list(
                                                                         'Scheme__Scheme', flat=True).filter(
                                                                         AgencyName__AgencyName=request.user.first_name).distinct()])
                self.fields['Sector'].widget = forms.Select(choices=[(str(c), str(c)) for c in
                                                                     MasterSanctionForm.objects.values_list('Sector',
                                                                                                            flat=True).filter(
                                                                         AgencyName__AgencyName=request.user.first_name).distinct()])
                self.fields['Project_ID'].widget = forms.Select(choices=[(str(c), str(c)) for c in
                                                                         MasterSanctionForm.objects.values_list(
                                                                             'Project_ID', flat=True).filter(
                                                                             AgencyName__AgencyName=request.user.first_name).order_by(
                                                                             'SNo').distinct()])
            else:
                list = []
                for i in map(str, request.user.groups.all()):
                    list.append(i)
                self.fields['Scheme'].widget = forms.Select(choices=[(str(c), str(c)) for c in
                                                                     MasterSanctionForm.objects.values_list(
                                                                         'Scheme__Scheme', flat=True).filter(
                                                                         AgencyName__AgencyName=request.user.first_name).distinct()])
                self.fields['Sector'].widget = forms.Select(choices=[(str(c), str(c)) for c in
                                                                     MasterSanctionForm.objects.values_list('Sector',
                                                                                                            flat=True).filter(
                                                                         AgencyName__AgencyName=request.user.first_name).filter(
                                                                         AgencyType__AgencyType=list[1]).distinct()])
                self.fields['Project_ID'].widget = forms.Select(choices=[(str(c), str(c)) for c in
                                                                         MasterSanctionForm.objects.values_list(
                                                                             'Project_ID', flat=True).filter(
                                                                             AgencyName__AgencyName=request.user.first_name).filter(
                                                                             AgencyType__AgencyType=list[1]).order_by(
                                                                             'SNo').distinct()])
        else:
            self.fields['Scheme'].widget = forms.Select(choices=[(str(c), str(c)) for c in
                                                                 MasterSanctionForm.objects.values_list(
                                                                     'Scheme__Scheme', flat=True).distinct()])
            self.fields['Sector'].widget = forms.Select(choices=[(str(c), str(c)) for c in
                                                                 MasterSanctionForm.objects.values_list('Sector',
                                                                                                        flat=True).distinct()])
            self.fields['Project_ID'].widget = forms.Select(choices=[(str(c), str(c)) for c in
                                                                     MasterSanctionForm.objects.values_list(
                                                                         'Project_ID', flat=True).order_by(
                                                                         'SNo').distinct()])


class AgencySanctionForm(forms.ModelForm):
    class Meta:
        model = AgencySanctionModel
        fields = ('Sector',)
        widgets = {
            'ts_awarded': forms.RadioSelect(),
            'tr_awarded': forms.RadioSelect(),
            'wd_awarded': forms.RadioSelect()
        }

    def __init__(self, request, *args, **kwargs):
        super(AgencySanctionForm, self).__init__(*args, **kwargs)
        if not request.user.groups.filter(name__in=["Admin", 'progressdetails']).exists():
            if request.user.groups.filter(name__in=['Corporation', ]).exists():
                self.fields['Scheme'].widget = forms.Select(choices=[(str(c), str(c)) for c in
                                                                     MasterSanctionForm.objects.values_list(
                                                                         'Scheme__Scheme', flat=True).filter(
                                                                         AgencyName__AgencyName=request.user.first_name).distinct()])
                self.fields['Sector'].widget = forms.Select(choices=[(str(c), str(c)) for c in
                                                                     MasterSanctionForm.objects.values_list('Sector',
                                                                                                            flat=True).filter(
                                                                         AgencyName__AgencyName=request.user.first_name).distinct()])
                self.fields['Project_ID'].widget = forms.Select(choices=[(str(c), str(c)) for c in
                                                                         MasterSanctionForm.objects.values_list(
                                                                             'Project_ID', flat=True).filter(
                                                                             AgencyName__AgencyName=request.user.first_name).order_by(
                                                                             'SNo').distinct()])
            else:
                list = []
                for i in map(str, request.user.groups.all()):
                    list.append(i)
                print(request.user.groups.all())
                self.fields['Scheme'].widget = forms.Select(choices=[(str(c), str(c)) for c in
                                                                     MasterSanctionForm.objects.values_list(
                                                                         'Scheme__Scheme', flat=True).filter(
                                                                         AgencyName__AgencyName=request.user.first_name).distinct()])
                self.fields['Sector'].widget = forms.Select(choices=[(str(c), str(c)) for c in
                                                                     MasterSanctionForm.objects.values_list('Sector',
                                                                                                            flat=True).filter(
                                                                         AgencyName__AgencyName=request.user.first_name).filter(
                                                                         AgencyType__AgencyType=list[1]).distinct()])
                self.fields['Project_ID'].widget = forms.Select(choices=[(str(c), str(c)) for c in
                                                                         MasterSanctionForm.objects.values_list(
                                                                             'Project_ID', flat=True).filter(
                                                                             AgencyName__AgencyName=request.user.first_name).filter(
                                                                             AgencyType__AgencyType=list[1]).order_by(
                                                                             'SNo').distinct()])
        else:
            self.fields['Scheme'].widget = forms.Select(choices=[(str(c), str(c)) for c in
                                                                 MasterSanctionForm.objects.values_list(
                                                                     'Scheme__Scheme', flat=True).distinct()])
            self.fields['Sector'].widget = forms.Select(choices=[(str(c), str(c)) for c in
                                                                 MasterSanctionForm.objects.values_list('Sector',
                                                                                                        flat=True).distinct()])
            self.fields['Project_ID'].widget = forms.Select(choices=[(str(c), str(c)) for c in
                                                                     MasterSanctionForm.objects.values_list(
                                                                         'Project_ID', flat=True).order_by(
                                                                         'SNo').distinct()])

