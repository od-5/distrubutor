# coding=utf-8
from betterforms.multiform import MultiModelForm

from django import forms

from core.models import User
from django.db.models import Q

from core.forms import UserAddForm, UserUpdateForm
from .models import Manager

__author__ = 'alexy'


class ManagerForm(forms.ModelForm):
    class Meta:
        model = Manager
        exclude = ['user', ]
        widgets = {
            'moderator': forms.Select(attrs={'class': 'form-control'}),
        }


class ManagerAddForm(ManagerForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ManagerAddForm, self).__init__(*args, **kwargs)

        if user.type == User.UserType.administrator:
            self.fields['moderator'].queryset = User.objects.filter(type=User.UserType.moderator)
        elif user.type == User.UserType.moderator:
            if user.superviser:
                self.fields['moderator'].queryset = User.objects.filter(
                    Q(superviser=user) | Q(moderator_user__superviser=user))
            else:
                self.fields['moderator'].queryset = User.objects.filter(pk=user.pk)
        elif user.type == User.UserType.manager:
            manager = Manager.objects.get(user=user)
            self.fields['moderator'].queryset = User.objects.filter(pk=manager.moderator.pk)


class ManagerUpdateForm(ManagerForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ManagerUpdateForm, self).__init__(*args, **kwargs)

        if user.type == User.UserType.administrator:
            self.fields['moderator'].queryset = User.objects.filter(type=User.UserType.moderator)
        elif user.type == User.UserType.moderator:
            self.fields['moderator'].queryset = User.objects.filter(pk=user.pk)
        elif user.type == User.UserType.manager:
            manager = Manager.objects.get(user=user)
            self.fields['moderator'].queryset = User.objects.filter(pk=manager.moderator.pk)


class ManagerMultiForm(MultiModelForm):
    form_classes = {
        'manager': ManagerAddForm,
        'user': UserAddForm
    }

    def get_form_args_kwargs(self, key, args, kwargs):
        if key != 'manager':
            kwargs.pop('user')

        return super(ManagerMultiForm, self).get_form_args_kwargs(key, args, kwargs)


class ManagerAddMultiForm(ManagerMultiForm):
    form_classes = {
        'manager': ManagerAddForm,
        'user': UserAddForm
    }


class ManagerUpdateMultiForm(ManagerMultiForm):
    form_classes = {
        'manager': ManagerUpdateForm,
        'user': UserUpdateForm
    }
