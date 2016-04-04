# coding=utf-8
from django import forms
from django.contrib.admin.widgets import ManyToManyRawIdWidget
from .models import Moderator

__author__ = 'alexy'


class ModeratorForm(forms.ModelForm):
    class Meta:
        model = Moderator
        fields = '__all__'
        widgets = {
            'moderator': forms.HiddenInput(attrs={'class': 'form-control'}),
            'city': forms.CheckboxSelectMultiple(),
            'company': forms.TextInput(attrs={'class': 'form-control'}),
            'leader': forms.TextInput(attrs={'class': 'form-control'}),
            'leader_function': forms.TextInput(attrs={'class': 'form-control'}),
            'work_basis': forms.TextInput(attrs={'class': 'form-control'}),
        }
