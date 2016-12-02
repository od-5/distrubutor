# coding=utf-8
from django.contrib.auth.decorators import login_required
from .decorators import administrator_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import UpdateView, ListView
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


@administrator_required
def administrator_add(request):
    context = {}
    if request.method == "POST":
        form = UserAddForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.type = 1
            user.is_superuser = True
            user.is_staff = True
            user.is_active = True
            user.save()
            return HttpResponseRedirect(reverse('administrator:update', args=(user.id,)))
        else:
            context.update({
                'error': u'Проверьте правильность ввода полей'
            })
    else:
        form = UserAddForm()
    context.update({
        'form': form,
    })
    return render(request, 'administrator/administrator_add.html', context)


@administrator_required
def administrator_update(request, pk):
    context = {}
    user = User.objects.get(pk=int(pk))
    success_msg = u''
    error_msg = u''
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            success_msg += u' Изменения успешно сохранены'
        else:
            error_msg = u'Проверьте правильность ввода полей!'
    else:
        form = UserUpdateForm(instance=user)
    context.update({
        'success': success_msg,
        'error': error_msg,
        'form': form,
        'object': user
    })
    return render(request, 'administrator/administrator_update.html', context)
