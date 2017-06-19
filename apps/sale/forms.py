# coding=utf-8
from nested_formset import nestedformset_factory
from betterforms.multiform import MultiModelForm

from django import forms
from django.forms.models import inlineformset_factory, BaseInlineFormSet

from lib.forms import BlockedModelFormMixin, FormKwargsFormsetMixin, FormKwargsNestedFormsetMixin
from apps.manager.models import Manager
from core.models import User
from core.forms import UserAddForm
from .models import Sale, SaleOrder, SaleMaket, Questionary, QuestionaryQuestion, QuestionaryAnswer

__author__ = 'alexy'


class SaleAddForm(forms.ModelForm):
    """
    Форма добавления новой продажи
    """
    class Meta:
        model = Sale
        exclude = ['user', 'password']
        widgets = {
            'presale': forms.HiddenInput(),
            'moderator': forms.Select(attrs={'class': 'form-control'}),
            'city': forms.Select(attrs={'class': 'form-control'}),
            'manager': forms.Select(attrs={'class': 'form-control'}),
            'phone_sms': forms.TextInput(attrs={'class': 'form-control'}),
            'sender_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'legal_name': forms.TextInput(attrs={'class': 'form-control'}),
            'actual_name': forms.TextInput(attrs={'class': 'form-control'}),
            'inn': forms.TextInput(attrs={'class': 'form-control'}),
            'kpp': forms.TextInput(attrs={'class': 'form-control'}),
            'ogrn': forms.TextInput(attrs={'class': 'form-control'}),
            'bank': forms.TextInput(attrs={'class': 'form-control'}),
            'bik': forms.TextInput(attrs={'class': 'form-control'}),
            'account': forms.TextInput(attrs={'class': 'form-control'}),
            'account_cor': forms.TextInput(attrs={'class': 'form-control'}),
            'signer_post_dec': forms.TextInput(attrs={'class': 'form-control'}),
            'signer_name_dec': forms.TextInput(attrs={'class': 'form-control'}),
            'signer_doc_dec': forms.TextInput(attrs={'class': 'form-control'}),
            'legal_address': forms.TextInput(attrs={'class': 'form-control'}),
            'leader': forms.TextInput(attrs={'class': 'form-control'}),
            'leader_function': forms.TextInput(attrs={'class': 'form-control'}),
            'work_basis': forms.TextInput(attrs={'class': 'form-control'}),
            'hide_empty_point': forms.CheckboxInput(),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super(SaleAddForm, self).__init__(*args, **kwargs)

        if user.type == User.UserType.administrator:
            self.fields['manager'].queryset = Manager.objects.filter(user__is_active=True)
        elif user.type == User.UserType.moderator:
            self.fields['city'].queryset = user.moderator_user.city.all()
            self.fields['manager'].queryset = user.manager_set.filter(user__is_active=True)
            self.fields['moderator'].initial = user.moderator_user
            self.fields['moderator'].widget = forms.HiddenInput()
        elif user.type == User.UserType.manager:
            self.fields['city'].queryset = user.manager_user.moderator.moderator_user.city.all()
            self.fields['manager'].queryset = user.manager_user.moderator.manager_set.filter(user__is_active=True)
            self.fields['manager'].initial = user.manager_user
            self.fields['moderator'].initial = user.manager_user.moderator.moderator_user
            self.fields['moderator'].widget = forms.HiddenInput()


class SaleAddMultiForm(MultiModelForm):
    """
    Составная форма добавления новой продажи
    """
    form_classes = {
        'sale': SaleAddForm,
        'user': UserAddForm
    }

    def get_form_args_kwargs(self, key, args, kwargs):
        if key != 'sale':
            kwargs.pop('user')

        return super(SaleAddMultiForm, self).get_form_args_kwargs(key, args, kwargs)


class SaleUpdateForm(forms.ModelForm):
    """
    Форма редактирования продажи
    """
    class Meta:
        model = Sale
        exclude = ['password', ]
        widgets = {
            'user': forms.HiddenInput(),
            'moderator': forms.Select(attrs={'class': 'form-control'}),
            'city': forms.Select(attrs={'class': 'form-control'}),
            'manager': forms.Select(attrs={'class': 'form-control'}),
            'phone_sms': forms.TextInput(attrs={'class': 'form-control'}),
            'sender_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'legal_name': forms.TextInput(attrs={'class': 'form-control'}),
            'actual_name': forms.TextInput(attrs={'class': 'form-control'}),
            'inn': forms.TextInput(attrs={'class': 'form-control'}),
            'kpp': forms.TextInput(attrs={'class': 'form-control'}),
            'ogrn': forms.TextInput(attrs={'class': 'form-control'}),
            'bank': forms.TextInput(attrs={'class': 'form-control'}),
            'bik': forms.TextInput(attrs={'class': 'form-control'}),
            'account': forms.TextInput(attrs={'class': 'form-control'}),
            'account_cor': forms.TextInput(attrs={'class': 'form-control'}),
            'signer_post_dec': forms.TextInput(attrs={'class': 'form-control'}),
            'signer_name_dec': forms.TextInput(attrs={'class': 'form-control'}),
            'signer_doc_dec': forms.TextInput(attrs={'class': 'form-control'}),
            'legal_address': forms.TextInput(attrs={'class': 'form-control'}),
            'leader': forms.TextInput(attrs={'class': 'form-control'}),
            'leader_function': forms.TextInput(attrs={'class': 'form-control'}),
            'work_basis': forms.TextInput(attrs={'class': 'form-control'}),
            'hide_empty_point': forms.CheckboxInput()
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super(SaleUpdateForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs:
            sale = kwargs['instance']
            self.fields['manager'].queryset = sale.moderator.user.manager_set.filter(user__is_active=True)
        else:
            sale = None
        if user.type == User.UserType.administrator:
            if not sale:
                self.fields['manager'].queryset = Manager.objects.filter(user__is_active=True)
        elif user.type == User.UserType.moderator:
            if not sale:
                self.fields['manager'].queryset = user.manager_set.filter(user__is_active=True)
            self.fields['city'].queryset = user.moderator_user.city.all()
            self.fields['moderator'].widget = forms.HiddenInput()
        elif user.type == User.UserType.manager:
            if not sale:
                self.fields['manager'].queryset = user.manager_user.moderator.manager_set.filter(user__is_active=True)
            self.fields['city'].queryset = user.manager_user.moderator.moderator_user.city.all()
            self.fields['moderator'].widget = forms.HiddenInput()


class SaleOrderForm(forms.ModelForm):
    """
    Форма добавления/редактирования заказа по продаже
    """
    class Meta:
        model = SaleOrder
        fields = '__all__'
        widgets = {
            'sale': forms.HiddenInput(attrs={'class': 'form-control'}),
            'date_start': forms.DateInput(attrs={'class': 'form-control'}),
            'date_end': forms.DateInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'count': forms.NumberInput(attrs={'class': 'form-control'}),
            'cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'full_cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'add_cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'closed': forms.CheckboxInput(),
            'questionary': forms.Select(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(SaleOrderForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['type'].queryset = self.instance.sale.moderator.moderatoraction_set.all()
            self.fields['questionary'].queryset = self.instance.sale.questionary_set.all()
        else:
            if 'initial' in kwargs and 'sale' in kwargs['initial']:
                self.fields['type'].queryset = kwargs['initial']['sale'].moderator.moderatoraction_set.all()
                self.fields['questionary'].queryset = kwargs['initial']['sale'].questionary_set.all()


class SaleMaketForm(forms.ModelForm):
    """
    Форма добавления/редактирования макета рекламы по продаже
    """
    class Meta:
        model = SaleMaket
        fields = ('sale', 'name', 'file', 'date')
        widgets = {
            'sale': forms.HiddenInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control'}),
        }


class SaleQuestionaryCreateForm(forms.ModelForm):
    class Meta:
        model = Questionary
        fields = ('title', 'sale')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'sale': forms.HiddenInput(),
        }


class BaseSaleQuestionaryAnswerFormset(BaseInlineFormSet, FormKwargsFormsetMixin):
    @property
    def empty_form(self):
        form = super(BaseSaleQuestionaryAnswerFormset, self).empty_form
        form.prefix = self.add_prefix('__answer_prefix__')
        return form


SaleQuestionaryAnswerFormset = inlineformset_factory(
    QuestionaryQuestion, QuestionaryAnswer,
    formset=BaseSaleQuestionaryAnswerFormset,
    form=BlockedModelFormMixin,
    fields=('text',),
    widgets={
        'text': forms.Textarea(attrs={'class': 'form-control', 'rows': '2', 'placeholder': 'введите текст ответа'}),
    },
    can_delete=True,
    extra=0
)


class QuestionaryQuestionForm(BlockedModelFormMixin):
    class Meta:
        model = QuestionaryQuestion
        fields = ('text', 'question_type',)

    def clean(self):
        super(QuestionaryQuestionForm, self).clean()
        if self.is_bound and not self.is_valid():
            return
        if (self.cleaned_data['question_type'] == QuestionaryQuestion.QUESTION_TYPE_CHOICE[1][0] and
                self.nested.is_bound and (self.nested.total_form_count() - len(self.nested.deleted_forms)) == 0):
            raise forms.ValidationError(u'Заполните список ответов!')


class BaseSaleQuestionaryQuestionFormset(FormKwargsNestedFormsetMixin):
    def clean(self):
        if self.is_bound and (self.total_form_count() - len(self.deleted_forms)) == 0:
            raise forms.ValidationError(u'Заполните список вопросов!')
        super(BaseSaleQuestionaryQuestionFormset, self).clean()


SaleQuestionaryQuestionFormset = nestedformset_factory(
    Questionary, QuestionaryQuestion,
    formset=BaseSaleQuestionaryQuestionFormset,
    nested_formset=SaleQuestionaryAnswerFormset,
    form=QuestionaryQuestionForm,
    fields=('text', 'question_type',),
    widgets={
        'text': forms.Textarea(attrs={'class': 'form-control', 'rows': '2', 'placeholder': 'введите текст вопроса'}),
        'question_type': forms.RadioSelect()
    },
    can_delete=True,
    extra=0
)


class SaleQuestionaryUpdateForm(SaleQuestionaryCreateForm, BlockedModelFormMixin):
    def __init__(self, *args, **kwargs):
        super(SaleQuestionaryUpdateForm, self).__init__(*args, **kwargs)
        self.question_formset = SaleQuestionaryQuestionFormset(
            instance=self.instance, data=self.data or None, form_kwargs={'blocked': self.blocked})

    def save(self, commit=True):
        result = super(SaleQuestionaryUpdateForm, self).save(commit)
        self.question_formset.save(commit)
        return result

    def clean(self):
        if self.question_formset.is_bound and not self.question_formset.is_valid():
            raise forms.ValidationError(u'Проверьте правильность заполнения содержимого анкеты!')
        super(SaleQuestionaryUpdateForm, self).clean()
