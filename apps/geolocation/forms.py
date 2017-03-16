# coding=utf-8
from django import forms

from .models import City, Region, Country

__author__ = '2mitrij'


class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ('country', 'region', 'name', 'timezone')
        widgets = {
            'country': forms.Select(attrs={'class': 'form-control'}),
            'region': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'timezone': forms.Select(attrs={'class': 'form-control'}),
        }


class RegionForm(forms.ModelForm):
    class Meta:
        model = Region
        fields = ('name', 'country',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.Select(attrs={'class': 'form-control'}),
        }


class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = ('name', 'code')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
        }
