# coding=utf-8
from django.forms import ModelForm, TextInput, Select, DateInput, HiddenInput
from core.models import User
from .models import City

__author__ = 'alexy'


class CityForm(ModelForm):
    class Meta:
        model = City
        fields = ('name',)
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
        }
    #
    # def __init__(self, *args, **kwargs):
    #     super(CityAddForm, self).__init__(*args, **kwargs)
    #     self.fields['moderator'].queryset = User.objects.filter(type=2)
