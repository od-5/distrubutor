# coding=utf-8
import datetime

import xlwt
from annoying.functions import get_object_or_None

from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Q
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.decorators import login_required

from lib.cbv import SendUserToFormMixin
from apps.moderator.models import ModeratorAction, Moderator
from .task_calendar import get_months
from .models import Distributor, DistributorTask, DistributorPayment, GPSPoint
from .forms import DistributorAddForm, DistributorUpdateForm, DistributorPaymentForm, DistributorTaskForm,\
    GPSPointUpdateForm, DistributorPromoTaskForm, DistributorQuestTaskForm
from core.forms import UserAddForm, UserUpdateForm
from core.models import User

__author__ = 'alexy'


# TODO: нужно упрощать
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
            if user.superviser:
                qs = User.objects.filter(
                    Q(type=4, distributor_user__moderator__superviser=user) |
                    Q(type=4, distributor_user__moderator=user.moderator_user)
                )
            else:
                qs = User.objects.filter(type=4, distributor_user__moderator=user.moderator_user)
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
            qs = qs.filter(distributor_user__moderator__company__icontains=self.request.GET.get('moderator'))
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


# TODO: переделать в CBV, нужно красивое решение с двумя формами
@login_required
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


# TODO: переделать в CBV, нужно красивое решение с двумя формами
@login_required
def distributor_update(request, pk):
    context = {}
    distributor = Distributor.objects.get(pk=int(pk))
    user = distributor.user
    success_msg = u''
    error_msg = u''
    context.update(
        get_months(),
    )
    formset_fields_count = distributor.moderator.moderatoraction_set.count()
    distributor_formset = inlineformset_factory(Distributor, DistributorPayment, form=DistributorPaymentForm,
                                                can_delete=True, min_num=formset_fields_count,
                                                max_num=formset_fields_count)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=user)
        d_form = DistributorUpdateForm(request.POST, instance=distributor)
        # p_form = DistributorPaymentForm(request.POST, instance=distributor)
        formset = distributor_formset(instance=distributor)
        if u_form.is_valid() and d_form.is_valid():
            u_form.save()
            d_form.save()
            success_msg += u' Изменения успешно сохранены'
        else:
            error_msg = u'Проверьте правильность ввода полей!'
    else:
        u_form = UserUpdateForm(instance=user)
        d_form = DistributorUpdateForm(instance=distributor)
        # p_form = DistributorPaymentForm(instance=distributor)
        formset = distributor_formset(instance=distributor)
    for form in formset.forms:
        form.fields['type'].queryset = distributor.moderator.moderatoraction_set.all()
    context.update({
        'success': success_msg,
        'error': error_msg,
        'u_form': u_form,
        'd_form': d_form,
        # 'p_form': p_form,
        'formset': formset,
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
                qs = DistributorTask.objects.filter(distributor__moderator=user.manager_user.moderator.moderator_user,
                                                    closed=False)
            else:
                qs = DistributorTask.objects.filter(sale__manager=user.manager_user, closed=False)
        elif user.type == 6:
            qs = DistributorTask.objects.filter(distributor__moderator__ticket_forward=True, closed=False)
        else:
            qs = DistributorTask.objects.none()
        r_city = self.request.GET.get('city')
        r_type = self.request.GET.get('type')
        r_category = self.request.GET.get('category')
        r_company = self.request.GET.get('company')
        r_distributor = self.request.GET.get('distributor')
        r_date = self.request.GET.get('date')
        if r_city:
            qs = qs.filter(sale__city__name__icontains=r_city)
        if r_type and r_type.isdigit():
            qs = qs.filter(type=int(r_type))
        if r_category and r_category.isdigit():
            qs = qs.filter(category=int(r_category))
        if r_company:
            qs = qs.filter(distributor__moderator__company__icontains=r_company)
        if r_distributor:
            qs = qs.filter(distributor__user__last_name__icontains=r_distributor)
        if r_date:
            qs = qs.filter(date=datetime.datetime.strptime(r_date, '%d.%m.%Y'))
        if self.request.GET.get('date__day') and self.request.GET.get('date__month') and self.request.GET.get(
                'date__year'):
            day = self.request.GET.get('date__day')
            month = self.request.GET.get('date__month')
            year = self.request.GET.get('date__year')
            qs = qs.filter(date__day=day, date__month=month, date__year=year)
        return qs

    def get_context_data(self, **kwargs):
        context = super(DistributorTaskListView, self).get_context_data(**kwargs)
        context.update(
            get_months(),
        )
        user = self.request.user
        if user.type == 2:
            action_qs = ModeratorAction.objects.filter(moderator=user.moderator_user)
        elif user.type == 5:
            action_qs = ModeratorAction.objects.filter(moderator=user.manager_user.moderator.moderator_user)
        else:
            action_qs = None
        context.update({
            'action_list': action_qs
        })
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
        if self.request.GET.get('type') and int(self.request.GET.get('type')) != 0:
            context.update({
                'r_type': int(self.request.GET.get('type'))
            })
        if self.request.GET.get('category') and self.request.GET.get('category').isdigit():
            context.update({
                'r_category': int(self.request.GET.get('category'))
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
                qs = DistributorTask.objects.filter(closed=True,
                                                    distributor__moderator=user.manager_user.moderator.moderator_user)
            else:
                qs = DistributorTask.objects.filter(closed=True, sale__manager=user.manager_user)
        elif user.type == 6:
            qs = DistributorTask.objects.filter(distributor__moderator__ticket_forward=True, closed=False)
        else:
            qs = DistributorTask.objects.none()
        r_city = self.request.GET.get('city')
        r_type = self.request.GET.get('type')
        r_category = self.request.GET.get('category')
        r_company = self.request.GET.get('company')
        r_distributor = self.request.GET.get('distributor')
        r_date = self.request.GET.get('date')
        if qs:
            if r_city:
                qs = qs.filter(sale__city__name=r_city)
            if r_type and r_type.isdigit():
                qs = qs.filter(type=int(r_type))
            if r_category and r_category.isdigit():
                qs = qs.filter(category=int(r_category))
            if r_company:
                qs = qs.filter(distributor__moderator__company__iexact=r_company)
            if r_distributor:
                qs = qs.filter(distributor__last_name__iexact=r_distributor)
            if r_date:
                qs = qs.filter(date=datetime.datetime.strptime(r_date, '%d.%m.%Y'))
        return qs

    def get_context_data(self, **kwargs):
        context = super(DistributorTaskArchiveView, self).get_context_data(**kwargs)
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
                'r_type': int(self.request.GET.get('type'))
            })
        if self.request.GET.get('category'):
            context.update({
                'r_category': int(self.request.GET.get('category'))
            })
        context.update({
            'archive': True
        })
        return context


class DistributorTaskCreateView(CreateView, SendUserToFormMixin):
    form_class = DistributorTaskForm
    template_name = 'distributor/task_add.html'
    success_url = reverse_lazy('distributor:task-list')
    initial = {'category': 0}

    def form_valid(self, form):
        form.instance.type = form.instance.order.type
        return super(DistributorTaskCreateView, self).form_valid(form)


class DistributorTaskUpdateView(UpdateView, SendUserToFormMixin):
    model = DistributorTask
    form_class = DistributorTaskForm
    template_name = 'distributor/task_update.html'
    success_url = reverse_lazy('distributor:task-list')

    def form_valid(self, form):
        if form.instance.order.category == 0:
            form.instance.type = form.instance.order.type
        return super(DistributorTaskUpdateView, self).form_valid(form)


@login_required
def distributor_task_update_map(request, pk):
    context = {}
    task = DistributorTask.objects.select_related().get(pk=int(pk))
    if task.gpspoint_set.all():
        context.update({
            'material_count': task.actual_material_count(),
            'point_list': task.gpspoint_set.all()
        })
    context.update({
        'object': task
    })
    return render(request, 'distributor/task_update_map.html', context)


class DistributorPromoTaskCreateView(CreateView, SendUserToFormMixin):
    """
    Добавление задачи на проведение промо акции
    """
    form_class = DistributorPromoTaskForm
    template_name = 'distributor/task_promo_add.html'
    success_url = reverse_lazy('distributor:task-list')
    initial = {'category': 1}


class DistributorPromoTaskUpdateView(UpdateView, SendUserToFormMixin):
    model = DistributorTask
    form_class = DistributorPromoTaskForm
    template_name = 'distributor/task_promo_update.html'
    success_url = reverse_lazy('distributor:task-list')


class DistributorQuestTaskCreateView(CreateView, SendUserToFormMixin):
    form_class = DistributorQuestTaskForm
    template_name = 'distributor/task_quest_add.html'
    success_url = reverse_lazy('distributor:task-list')
    initial = {'category': 2}


class DistributorQuestTaskUpdateView(UpdateView, SendUserToFormMixin):
    model = DistributorTask
    form_class = DistributorQuestTaskForm
    template_name = 'distributor/task_quest_update.html'
    success_url = reverse_lazy('distributor:task-list')


@login_required
def gps_point_update(request, pk):
    point = GPSPoint.objects.get(pk=int(pk))
    if request.method == 'POST':
        form = GPSPointUpdateForm(request.POST, instance=point)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('distributor:task-update-map', args=(point.task.id, )))
    else:
        form = GPSPointUpdateForm(instance=point)
    context = {
        'point': point,
        'form': form
    }
    return render(request, 'distributor/point_update.html', context)


# TODO: нужно упрощать
class DistributorReportView(ListView):
    template_name = 'distributor/distributor_report.html'

    def get_queryset(self):
        user = self.request.user
        r_email = self.request.GET.get('email')
        r_last_name = self.request.GET.get('last_name')
        r_moderator = self.request.GET.get('moderator')
        r_date_s = self.request.GET.get('date_s')
        r_date_e = self.request.GET.get('date_e')

        qs = None
        if user.type == 1:
            if r_moderator:
                qs = Distributor.objects.select_related().all()
        elif user.type == 2:
            if user.superviser:
                qs = Distributor.objects.filter(
                    Q(moderator__superviser=user) | Q(moderator=user.moderator_user))
            else:
                qs = Distributor.objects.select_related().filter(moderator=user.moderator_user)
        elif user.type == 5:
            qs = Distributor.objects.select_related().filter(moderator=user.manager_user.moderator.moderator_user)

        if r_email:
            qs = qs.filter(user__email__icontains=r_email)
        if r_last_name:
            qs = qs.filter(user__last_name__icontains=r_last_name)
        if r_moderator and r_moderator.isdigit():
            if int(r_moderator) != 0:
                qs = qs.filter(moderator=int(r_moderator))

        if qs:
            for distributor in qs:
                d_task_qs = distributor.distributortask_set.all()
                if r_date_s:
                    d_task_qs = d_task_qs.filter(date__gte=datetime.datetime.strptime(r_date_s, '%d.%m.%Y'))
                if r_date_e:
                    d_task_qs = d_task_qs.filter(date__lte=datetime.datetime.strptime(r_date_e, '%d.%m.%Y'))
                distributor.task_count = d_task_qs.count()
                distributor.actual_material_count = distributor.actual_cost = distributor.total_cost = 0
                for task in d_task_qs:
                    distributor.actual_material_count += task.actual_material_count()
                    distributor.actual_cost += task.actual_cost()
                    distributor.total_cost += task.total_cost()

        return qs

    def get_context_data(self, **kwargs):
        context = super(DistributorReportView, self).get_context_data(**kwargs)

        user = self.request.user
        moderator_qs = None
        if user.type == 1:
            moderator_qs = Moderator.objects.all()
        elif user.type == 2:
            if user.superviser:
                moderator_qs = Moderator.objects.filter(Q(superviser=user) | Q(user=user))
        if moderator_qs is not None:
            context.update({
                'moderator_list': moderator_qs
            })

        r_email = self.request.GET.get('email')
        r_last_name = self.request.GET.get('last_name')
        r_moderator = self.request.GET.get('moderator')
        r_date_s = self.request.GET.get('date_s')
        r_date_e = self.request.GET.get('date_e')
        context.update({
            'r_date_s': r_date_s,
            'r_date_e': r_date_e
        })
        if r_email:
            context.update({
                'r_email': r_email
            })
        if r_last_name:
            context.update({
                'r_last_name': r_last_name
            })
        if r_moderator and r_moderator.isdigit():
            context.update({
                'r_moderator': int(r_moderator)
            })

        return context


def distributor_report_excel(request):
    """
    Экспорт отчёта по выбранным распространителям в xls файл
    :param request:
    :return:
    """
    distributor_qs = None
    date_from = request.POST.get('date_from')
    date_to = request.POST.get('date_to')
    if request.POST.getlist('chk_group[]'):
        distributor_list = [int(i) for i in request.POST.getlist('chk_group[]')]
        distributor_qs = Distributor.objects.filter(pk__in=distributor_list)
    font0 = xlwt.Font()
    font0.name = 'Calibri'
    font0.height = 220

    borders = xlwt.Borders()
    borders.left = xlwt.Borders.THIN
    borders.right = xlwt.Borders.THIN
    borders.top = xlwt.Borders.THIN
    borders.bottom = xlwt.Borders.THIN

    style0 = xlwt.XFStyle()
    style0.font = font0

    style1 = xlwt.XFStyle()
    style1.font = font0
    style1.borders = borders

    wb = xlwt.Workbook()
    ws = wb.add_sheet(u'Распространители')
    ws.write(0, 0, u'Отчёт по распространителям:', style0)
    ws.write(1, 0, u'Выбранный период:', style0)
    ws.write(1, 1, u'%s' % date_from, style0)
    ws.write(1, 2, u'%s' % date_to, style0)

    ws.write(3, 0, u'ФИО', style1)
    ws.write(3, 1, u'Исполнитель', style1)
    ws.write(3, 2, u'Задачи', style1)
    ws.write(3, 3, u'Количество реализованного материала', style1)
    ws.write(3, 4, u'Стоимость работ', style1)
    ws.write(3, 5, u'Сумма к выплате', style1)
    total_task = actual_material_count = total_cost = actual_cost = 0
    i = 4
    if distributor_qs:
        for distributor in distributor_qs:
            task_qs = distributor.distributortask_set.all()
            if date_from:
                task_qs = task_qs.filter(date__gte=datetime.datetime.strptime(date_from, '%d.%m.%Y'))
            if date_to:
                task_qs = task_qs.filter(date__lte=datetime.datetime.strptime(date_to, '%d.%m.%Y'))
            distributor.task_count = task_qs.count()
            distributor.stand_count = 0
            distributor.actual_cost = distributor.total_cost = distributor.actual_material_count = 0
            for task in task_qs:
                distributor.actual_cost += task.actual_cost()
                distributor.total_cost += task.total_cost()
                distributor.actual_material_count += task.actual_material_count()
            total_task += distributor.task_count
            total_cost += distributor.total_cost
            actual_material_count += distributor.actual_material_count
            actual_cost += distributor.actual_cost

            ws.write(i, 0, distributor.__unicode__(), style1)
            ws.write(i, 1, distributor.moderator.__unicode__(), style1)
            ws.write(i, 2, distributor.task_count, style1)
            ws.write(i, 3, distributor.actual_material_count, style1)
            ws.write(i, 4, distributor.total_cost, style1)
            ws.write(i, 5, distributor.actual_cost, style1)
            i += 1
        ws.write(i, 0, u'Итого', style0)
        ws.write(i, 2, total_task, style0)
        ws.write(i, 3, actual_material_count, style0)
        ws.write(i, 4, total_cost, style0)
        ws.write(i, 5, actual_cost, style0)

    ws.col(0).width = 10000
    ws.col(1).width = 10000
    ws.col(2).width = 4000
    ws.col(3).width = 13000
    ws.col(4).width = 5000
    ws.col(5).width = 5000
    for count in range(i + 1):
        ws.row(count).height = 400

    fname = 'distributor_report.xls'
    response = HttpResponse(content_type="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename=%s' % fname
    wb.save(response)
    return response


def distributor_detail_report_excel(request, pk):
    """
    Экспорт детального отчёта по выбранному распространителю в xls файл
    :param request:
    :return:
    """
    distributor = get_object_or_None(Distributor, pk=int(pk))
    date_from = request.GET.get('date_from') or ''
    date_to = request.GET.get('date_to') or ''
    font0 = xlwt.Font()
    font0.name = 'Calibri'
    font0.height = 220

    borders = xlwt.Borders()
    borders.left = xlwt.Borders.THIN
    borders.right = xlwt.Borders.THIN
    borders.top = xlwt.Borders.THIN
    borders.bottom = xlwt.Borders.THIN

    style0 = xlwt.XFStyle()
    style0.font = font0

    style1 = xlwt.XFStyle()
    style1.font = font0
    style1.borders = borders

    wb = xlwt.Workbook()
    ws = wb.add_sheet(u'Отчёт')
    if distributor:
        ws.write(0, 0, u'Отчёт по распространителю:', style0)
        ws.write(0, 1, distributor.__unicode__(), style0)

        ws.write(1, 0, u'Выбранный период:', style0)
        ws.write(1, 1, u'%s' % date_from or '', style0)
        ws.write(1, 2, u'%s' % date_to or '', style0)

        ws.write(3, 0, u'Дата', style1)
        ws.write(3, 1, u'Тип задачи', style1)
        ws.write(3, 2, u'Количество реализованного материала', style1)
        ws.write(3, 3, u'Стоимость работ', style1)
        ws.write(3, 4, u'Сумма к выплате', style1)
        actual_material_count = total_cost = actual_cost = 0
        i = 4
        task_qs = distributor.distributortask_set.all()
        if date_from:
            task_qs = task_qs.filter(date__gte=datetime.datetime.strptime(date_from, '%d.%m.%Y'))
        if date_to:
            task_qs = task_qs.filter(date__lte=datetime.datetime.strptime(date_to, '%d.%m.%Y'))
        for task in task_qs:
            actual_material_count += task.actual_material_count()
            total_cost += task.total_cost()
            actual_cost += task.actual_cost()

            ws.write(i, 0, task.date.strftime('%d.%m.%Y'), style1)
            ws.write(i, 1, task.type.name, style1)
            ws.write(i, 2, task.actual_material_count(), style1)
            ws.write(i, 3, task.total_cost(), style1)
            ws.write(i, 4, task.actual_cost(), style1)
            i += 1
        ws.write(i, 0, u'Итого', style0)
        ws.write(i, 1, task_qs.count(), style0)
        ws.write(i, 2, actual_material_count, style0)
        ws.write(i, 3, total_cost, style0)
        ws.write(i, 4, actual_cost, style0)

        ws.col(0).width = 8000
        ws.col(1).width = 8000
        ws.col(2).width = 15000
        ws.col(3).width = 6000
        ws.col(4).width = 6000
        ws.col(5).width = 6000
        for count in range(i + 1):
            ws.row(count).height = 400

    fname = 'distributor_report_detail_report.xls'
    response = HttpResponse(content_type="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename=%s' % fname
    wb.save(response)
    return response
