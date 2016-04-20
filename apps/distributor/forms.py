# coding=utf-8
from django import forms
from apps.sale.models import Sale
from .models import Distributor, DistributorTask

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
        fields = ['user', 'moderator']
        widgets = {
            'user': forms.HiddenInput(attrs={'class': 'form-control'}),
            'moderator': forms.Select(attrs={'class': 'form-control'}),
        }


class DistributorPaymentForm(forms.ModelForm):
    class Meta:
        model = Distributor
        fields = '__all__'
        widgets = {
            'user': forms.HiddenInput(),
            'moderator': forms.HiddenInput(),
            'distribution_cost': forms.NumberInput(attrs={'class': 'form-control'}),
            'posting_cost': forms.NumberInput(attrs={'class': 'form-control'})
        }


class DistributorTaskForm(forms.ModelForm):
    class Meta:
        model = DistributorTask
        exclude = ['closed', ]
        widgets = {
            'distributor': forms.Select(attrs={'class': 'form-control'}),
            'sale': forms.Select(attrs={'class': 'form-control'}),
            'area': forms.Select(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'material_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        # self.request = kwargs.pop("request")
        user = kwargs.pop("user")
        super(DistributorTaskForm, self).__init__(*args, **kwargs)
        if user.type == 2:
            self.fields['distributor'].queryset = user.moderator_user.distributor_set.all()
            self.fields['sale'].queryset = Sale.objects.filter(moderator=user.moderator_user)
            self.fields['area'].queryset = user.moderator_user.moderatorarea_set.all()
            # self.fields['moderator'].initial = user.moderator_user
            # self.fields['moderator'].widget = forms.HiddenInput()
        # elif user.type == 5:
            # self.fields['city'].queryset = user.manager_user.moderator.moderator_user.city.all()
            # self.fields['manager'].queryset = user.manager_user.moderator.manager_set.all()
            # self.fields['manager'].initial = user.manager_user
            # self.fields['moderator'].initial = user.manager_user.moderator.moderator_user
            # self.fields['moderator'].widget = forms.HiddenInput()


class DistributorTaskUpdateForm(forms.ModelForm):
    class Meta:
        model = DistributorTask
        exclude = ['closed', ]
        widgets = {
            'distributor': forms.Select(attrs={'class': 'form-control'}),
            'sale': forms.Select(attrs={'class': 'form-control'}),
            'area': forms.Select(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'material_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        # self.request = kwargs.pop("request")
        user = kwargs.pop("user")
        super(DistributorTaskUpdateForm, self).__init__(*args, **kwargs)
        if user.type == 2:
            self.fields['distributor'].queryset = user.moderator_user.distributor_set.all()
            self.fields['sale'].queryset = Sale.objects.filter(moderator=user.moderator_user)
            self.fields['area'].queryset = user.moderator_user.moderatorarea_set.all()

        #     self.fields['moderator'].initial = user.moderator_user
        #     self.fields['moderator'].widget = forms.HiddenInput()
        # elif user.type == 5:
        #     self.fields['city'].queryset = user.manager_user.moderator.moderator_user.city.all()
        #     self.fields['manager'].queryset = user.manager_user.moderator.manager_set.all()
        #     self.fields['manager'].initial = user.manager_user
        #     self.fields['moderator'].initial = user.manager_user.moderator.moderator_user
        #     self.fields['moderator'].widget = forms.HiddenInput()
