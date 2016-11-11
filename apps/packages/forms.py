# coding=utf-8
from django import forms
from .models import Package

__author__ = 'alexy'


class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'month': forms.Select(attrs={'class': 'form-control'}),
            'cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'discount': forms.TextInput(attrs={'class': 'form-control'}),
        }
