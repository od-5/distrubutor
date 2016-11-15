# coding=utf-8
from django import forms
from .models import Ticket

__author__ = 'Rylcev Alexy'


class TicketAddForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('name', 'mail', 'phone', 'city', 'moderator')


class TicketChangeForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = '__all__'
        widgets = {
            'city': forms.Select(attrs={'class': 'form-control'}),
            'moderator': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'mail': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': 0.01}),
            'comment': forms.Textarea(attrs={'class': 'form-control'}),
        }
