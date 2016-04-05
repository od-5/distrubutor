# coding=utf-8
from django import forms
from apps.city.models import City
from .models import Sale
from apps.manager.models import Manager
from core.models import User

__author__ = 'alexy'


class SaleAddForm(forms.ModelForm):
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
            self.fields['city'].queryset = user.moderator.city.all()
            self.fields['manager'].queryset = user.manager_set.all()
            self.fields['moderator'].initial = user.moderator
            self.fields['moderator'].widget = forms.HiddenInput()
        elif user.type == 5:
            self.fields['city'].queryset = user.manager_user.moderator.moderator.city.all()
            self.fields['manager'].queryset = user.manager_user.moderator.manager_set.all()
            self.fields['moderator'].initial = user.manager_user.moderator.moderator
            self.fields['moderator'].widget = forms.HiddenInput()

        # if self.request.user:
        #     if self.request.user.type == 2:
        #         self.fields['city'].queryset = City.objects.filter(moderator=self.request.user)
        #     elif self.request.user.type == 5 and self.request.user.is_leader_manager():
        #         manager = Manager.objects.get(user=self.request.user)
        #         self.fields['city'].queryset = City.objects.filter(moderator=manager.moderator)


class SaleUpdateForm(forms.ModelForm):
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
            self.fields['city'].queryset = user.moderator.city.all()
            self.fields['manager'].queryset = user.manager_set.all()
            self.fields['moderator'].widget = forms.HiddenInput()
        elif user.type == 5:
            self.fields['city'].queryset = user.manager_user.moderator.moderator.city.all()
            self.fields['manager'].queryset = user.manager_user.moderator.manager_set.all()
            self.fields['moderator'].widget = forms.HiddenInput()
    # def __init__(self, *args, **kwargs):
    #     self.request = kwargs.pop("request")
    #     super(SaleUpdateForm, self).__init__(*args, **kwargs)
    #     if self.request.user:
    #         if self.request.user.type == 2:
    #             self.fields['city'].queryset = City.objects.filter(moderator=self.request.user)
    #             self.fields['manager'].queryset = Manager.objects.filter(moderator=self.request.user)
    #         elif self.request.user.type == 5 and self.request.user.is_leader_manager():
    #             manager = Manager.objects.get(user=self.request.user)
    #             self.fields['city'].queryset = City.objects.filter(moderator=manager.moderator)
    #             self.fields['manager'].queryset = Manager.objects.filter(moderator=manager.moderator)



#
#
# class ClientMaketForm(forms.ModelForm):
#     class Meta:
#         model = ClientMaket
#         fields = ('client', 'name', 'file', 'date')
#         widgets = {
#             'client': forms.HiddenInput(attrs={'class': 'form-control'}),
#             'name': forms.TextInput(attrs={'class': 'form-control'}),
#             'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
#             'date': forms.DateInput(attrs={'class': 'form-control'}),
#         }
#
#
# class ClientOrderForm(forms.ModelForm):
#     class Meta:
#         model = ClientOrder
#         fields = ('client', 'date_start', 'date_end')
#         widgets = {
#             'client': forms.HiddenInput(attrs={'class': 'form-control'}),
#             'date_start': forms.DateInput(attrs={'class': 'form-control'}),
#             'date_end': forms.DateInput(attrs={'class': 'form-control'}),
#         }
#
#
# class ClientJournalForm(forms.ModelForm):
#     class Meta:
#         model = ClientJournal
#         fields = ('client', 'clientorder', 'cost', 'add_cost', 'discount')
#         widgets = {
#             'client': forms.HiddenInput(attrs={'class': 'form-control'}),
#             'clientorder': forms.CheckboxSelectMultiple(),
#             'cost': forms.TextInput(attrs={'class': 'form-control'}),
#             'add_cost': forms.TextInput(attrs={'class': 'form-control'}),
#             'discount': forms.TextInput(attrs={'class': 'form-control'}),
#         }
#
