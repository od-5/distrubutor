# coding=utf-8
from django import forms

from .models import HangerMail

__author__ = 'alexy'


class HangerMailForm(forms.ModelForm):
    """
    Форма добавления/редактирования рассылки
    """
    class Meta:
        model = HangerMail
        fields = '__all__'
        widgets = {
            'moderator': forms.HiddenInput(),
            'city': forms.Select(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': 1}),
            'count': forms.NumberInput(attrs={'class': 'form-control', 'step': 1}),
        }

    mail_list = forms.CharField(
        label=u'Введите список адресов через запятую',
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': u'mail1@test.ru, mail2@test.ru, и т.д.'}),
        required=False
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(HangerMailForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs:
            instance = kwargs.get('instance')
        else:
            self.fields['mail_list'].widget = forms.HiddenInput()
            instance = None
        if user:
            if user.type == 2:
                self.fields['city'].queryset = user.moderator_user.city.all()
            elif user.type == 5:
                self.fields['city'].initial = user.manager_user.moderator.moderator_user
            if not instance:
                if user.type == 2:
                    self.fields['moderator'].initial = user.moderator_user
                elif user.type == 5:
                    self.fields['moderator'].initial = user.manager_user.moderator.moderator_user