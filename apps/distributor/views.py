# coding=utf-8
from annoying.decorators import ajax_request
from annoying.functions import get_object_or_None
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
import datetime
from django.core.urlresolvers import reverse
from django.forms import HiddenInput
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView
from .task_calendar import get_months
from .models import Distributor, DistributorTask
from .forms import DistributorAddForm, DistributorUpdateForm, DistributorPaymentForm, DistributorTaskForm, DistributorTaskUpdateForm
from core.forms import UserAddForm, UserUpdateForm
from core.models import User

__author__ = 'alexy'


class DistributorListView(ListView):
    queryset = User.objects.filter(type=4)
    template_name = 'distributor/distributor_list.html'
    paginate_by = 50

    def get_queryset(self):
        user = self.request.user
        # qs = User.objects.filter(type=4)
        if user.type == 1:
            qs = User.objects.filter(type=4)
        elif user.type == 2:
            # qs = user.moderator_user.distributor_set.all()
            qs = User.objects.filter(distributor_user__moderator=user.moderator_user)
        elif user.type == 5:
            if user.manager_user.leader:
                qs = User.objects.filter(distributor_user__moderator=user.manager_user.moderator.moderator_user)
                # qs = user.manager_user.moderator.moderator_user.distributor_set.all()
            else:
                qs = None
        else:
            qs = None
        if self.request.GET.get('email'):
            qs = qs.filter(email=self.request.GET.get('email'))
        if self.request.GET.get('last_name'):
            qs = qs.filter(last_name=self.request.GET.get('last_name'))
        if self.request.GET.get('first_name'):
            qs = qs.filter(first_name=self.request.GET.get('first_name'))
        if self.request.GET.get('phone'):
            qs = qs.filter(phone=self.request.GET.get('phone'))
        if self.request.GET.get('moderator'):
            qs = qs.filter(distributor_user__moderator__company__iexact=self.request.GET.get('moderator'))
        return qs

    def get_context_data(self, **kwargs):
        context = super(DistributorListView, self).get_context_data(**kwargs)
        context.update({
            'r_email': self.request.GET.get('email', ''),
            'r_last_name': self.request.GET.get('last_name', ''),
            'r_first_name': self.request.GET.get('first_name', ''),
            'r_phone': self.request.GET.get('phone', ''),
            'r_moderator': self.request.GET.get('moderator', '')
        })
        return context


def distributor_add(request):
    context = {}
    user = request.user
    if request.method == "POST":
        u_form = UserAddForm(request.POST)
        d_form = DistributorAddForm(request.POST, user=user)
        if u_form.is_valid() and d_form.is_valid():
            new_user = u_form.save(commit=False)
            new_user.type = 4
            new_user.save()
            distriutor = d_form.save(commit=False)
            distriutor.user = new_user
            distriutor.save()
            return HttpResponseRedirect(reverse('distributor:update', args=(distriutor.id,)))
        else:
            context.update({
                'error': u'Проверьте правильность ввода полей'
            })
    else:
        u_form = UserAddForm()
        d_form = DistributorAddForm(user=user)
    context.update({
        'u_form': u_form,
        'd_form': d_form
    })
    return render(request, 'distributor/distributor_add.html', context)


def distributor_update(request, pk):
    context = {}
    distributor = Distributor.objects.get(pk=int(pk))
    user = distributor.user
    success_msg = u''
    error_msg = u''
    context.update(
        get_months(),
    )
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=user)
        d_form = DistributorUpdateForm(request.POST, instance=distributor)
        p_form = DistributorPaymentForm(request.POST, instance=distributor)
        if u_form.is_valid() and d_form.is_valid():
            u_form.save()
            d_form.save()
            success_msg += u' Изменения успешно сохранены'
        else:
            error_msg = u'Проверьте правильность ввода полей!'
    else:
        u_form = UserUpdateForm(instance=user)
        d_form = DistributorUpdateForm(instance=distributor)
        p_form = DistributorPaymentForm(instance=distributor)

    context.update({
        'success': success_msg,
        'error': error_msg,
        'u_form': u_form,
        'd_form': d_form,
        'p_form': p_form,
        'object': distributor
    })
    return render(request, 'distributor/distributor_update.html', context)


