# coding=utf-8
from django import forms

from .models import Section, Topic, Comment

__author__ = 'alexy'


class SectionAddForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ('author', 'title', 'description')
        widgets = {
            'author': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super(SectionAddForm, self).__init__(*args, **kwargs)
        self.fields['author'].initial = user


class SectionUpdateForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ('author', 'title', 'description')
        widgets = {
            'author': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }


class TopicAddForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = (
            'section',
            'author', 'title',
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
            'superviser': forms.CheckboxInput(),
            'moderator': forms.CheckboxInput(),
            'leader': forms.CheckboxInput(),
            'manager': forms.CheckboxInput(),
            'distributor': forms.CheckboxInput(),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super(TopicAddForm, self).__init__(*args, **kwargs)
        self.fields['author'].initial = user


class TopicUpdateForm(forms.ModelForm):
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


class CommentAddForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'topic', 'text')
        widgets = {
            'author': forms.HiddenInput(),
            'topic': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        topic = kwargs.pop("topic")
        super(CommentAddForm, self).__init__(*args, **kwargs)
        self.fields['author'].initial = user
        self.fields['topic'].initial = topic


class CommentUpdateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'topic', 'text')
        widgets = {
            'author': forms.HiddenInput(),
            'topic': forms.HiddenInput()
        }
