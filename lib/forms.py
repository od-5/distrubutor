# coding=utf-8
from functools import partial, wraps

from django import forms
from django.forms.formsets import BaseFormSet


class BlockedModelFormMixin(forms.ModelForm):
    """
    Миксин реализует модельную форму, содержимое которой может быть недоступно для редактирования.

    Форма блокируется если в конструктор передан аргумент blocked.
    """
    def __init__(self, *args, **kwargs):
        self.blocked = kwargs.pop('blocked', False)
        if self.blocked:
            kwargs.pop('data', None)
            kwargs.pop('files', None)

        super(BlockedModelFormMixin, self).__init__(*args, **kwargs)

        if self.blocked:
            for field in self.fields.values():
                field.widget.attrs['disabled'] = 'disabled'


class FormKwargsFormsetMixin(BaseFormSet):
    """
    Миксин расширяет функционал наборов форм, позволяя передавать дополнительные аргументы в конструктор форм формсета.

    Аргументы форм необходимо передать в конструктор формсета как аргумент form_kwargs в виде словаря.
    P.S. реализовано в Django 1.9.
    """
    def __init__(self, *args, **kwargs):
        form_kwargs = kwargs.pop('form_kwargs', None)
        if form_kwargs is not None:
            self.form = wraps(self.form)(partial(self.form, **form_kwargs))

        super(FormKwargsFormsetMixin, self).__init__(*args, **kwargs)