class DistributorTaskListView(ListView):
    model = DistributorTask
    paginate_by = 25
    template_name = 'distributor/task_list.html'

    def get_queryset(self):
        user = self.request.user
        if user.type == 1:
            qs = DistributorTask.objects.filter(closed=False)
        elif user.type == 2:
            qs = DistributorTask.objects.filter(distributor__moderator=user.moderator_user, closed=False)
        elif user.type == 4:
            qs = DistributorTask.objects.filter(distributor=user.distributor_user, closed=False)
        elif user.type == 5:
            if user.manager_user.leader:
                qs = DistributorTask.objects.filter(distributor__moderator=user.manager_user.moderator.moderator_user, closed=False)
            else:
                qs = DistributorTask.objects.filter(sale__manager=user.manager_user, closed=False)
        else:
            qs = None
        r_city = self.request.GET.get('city')
        r_type = self.request.GET.get('type')
        r_company = self.request.GET.get('company')
        r_distributor = self.request.GET.get('distributor')
        r_date = self.request.GET.get('date')
        if qs:
            if r_city:
                qs = qs.filter(sale__city__name=r_city)
            if r_type:
                qs = qs.filter(type=int(r_type))
            if r_company:
                qs = qs.filter(distributor__moderator__company__iexact=r_company)
            if r_distributor:
                qs = qs.filter(distributor__last_name__iexact=r_distributor)
            if r_date:
                qs = qs.filter(date=datetime.datetime.strptime(r_date, '%d.%m.%Y'))
            if self.request.GET.get('date__day') and self.request.GET.get('date__month') and self.request.GET.get('date__year'):
                day = self.request.GET.get('date__day')
                month = self.request.GET.get('date__month')
                year = self.request.GET.get('date__year')
                qs = qs.filter(date__day=day, date__month=month, date__year=year)
        return qs

    def get_context_data(self, **kwargs):
        context = super(DistributorTaskListView, self).get_context_data()
        context.update(
            get_months(),
        )
        if self.request.GET.get('city'):
            context.update({
                'r_city': self.request.GET.get('city')
            })
        if self.request.GET.get('distributor'):
            context.update({
                'r_distributor': self.request.GET.get('distributor')
            })
        if self.request.GET.get('company'):
            context.update({
                'r_company': self.request.GET.get('company')
            })
        if self.request.GET.get('date'):
            context.update({
                'r_date': self.request.GET.get('date')
            })
        if self.request.GET.get('type'):
            context.update({
                'r_type': self.request.GET.get('type')
            })
        return context


class DistributorTaskArchiveView(ListView):
    model = DistributorTask
    paginate_by = 25
    template_name = 'distributor/task_list.html'

    def get_queryset(self):
        user = self.request.user
        if user.type == 1:
            qs = DistributorTask.objects.filter(closed=True)
        elif user.type == 2:
            qs = DistributorTask.objects.filter(closed=True, distributor__moderator=user.moderator_user)
        elif user.type == 4:
            qs = DistributorTask.objects.filter(closed=True, distributor=user.distributor_user)
        elif user.type == 5:
            if user.manager_user.leader:
                qs = DistributorTask.objects.filter(closed=True, distributor__moderator=user.manager_user.moderator.moderator_user)
            else:
                qs = DistributorTask.objects.filter(closed=True, sale__manager=user.manager_user)
        else:
            qs = None
        r_city = self.request.GET.get('city')
        r_type = self.request.GET.get('type')
        r_company = self.request.GET.get('company')
        r_distributor = self.request.GET.get('distributor')
        r_date = self.request.GET.get('date')
        if qs:
            if r_city:
                qs = qs.filter(sale__city__name=r_city)
            if r_type:
                qs = qs.filter(type=int(r_type))
            if r_company:
                qs = qs.filter(distributor__moderator__company__iexact=r_company)
            if r_distributor:
                qs = qs.filter(distributor__last_name__iexact=r_distributor)
            if r_date:
                qs = qs.filter(date=datetime.datetime.strptime(r_date, '%d.%m.%Y'))
        return qs

    def get_context_data(self, **kwargs):
        context = super(DistributorTaskArchiveView, self).get_context_data()
        if self.request.GET.get('city'):
            context.update({
                'r_city': self.request.GET.get('city')
            })
        if self.request.GET.get('distributor'):
            context.update({
                'r_distributor': self.request.GET.get('distributor')
            })
        if self.request.GET.get('company'):
            context.update({
                'r_company': self.request.GET.get('company')
            })
        if self.request.GET.get('date'):
            context.update({
                'r_date': self.request.GET.get('date')
            })
        if self.request.GET.get('type'):
            context.update({
                'r_type': self.request.GET.get('type')
            })
        context.update({
            'archive': True
        })
        return context


def distributor_task_add(request):
    context = {}
    user = request.user
    if request.method == 'POST':
        form = DistributorTaskForm(request.POST, user=user)
        if form.is_valid():
            task = form.save(commit=False)
            task.type = task.order.type
            task.save()
            print task.order.type
            return HttpResponseRedirect(reverse('distributor:task-list'))
        else:
            context.update({
                'error': u'Проверьте правильность ввода полей'
            })
    else:
        form = DistributorTaskForm(user=user)
    context.update({
        'form': form
    })
    return render(request, 'distributor/task_add.html', context)


def distributor_task_update(request, pk):
    context = {}
    user = request.user
    task = DistributorTask.objects.select_related().get(pk=int(pk))
    if task.gpspoint_set.all():
        context.update({
            'point_list': task.gpspoint_set.all()
        })
    if request.method == 'POST':
        form = DistributorTaskUpdateForm(request.POST, user=user, instance=task)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.type = instance.order.type
            instance.save()
            return HttpResponseRedirect(reverse('distributor:task-list'))
        else:
            context.update({
                'error': u'Проверьте правильность ввода полей'
            })
    else:
        form = DistributorTaskUpdateForm(user=user, instance=task)
    form.fields['sale'].widget = HiddenInput()
    form.fields['order'].queryset = task.sale.saleorder_set.filter(closed=False)
    context.update({
        'form': form,
        'object': task
    })
    return render(request, 'distributor/task_update.html', context)
