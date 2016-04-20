# coding=utf-8
from django import forms
from django.contrib.admin.widgets import ManyToManyRawIdWidget
from .models import Moderator, ModeratorArea

__author__ = 'alexy'


class ModeratorForm(forms.ModelForm):
    class Meta:
        model = Moderator
        fields = '__all__'
        widgets = {
            'user': forms.HiddenInput(attrs={'class': 'form-control'}),
            'city': forms.CheckboxSelectMultiple(),
            'company': forms.TextInput(attrs={'class': 'form-control'}),
            'leader': forms.TextInput(attrs={'class': 'form-control'}),
            'leader_function': forms.TextInput(attrs={'class': 'form-control'}),
            'work_basis': forms.TextInput(attrs={'class': 'form-control'}),
            'experience': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'contact': forms.Textarea(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'logotype': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class ModeratorAreaForm(forms.ModelForm):
    class Meta:
        model = ModeratorArea
        fields = '__all__'
        widgets = {
            'moderator': forms.HiddenInput(),
            'city': forms.HiddenInput(),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
