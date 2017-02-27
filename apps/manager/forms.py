# coding=utf-8
from django import forms

from .models import Manager

__author__ = 'alexy'


class ManagerForm(forms.ModelForm):
    class Meta:
        model = Manager
        exclude = ['user', ]
        widgets = {
            'moderator': forms.Select(attrs={'class': 'form-control'}),
        }
