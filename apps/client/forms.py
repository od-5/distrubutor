# coding=utf-8
from django import forms
from core.models import User
from .models import Client, Task, ClientContact

__author__ = 'alexy'


class ClientAddForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
        exclude = ['type', ]
        widgets = {
            'moderator': forms.Select(attrs={'class': 'form-control'}),
            'manager': forms.Select(attrs={'class': 'form-control'}),
            'city': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'kind_of_activity': forms.TextInput(attrs={'class': 'form-control'}),
            'actual_address': forms.TextInput(attrs={'class': 'form-control'}),
            'site': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        # self.request = kwargs.pop("request")
        user = kwargs.pop("user")
        super(ClientAddForm, self).__init__(*args, **kwargs)
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

    def clean_name(self):
        data = self.cleaned_data
        try:
            Client.objects.get(name=data['name'])
        except Client.DoesNotExist:
            return data['name']
        raise forms.ValidationError(u'Клиент с таким названием уже есть в системе')


class ClientUpdateForm(forms.ModelForm):
    class Meta:
        model = Client
        exclude = ['type', ]
        widgets = {
            'moderator': forms.Select(attrs={'class': 'form-control'}),
            'manager': forms.Select(attrs={'class': 'form-control'}),
            'city': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'kind_of_activity': forms.TextInput(attrs={'class': 'form-control'}),
            'actual_address': forms.TextInput(attrs={'class': 'form-control'}),
            'site': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        # self.request = kwargs.pop("request")
        user = kwargs.pop("user")
        super(ClientUpdateForm, self).__init__(*args, **kwargs)
        if user.type == 2:
            self.fields['city'].queryset = user.moderator_user.city.all()
            self.fields['manager'].queryset = user.manager_set.all()
            self.fields['moderator'].initial = user.moderator_user
            # self.fields['moderator'].widget = forms.HiddenInput()
        elif user.type == 5:
            self.fields['city'].queryset = user.manager_user.moderator.moderator_user.city.all()
            self.fields['manager'].queryset = user.manager_user.moderator.manager_set.all()
            # self.fields['manager'].initial = user.manager_user
            self.fields['moderator'].initial = user.manager_user.moderator.moderator_user
            # self.fields['moderator'].widget = forms.HiddenInput()


class ClientContactForm(forms.ModelForm):
    class Meta:
        model = ClientContact
        fields = '__all__'
        widgets = {
            'client': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'function': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'})
        }


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
        widgets = {
            'manager': forms.Select(attrs={'class': 'form-control'}),
            'client': forms.Select(attrs={'class': 'form-control'}),
            'clientcontact': forms.Select(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'placeholder': u'Текст комментария к задаче'}),
            'status': forms.HiddenInput(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        # self.request = kwargs.pop("request")
        user = kwargs.pop("user")
        super(TaskForm, self).__init__(*args, **kwargs)
        if user.type == 2:
            self.fields['manager'].queryset = user.manager_set.all()
            self.fields['client'].queryset = user.moderator_user.client_set.all()
        elif user.type == 5:
            self.fields['client'].queryset = user.manager_user.moderator.moderator_user.client_set.all()
            self.fields['manager'].queryset = user.manager_user.moderator.manager_set.all()
            self.fields['manager'].initial = user.manager_user
