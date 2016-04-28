# coding=utf-8
from django import forms
from core.models import User
from .models import City

__author__ = 'alexy'


class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ('country', 'name')
        widgets = {
            'country': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
    #
    # def __init__(self, *args, **kwargs):
    #     super(CityAddForm, self).__init__(*args, **kwargs)
    #     self.fields['moderator'].queryset = User.objects.filter(type=2)
