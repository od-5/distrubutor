# coding=utf-8
from django import forms
from .models import Distributor

__author__ = 'alexy'


class DistributorAddForm(forms.ModelForm):
    class Meta:
        model = Distributor
        exclude = ['user', ]
        widgets = {
            'moderator': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super(DistributorAddForm, self).__init__(*args, **kwargs)
        if user.type == 2:
            self.fields['moderator'].initial = user.moderator_user
            # self.fields['moderator'].widget = forms.HiddenInput()
        elif user.type == 5:
            self.fields['moderator'].initial = user.manager_user.moderator.moderator_user
            # self.fields['moderator'].widget = forms.HiddenInput()


class DistributorUpdateForm(forms.ModelForm):
    class Meta:
        model = Distributor
        fields = '__all__'
        widgets = {
            'user': forms.HiddenInput(attrs={'class': 'form-control'}),
            'moderator': forms.Select(attrs={'class': 'form-control'}),
        }
