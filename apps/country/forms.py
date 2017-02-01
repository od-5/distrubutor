# coding=utf-8
from django import forms
from apps.geolocation.models import Country

__author__ = '2mitrij'


class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = ('name', 'code')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
        }
