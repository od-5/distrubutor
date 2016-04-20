# coding=utf-8
import datetime
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import xlwt
from datetime import date
from annoying.decorators import ajax_request
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from core.forms import UserAddForm, UserUpdateForm
from core.models import User
from .models import Manager
from .forms import ManagerForm

__author__ = 'alexy'


class ManagerListView(ListView):
    model = Manager
    template_name = 'manager/manager_list.html'
    paginate_by = 25

    def get_queryset(self):
        user = self.request.user
        if user.type == 1:
            qs = Manager.objects.all()
        elif self.request.user.type == 2:
            qs = Manager.objects.filter(moderator=user)
        elif self.request.user.type == 5:
            manager = Manager.objects.get(user=self.request.user)
            qs = Manager.objects.filter(moderator=manager.moderator)
        else:
            qs = None
        if qs:
            if self.request.GET.get('email'):
                qs = qs.filter(user__email=self.request.GET.get('email'))
            if self.request.GET.get('last_name'):
                qs = qs.filter(user__last_name=self.request.GET.get('last_name'))
            if self.request.GET.get('email'):
                qs = qs.filter(user__first_name=self.request.GET.get('first_name'))
            if self.request.GET.get('patronymic'):
                qs = qs.filter(user__patronymic=self.request.GET.get('patronymic'))
            if self.request.GET.get('phone'):
                qs = qs.filter(user__phone=self.request.GET.get('phone'))
        return qs

    def get_context_data(self, **kwargs):
        context = super(ManagerListView, self).get_context_data()
        context.update({
            'r_email': self.request.GET.get('email'),
            'r_last_name': self.request.GET.get('last_name'),
            'first_name': self.request.GET.get('first_name'),
            'r_patronymic': self.request.GET.get('patronymic'),
            'r_phone': self.request.GET.get('phone'),
        })
        return context


def manager_add(request):
    context = {}
    if request.method == "POST":
        u_form = UserAddForm(request.POST)
        m_form = ManagerForm(request.POST)
        if u_form.is_valid() and m_form.is_valid():
            user = u_form.save(commit=False)
            user.type = 5
            user.save()
            manager = m_form.save(commit=False)
            manager.user = user
            manager.save()
            return HttpResponseRedirect(reverse('manager:update', args=(manager.id,)))
        else:
            context.update({
                'error': u'Проверьте правильность ввода полей'
            })
    else:
        m_form_initial = {}
        if request.user.type == 2:
            m_form_initial.update({
                'moderator': request.user
            })
        elif request.user.type == 5:
            manager = Manager.objects.get(user=request.user)
            m_form_initial.update({
                'moderator': manager.moderator
            })
        u_form = UserAddForm()
        m_form = ManagerForm(initial=m_form_initial)
        if request.user.type == 1:
            m_form.fields['moderator'].queryset = User.objects.filter(type=2)
        elif request.user.type == 2:
            m_form.fields['moderator'].queryset = User.objects.filter(pk=request.user.id)
        elif request.user.type == 5:
            manager = Manager.objects.get(user=request.user)
            m_form.fields['moderator'].queryset = User.objects.filter(pk=manager.moderator.id)

    context.update({
        'u_form': u_form,
        'm_form': m_form
    })
    return render(request, 'manager/manager_add.html', context)


def manager_update(request, pk):
    context = {}
    manager = Manager.objects.get(pk=int(pk))
    user = manager.user
    success_msg = u''
    error_msg = u''
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=user)
        m_form = ManagerForm(request.POST, instance=manager)
        if u_form.is_valid() and m_form.is_valid():
            u_form.save()
            m_form.save()
            success_msg += u' Изменения успешно сохранены'
        else:
            error_msg = u'Проверьте правильность ввода полей!'
    else:
        u_form = UserUpdateForm(instance=user)
        m_form = ManagerForm(instance=manager)
        if request.user.type == 1:
            m_form.fields['moderator'].queryset = User.objects.filter(type=2)
        elif request.user.type == 2:
            m_form.fields['moderator'].queryset = User.objects.filter(pk=request.user.id)
        elif request.user.type == 5:
            manager = Manager.objects.get(user=request.user)
            m_form.fields['moderator'].queryset = User.objects.filter(pk=manager.moderator.id)

    context.update({
        'success': success_msg,
        'error': error_msg,
        'u_form': u_form,
        'm_form': m_form,
        'object': manager,
    })
    return render(request, 'manager/manager_update.html', context)

