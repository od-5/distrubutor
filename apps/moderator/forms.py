# coding=utf-8
from django import forms

from .models import Moderator, ModeratorArea, ModeratorAction, Review

__author__ = 'alexy'


class ModeratorForm(forms.ModelForm):
    class Meta:
        model = Moderator
        exclude = ['comment', ]
        widgets = {
            'user': forms.HiddenInput(attrs={'class': 'form-control'}),
            'superviser': forms.Select(attrs={'class': 'form-control'}),
            'ticket_forward': forms.CheckboxInput(),
            'deny_access': forms.CheckboxInput(),
            'site_visible': forms.CheckboxInput(),
            'stand_accept': forms.CheckboxInput(),
            'deny_date': forms.DateInput(attrs={'class': 'form-control'}),
            'city': forms.CheckboxSelectMultiple(),
            'company': forms.TextInput(attrs={'class': 'form-control'}),
            'leader': forms.TextInput(attrs={'class': 'form-control'}),
            'leader_function': forms.TextInput(attrs={'class': 'form-control'}),
            'work_basis': forms.TextInput(attrs={'class': 'form-control'}),
            'experience': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'contact': forms.Textarea(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'logotype': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'experience_lang': forms.TextInput(attrs={'class': 'form-control'}),
            'description_lang': forms.Textarea(attrs={'class': 'form-control'}),
            'contact_lang': forms.Textarea(attrs={'class': 'form-control'}),
            'fb_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'http://'}),
            'ok_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'http://'}),
            'vk_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'http://'}),
            'insta_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'http://'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super(ModeratorForm, self).__init__(*args, **kwargs)
        if user.type != 1:
            self.fields['superviser'].widget = forms.HiddenInput()
            self.fields['deny_access'].widget = forms.HiddenInput()
            self.fields['deny_date'].widget = forms.HiddenInput()
            self.fields['site_visible'].widget = forms.HiddenInput()
            self.fields['ticket_forward'].widget = forms.HiddenInput()
            self.fields['stand_accept'].widget = forms.HiddenInput()

    def clean_fb_link(self):
        fb_link = self.cleaned_data.get("fb_link")
        if fb_link and not fb_link.startswith('http://'):
            fb_link = 'http://%s' % fb_link
        return fb_link

    def clean_vk_link(self):
        vk_link = self.cleaned_data.get("vk_link")
        if vk_link and not vk_link.startswith('http://'):
            vk_link = 'http://%s' % vk_link
        return vk_link

    def clean_ok_link(self):
        ok_link = self.cleaned_data.get("ok_link")
        if ok_link and not ok_link.startswith('http://'):
            ok_link = 'http://%s' % ok_link
        return ok_link

    def clean_insta_link(self):
        insta_link = self.cleaned_data.get("insta_link")
        if insta_link and not insta_link.startswith('http://'):
            insta_link = 'http://%s' % insta_link
        return insta_link


class ModeratorAreaForm(forms.ModelForm):
    class Meta:
        model = ModeratorArea
        fields = '__all__'
        widgets = {
            'moderator': forms.HiddenInput(),
            'city': forms.HiddenInput(),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ModeratorActionForm(forms.ModelForm):
    class Meta:
        model = ModeratorAction
        fields = '__all__'
        widgets = {
            'moderator': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'cost': forms.NumberInput(attrs={'class': 'form-control', 'step': 0.01})
        }


class ReviewForm(forms.ModelForm):
    """
    Форма добавления/редактирования отзыва о работе модератора(исполнителя)
    """
    class Meta:
        model = Review
        fields = '__all__'
        widgets = {
            'moderator': forms.HiddenInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'mail': forms.EmailInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': u'Текст сообщения'}),
            'rating': forms.Select(attrs={'class': 'form-control'}),
        }
