# coding=utf-8
from django import forms
from django.core.urlresolvers import reverse
from apps.city.models import City
from .models import Message

__author__ = 'alexy'


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('title', 'text', 'author')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'}),
            'author': forms.HiddenInput(),
        }

    city = forms.ModelChoiceField(
        queryset=City.objects.all(), label=u'Выберите город', required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
