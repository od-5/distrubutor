# coding=utf-8
from django import forms
from django.core.urlresolvers import reverse
from apps.city.models import City
from .models import Message, UserMessageAnswer

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


class UserMessageAnswerForm(forms.ModelForm):
    class Meta:
        model = UserMessageAnswer
        fields = ('usermessage', 'author', 'recipient', 'text')
        widgets = {
            'author': forms.TextInput(),
            'recipient': forms.TextInput(),
            'usermessage': forms.TextInput(),
            'text': forms.Textarea(attrs={'class': 'form-control'}),

        }
