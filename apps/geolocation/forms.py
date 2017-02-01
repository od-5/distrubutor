# coding=utf-8
from django import forms

from .models import City, Country

__author__ = '2mitrij'


class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ('country', 'name', 'timezone')
        widgets = {
            'country': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'timezone': forms.Select(attrs={'class': 'form-control'}),
        }
    #
    # def __init__(self, *args, **kwargs):
    #     super(CityAddForm, self).__init__(*args, **kwargs)
    #     self.fields['moderator'].queryset = User.objects.filter(type=2)


class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = ('name', 'code')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
        }
