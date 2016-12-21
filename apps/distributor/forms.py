# coding=utf-8
from django import forms
from apps.sale.models import Sale
from .models import Distributor, DistributorTask, DistributorPayment, GPSPoint

__author__ = 'alexy'


class DistributorAddForm(forms.ModelForm):
    class Meta:
        model = Distributor
        fields = ['moderator', ]
        widgets = {
            'moderator': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super(DistributorAddForm, self).__init__(*args, **kwargs)
        if user.type == 2:
            self.fields['moderator'].initial = user.moderator_user
        elif user.type == 5:
            self.fields['moderator'].initial = user.manager_user.moderator.moderator_user


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
        model = DistributorPayment
        fields = '__all__'
        widgets = {
            'distributor': forms.HiddenInput(),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'cost': forms.NumberInput(attrs={'class': 'form-control'})
        }


class DistributorTaskForm(forms.ModelForm):
    class Meta:
        model = DistributorTask
        exclude = ['closed', 'type']
        widgets = {
            'distributor': forms.Select(attrs={'class': 'form-control'}),
            'sale': forms.Select(attrs={'class': 'form-control'}),
            'order': forms.Select(attrs={'class': 'form-control'}),
            'area': forms.Select(attrs={'class': 'form-control'}),
            'material_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control'}),
            'define_address': forms.CheckboxInput(),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super(DistributorTaskForm, self).__init__(*args, **kwargs)
        if user.type == 1:
            self.fields['distributor'].queryset = Distributor.objects.filter(user__is_active=True)
        elif user.type == 2:
            self.fields['distributor'].queryset = user.moderator_user.distributor_set.filter(user__is_active=True)
            self.fields['sale'].queryset = Sale.objects.filter(moderator=user.moderator_user)
            self.fields['area'].queryset = user.moderator_user.moderatorarea_set.all()


class DistributorTaskUpdateForm(forms.ModelForm):
    class Meta:
        model = DistributorTask
        exclude = ['type']
        widgets = {
            'distributor': forms.Select(attrs={'class': 'form-control'}),
            'sale': forms.Select(attrs={'class': 'form-control'}),
            'order': forms.Select(attrs={'class': 'form-control'}),
            'area': forms.Select(attrs={'class': 'form-control'}),
            'material_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control'}),
            'define_address': forms.CheckboxInput(),
            'closed': forms.CheckboxInput(),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super(DistributorTaskUpdateForm, self).__init__(*args, **kwargs)
        if user.type == 1:
            self.fields['distributor'].queryset = Distributor.objects.filter(user__is_active=True)
        elif user.type == 2:
            self.fields['distributor'].queryset = user.moderator_user.distributor_set.filter(user__is_active=True)
            self.fields['sale'].queryset = Sale.objects.filter(moderator=user.moderator_user)
            self.fields['area'].queryset = user.moderator_user.moderatorarea_set.all()


class GPSPointUpdateForm(forms.ModelForm):
    class Meta:
        model = GPSPoint
        fields = '__all__'
        widgets = {
            'task': forms.HiddenInput(),
            'name': forms.HiddenInput(),
            'count': forms.NumberInput(attrs={'class': 'form-control', 'step': '1'}),
            'comment': forms.HiddenInput(),
            'coord_x': forms.HiddenInput(),
            'coord_y': forms.HiddenInput(),
            'timestamp': forms.HiddenInput()
        }
