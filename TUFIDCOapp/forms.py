from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput
from .models import *


class PlaceholderAuthForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder': 'Password'}))


class AgencyProgressForm(forms.ModelForm):
    class Meta:
        model = AgencyProgressModel
        fields = ('Sector','status')
        widgets = {
            'status': forms.RadioSelect(),
        }
    
    def __init__(self, request, *args, **kwargs):
        super(AgencyProgressForm, self).__init__(*args, **kwargs)
        self.fields['Scheme'].widget = forms.Select(choices=[(str(c), str(c)) for c in
                                                             MasterSanctionForm.objects.values_list('Scheme__Scheme',
                                                                                                    flat=True).filter(
                                                                 AgencyName__AgencyName=request.user.first_name).distinct()])
        self.fields['Sector'].widget = forms.Select(choices=[(str(c), str(c)) for c in
                                                             MasterSanctionForm.objects.values_list('Sector',
                                                                                                    flat=True).filter(
                                                                 AgencyName__AgencyName=request.user.first_name).order_by(
                                                                 'SNo').distinct()])
        self.fields['Project_ID'].widget = forms.Select(choices=[(str(c), str(c)) for c in
                                                                 MasterSanctionForm.objects.values_list('Project_ID',
                                                                                                        flat=True).filter(
                                                                     AgencyName__AgencyName=request.user.first_name).order_by(
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
        self.fields['Scheme'].widget = forms.Select(choices=[(str(c), str(c)) for c in
                                                             MasterSanctionForm.objects.values_list(
                                                                 'Scheme__Scheme',
                                                                 flat=True).filter(
                                                                 AgencyName__AgencyName=request.user.first_name).distinct()])
        self.fields['Sector'].widget = forms.Select(choices=[(str(c), str(c)) for c in
                                                             MasterSanctionForm.objects.values_list('Sector',
                                                                                                    flat=True).filter(
                                                                 AgencyName__AgencyName=request.user.first_name).order_by(
                                                                 'SNo').distinct()])
        self.fields['Project_ID'].widget = forms.Select(choices=[(str(c), str(c)) for c in
                                                                 MasterSanctionForm.objects.values_list('Project_ID',
                                                                                                        flat=True).filter(
                                                                     AgencyName__AgencyName=request.user.first_name).order_by(
                                                                     'SNo').distinct()])


ULBchoices1 = [('---------', '---------'),
               ('Municipality', 'Municipality'),
               ('Town Panchayat', 'Town Panchayat')]


class EmailForm(forms.Form):
    ULB = forms.ChoiceField(choices=ULBchoices1, widget=forms.Select(attrs={'style': 'width: 450px;',
                                                                            'class': 'form-control'}))
    subject = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'placeholder': 'Enter Subject', 'style': 'width: 450px;', 'class': 'form-control'}))
    attach = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True, 'style': 'width: 450px;',
                                                                    'class': 'form-control'}))
    message = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': 'Enter Message', 'style': 'width: 450px;', 'class': 'form-control'}))
