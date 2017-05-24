# coding=utf-8
from django import forms

from .models import Section, Topic, Comment

__author__ = 'alexy'


class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ('author', 'title', 'description')
        widgets = {
            'author': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = (
            'section',
            'author',
            'title',
            'text',
            'all_city',
            'moderator',
            'leader',
            'manager',
            'distributor',
            'city'
        )
        widgets = {
            'section': forms.HiddenInput(),
            'author': forms.HiddenInput(),
            'city': forms.CheckboxSelectMultiple(),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'all_city': forms.CheckboxInput(),
            'moderator': forms.CheckboxInput(),
            'leader': forms.CheckboxInput(),
            'manager': forms.CheckboxInput(),
            'distributor': forms.CheckboxInput(),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'topic', 'text')
        widgets = {
            'author': forms.HiddenInput(),
            'topic': forms.HiddenInput()
        }
