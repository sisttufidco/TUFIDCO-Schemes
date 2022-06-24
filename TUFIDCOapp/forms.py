from tokenize import group
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput
from .models import *


class PlaceholderAuthForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder': 'Password'}))


class EmailForm(forms.Form):
    ULB = forms.MultipleChoiceField(choices=[(str(c), str(c)) for c in
                                             User.objects.values_list('first_name', flat=True).filter(
                                                 groups__name='Agency').filter(groups__name='Municipality').order_by(
                                                 'first_name')], widget=forms.CheckboxSelectMultiple())
    subject = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'placeholder': 'Enter Subject', 'style': 'width: 450px;', 'class': 'form-control'}))
    attach = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True, 'style': 'width: 450px;',
                                                                    'class': 'form-control'}))
    message = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': 'Enter Message', 'style': 'width: 450px;', 'class': 'form-control'}))


class EmailForm2(forms.Form):
    ULB2 = forms.MultipleChoiceField(choices=[(str(c), str(c)) for c in
                                              User.objects.values_list('first_name', flat=True).filter(
                                                  groups__name='Agency').filter(groups__name='Town Panchayat').order_by(
                                                  'first_name')], widget=forms.CheckboxSelectMultiple())
    subject = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'placeholder': 'Enter Subject', 'style': 'width: 450px;', 'class': 'form-control'}))
    attach = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True, 'style': 'width: 450px;',
                                                                    'class': 'form-control'}))
    message = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': 'Enter Message', 'style': 'width: 450px;', 'class': 'form-control'}))


class EmailForm3(forms.Form):
    ULB2 = forms.MultipleChoiceField(choices=[(str(c), str(c)) for c in
                                              User.objects.values_list('first_name', flat=True).filter(
                                                  groups__name='Agency').filter(groups__name='Corporation').order_by(
                                                  'first_name')], widget=forms.CheckboxSelectMultiple())
    subject = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'placeholder': 'Enter Subject', 'style': 'width: 450px;', 'class': 'form-control'}))
    attach = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True, 'style': 'width: 450px;',
                                                                    'class': 'form-control'}))
    message = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': 'Enter Message', 'style': 'width: 450px;', 'class': 'form-control'}))

