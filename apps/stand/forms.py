# coding=utf-8
from django import forms
from apps.manager.models import Manager
from apps.moderator.models import Moderator
from .models import Stand

__author__ = 'alexy'


class StandForm(forms.ModelForm):
    """
    Форма добавления/редактирования вёрстки
    """
    class Meta:
        model = Stand
        fields = '__all__'
        widgets = {
            'moderator': forms.HiddenInput(),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'date_start': forms.DateInput(attrs={'class': 'form-control'}),
            'date_end': forms.DateInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(StandForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs:
            instance = kwargs.get('instance')
        else:
            instance = None
        if user:
            if user.type == 1:
                self.fields['moderator'].widget = forms.Select(attrs={'class': 'form-control'})
                self.fields['moderator'].queryset = Moderator.objects.filter(stand_accept=True)
            if not instance:
                if user.type == 2:
                    self.fields['moderator'].initial = user.moderator_user
                elif user.type == 5:
                    self.fields['moderator'].initial = user.manager_user.moderator.moderator_user
