# coding=utf-8
from django.core.urlresolvers import reverse
from django.views.generic import CreateView, UpdateView, ListView

from lib.cbv import RedirectlessFormMixin

from core.forms import UserAddForm, UserUpdateForm
from core.models import User

__author__ = 'alexy'


class AdministratorListView(ListView):
    queryset = User.objects.filter(type=1)
    template_name = 'administrator/administrator_list.html'
    paginate_by = 50

    def get_queryset(self):
        qs = User.objects.filter(type=1)
        if self.request.GET.get('email'):
            qs = qs.filter(email=self.request.GET.get('email'))
        if self.request.GET.get('last_name'):
            qs = qs.filter(last_name=self.request.GET.get('last_name'))
        if self.request.GET.get('first_name'):
            qs = qs.filter(first_name=self.request.GET.get('first_name'))
        if self.request.GET.get('patronymic'):
            qs = qs.filter(patronymic=self.request.GET.get('patronymic'))
        if self.request.GET.get('phone'):
            qs = qs.filter(phone=self.request.GET.get('phone'))
        return qs

    def get_context_data(self, **kwargs):
        context = super(AdministratorListView, self).get_context_data(**kwargs)
        context.update({
            'r_email': self.request.GET.get('email', ''),
            'r_last_name': self.request.GET.get('last_name', ''),
            'r_first_name': self.request.GET.get('first_name', ''),
            'r_patronymic': self.request.GET.get('patronymic', ''),
            'r_phone': self.request.GET.get('phone', '')
        })
        return context


class AdministratorCreateView(CreateView):
    form_class = UserAddForm
    template_name = 'administrator/administrator_add.html'

    def get_success_url(self):
        return reverse('administrator:update', args=(self.object.pk,))

    def form_valid(self, form):
        form.instance.type = 1
        form.instance.is_superuser = True
        form.instance.is_staff = True
        form.instance.is_active = True
        return super(AdministratorCreateView, self).form_valid(form)


class AdministratorUpdateView(RedirectlessFormMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'administrator/administrator_update.html'
