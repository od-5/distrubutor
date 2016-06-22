# coding=utf-8
from django import forms
from .models import Sale, SaleOrder, SaleMaket

__author__ = 'alexy'


class SaleAddForm(forms.ModelForm):
    """
    Форма добавления новой продажи
    """
    class Meta:
        model = Sale
        exclude = ['user', ]
        widgets = {
            'moderator': forms.Select(attrs={'class': 'form-control'}),
            'city': forms.Select(attrs={'class': 'form-control'}),
            'manager': forms.Select(attrs={'class': 'form-control'}),
            'legal_name': forms.TextInput(attrs={'class': 'form-control'}),
            'actual_name': forms.TextInput(attrs={'class': 'form-control'}),
            'inn': forms.TextInput(attrs={'class': 'form-control'}),
            'kpp': forms.TextInput(attrs={'class': 'form-control'}),
            'ogrn': forms.TextInput(attrs={'class': 'form-control'}),
            'bank': forms.TextInput(attrs={'class': 'form-control'}),
            'bik': forms.TextInput(attrs={'class': 'form-control'}),
            'account': forms.TextInput(attrs={'class': 'form-control'}),
            'account_cor': forms.TextInput(attrs={'class': 'form-control'}),
            'signer_post_dec': forms.TextInput(attrs={'class': 'form-control'}),
            'signer_name_dec': forms.TextInput(attrs={'class': 'form-control'}),
            'signer_doc_dec': forms.TextInput(attrs={'class': 'form-control'}),
            'legal_address': forms.TextInput(attrs={'class': 'form-control'}),
            'leader': forms.TextInput(attrs={'class': 'form-control'}),
            'leader_function': forms.TextInput(attrs={'class': 'form-control'}),
            'work_basis': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        # self.request = kwargs.pop("request")
        user = kwargs.pop("user")
        super(SaleAddForm, self).__init__(*args, **kwargs)
        if user.type == 2:
            self.fields['city'].queryset = user.moderator_user.city.all()
            self.fields['manager'].queryset = user.manager_set.all()
            self.fields['moderator'].initial = user.moderator_user
            self.fields['moderator'].widget = forms.HiddenInput()
        elif user.type == 5:
            self.fields['city'].queryset = user.manager_user.moderator.moderator_user.city.all()
            self.fields['manager'].queryset = user.manager_user.moderator.manager_set.all()
            self.fields['manager'].initial = user.manager_user
            self.fields['moderator'].initial = user.manager_user.moderator.moderator_user
            self.fields['moderator'].widget = forms.HiddenInput()


class SaleUpdateForm(forms.ModelForm):
    """
    Форма редактирования продажи
    """
    class Meta:
        model = Sale
        exclude = []
        widgets = {
            'user': forms.HiddenInput(),
            'moderator': forms.Select(attrs={'class': 'form-control'}),
            'city': forms.Select(attrs={'class': 'form-control'}),
            'manager': forms.Select(attrs={'class': 'form-control'}),
            'legal_name': forms.TextInput(attrs={'class': 'form-control'}),
            'actual_name': forms.TextInput(attrs={'class': 'form-control'}),
            'inn': forms.TextInput(attrs={'class': 'form-control'}),
            'kpp': forms.TextInput(attrs={'class': 'form-control'}),
            'ogrn': forms.TextInput(attrs={'class': 'form-control'}),
            'bank': forms.TextInput(attrs={'class': 'form-control'}),
            'bik': forms.TextInput(attrs={'class': 'form-control'}),
            'account': forms.TextInput(attrs={'class': 'form-control'}),
            'account_cor': forms.TextInput(attrs={'class': 'form-control'}),
            'signer_post_dec': forms.TextInput(attrs={'class': 'form-control'}),
            'signer_name_dec': forms.TextInput(attrs={'class': 'form-control'}),
            'signer_doc_dec': forms.TextInput(attrs={'class': 'form-control'}),
            'legal_address': forms.TextInput(attrs={'class': 'form-control'}),
            'leader': forms.TextInput(attrs={'class': 'form-control'}),
            'leader_function': forms.TextInput(attrs={'class': 'form-control'}),
            'work_basis': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super(SaleUpdateForm, self).__init__(*args, **kwargs)
        if user.type == 2:
            self.fields['city'].queryset = user.moderator_user.city.all()
            self.fields['manager'].queryset = user.manager_set.all()
            self.fields['moderator'].widget = forms.HiddenInput()
        elif user.type == 5:
            self.fields['city'].queryset = user.manager_user.moderator.moderator_user.city.all()
            self.fields['manager'].queryset = user.manager_user.moderator.manager_set.all()
            self.fields['moderator'].widget = forms.HiddenInput()


class SaleOrderForm(forms.ModelForm):
    """
    Форма добавления/редактирования заказа по продаже
    """
    class Meta:
        model = SaleOrder
        fields = '__all__'
        widgets = {
            'sale': forms.HiddenInput(attrs={'class': 'form-control'}),
            'date_start': forms.DateInput(attrs={'class': 'form-control'}),
            'date_end': forms.DateInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'count': forms.NumberInput(attrs={'class': 'form-control'}),
            'cost': forms.NumberInput(attrs={'class': 'form-control'}),
            'add_cost': forms.NumberInput(attrs={'class': 'form-control'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control'}),
            'closed': forms.CheckboxInput(),
        }


class SaleMaketForm(forms.ModelForm):
    """
    Форма добавления/редактирования макета рекламы по продаже
    """
    class Meta:
        model = SaleMaket
        fields = ('sale', 'name', 'file', 'date')
        widgets = {
            'sale': forms.HiddenInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control'}),
        }
