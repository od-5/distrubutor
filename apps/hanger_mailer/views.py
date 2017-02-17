# coding=utf-8
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.views.generic import ListView, CreateView, UpdateView

from lib.cbv import SendUserToFormMixin
from .models import HangerMail, HangerMailItem
from .forms import HangerMailForm

__author__ = 'alexy'


class HangerMailListView(ListView):
    model = HangerMail
    template_name = 'hanger_mailer/hangermail_list.html'
    paginate_by = 25

    def get_queryset(self):
        user = self.request.user
        if user.type == 2:
            qs = self.model.objects.filter(moderator=user.moderator_user)
        elif user.type == 5:
            qs = self.model.objects.filter(moderator=user.manager_user.moderator.moderator_user)
        else:
            qs = self.model.objects.none()
        return qs


class HangerMailCreateView(CreateView, SendUserToFormMixin):
    model = HangerMail
    form_class = HangerMailForm
    template_name = 'hanger_mailer/hangermail_form.html'


class HangerMailUpdateView(UpdateView, SendUserToFormMixin):
    model = HangerMail
    form_class = HangerMailForm
    template_name = 'hanger_mailer/hangermail_form.html'

    def form_valid(self, form):
        if 'mail_list' in form.cleaned_data:
            mail_list_data = [mail.strip() for mail in form.cleaned_data.get('mail_list').split(',')]
            for i in mail_list_data:
                try:
                    validate_email(i)
                    item = HangerMailItem(hangermail=form.instance, email=i)
                except ValidationError:
                    pass

        return super(HangerMailUpdateView, self).form_valid(form)
