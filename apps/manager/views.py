# coding=utf-8
import datetime

import xlwt

from annoying.functions import get_object_or_None

from django.db.models import Sum, Q
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic import ListView

from apps.geolocation.models import City
from apps.moderator.models import Moderator
from apps.sale.models import SaleOrder, SaleOrderPayment
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
        if user.type == User.UserType.administrator:
            qs = Manager.objects.all()
        elif user.type == User.UserType.moderator:
            if user.superviser:
                qs = Manager.objects.select_related().filter(
                    Q(moderator__moderator_user__superviser=user) | Q(moderator=user))
            else:
                qs = Manager.objects.filter(moderator=user)
        elif user.type == User.UserType.manager:
            manager = Manager.objects.get(user=user)
            qs = Manager.objects.filter(moderator=manager.moderator)
        else:
            qs = None
        if qs:
            if self.request.GET.get('city') and int(self.request.GET.get('city')) != 0:
                qs = qs.filter(moderator__moderator_user__city=self.request.GET.get('city'))
            if self.request.GET.get('moderator') and int(self.request.GET.get('moderator')) != 0:
                qs = qs.filter(moderator__moderator_user=self.request.GET.get('moderator'))
            if self.request.GET.get('email'):
                qs = qs.filter(user__email__icontains=self.request.GET.get('email'))
            if self.request.GET.get('last_name'):
                qs = qs.filter(user__last_name__icontains=self.request.GET.get('last_name'))
            if self.request.GET.get('first_name'):
                qs = qs.filter(user__first_name__icontains=self.request.GET.get('first_name'))
            if self.request.GET.get('patronymic'):
                qs = qs.filter(user__patronymic__icontains=self.request.GET.get('patronymic'))
            if self.request.GET.get('phone'):
                qs = qs.filter(user__phone__icontains=self.request.GET.get('phone'))
        return qs

    def get_context_data(self, **kwargs):
        context = super(ManagerListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.type == User.UserType.administrator:
            context.update({
                'city_list': City.objects.all()
            })
        elif user.type == User.UserType.moderator:
            if user.superviser:
                city_qs = City.objects.select_related().filter(
                    Q(moderator__superviser=user) | Q(moderator=user.moderator_user)).distinct()
                moderator_qs = Moderator.objects.filter(Q(superviser=user) | Q(user=user))
                context.update({
                    'moderator_list': moderator_qs.distinct()
                })
            else:
                city_qs = user.moderator_user.city.all()
            context.update({
                'city_list': city_qs
            })
        elif user.type == User.UserType.manager and user.is_leader_manager():
            context.update({
                'city_list': user.manager_user.moderator.moderator_user.city.all()
            })
        if self.request.GET.get('city') and int(self.request.GET.get('city')) != 0:
            context.update({
                'r_city': int(self.request.GET.get('city'))
            })
        if self.request.GET.get('moderator') and int(self.request.GET.get('moderator')) != 0:
            context.update({
                'r_moderator': int(self.request.GET.get('moderator'))
            })
        context.update({
            'r_email': self.request.GET.get('email'),
            'r_last_name': self.request.GET.get('last_name'),
            'first_name': self.request.GET.get('first_name'),
            'r_patronymic': self.request.GET.get('patronymic'),
            'r_phone': self.request.GET.get('phone'),
        })
        return context


# TODO: нужно решение с двумя формами аналогично distributor_add, distributor_update
@login_required
def manager_add(request):
    context = {}
    if request.method == "POST":
        u_form = UserAddForm(request.POST)
        m_form = ManagerForm(request.POST)
        if u_form.is_valid() and m_form.is_valid():
            user = u_form.save(commit=False)
            user.type = User.UserType.manager
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
        if request.user.type == User.UserType.moderator:
            m_form_initial.update({
                'moderator': request.user
            })
        elif request.user.type == User.UserType.manager:
            manager = Manager.objects.get(user=request.user)
            m_form_initial.update({
                'moderator': manager.moderator
            })
        u_form = UserAddForm()
        m_form = ManagerForm(initial=m_form_initial)
        if request.user.type == User.UserType.administrator:
            m_form.fields['moderator'].queryset = User.objects.filter(type=User.UserType.moderator)
        elif request.user.type == User.UserType.moderator:
            if request.user.superviser:
                m_form.fields['moderator'].queryset = User.objects.filter(
                    Q(superviser=request.user) | Q(moderator_user__superviser=request.user)
                )
            else:
                m_form.fields['moderator'].queryset = User.objects.filter(pk=request.user.id)
        elif request.user.type == User.UserType.manager:
            manager = Manager.objects.get(user=request.user)
            m_form.fields['moderator'].queryset = User.objects.filter(pk=manager.moderator.id)

    context.update({
        'u_form': u_form,
        'm_form': m_form
    })
    return render(request, 'manager/manager_add.html', context)


# TODO: нужно решение с двумя формами аналогично distributor_add, distributor_update
@login_required
def manager_update(request, pk):
    context = {}
    manager = Manager.objects.get(pk=int(pk))
    user = manager.user
    success_msg = u''
    error_msg = u''
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=manager.user)
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
        if request.user.type == User.UserType.administrator:
            m_form.fields['moderator'].queryset = User.objects.filter(type=2)
        elif request.user.type == User.UserType.moderator:
            m_form.fields['moderator'].queryset = User.objects.filter(pk=request.user.id)
        elif request.user.type == User.UserType.manager:
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


class ManagerReportView(ListView):
    template_name = 'manager/manager_report.html'

    def get_queryset(self):
        user = self.request.user

        manager_qs = None
        if user.type == User.UserType.administrator:
            manager_qs = Manager.objects.all()
        elif user.type == User.UserType.moderator:
            if user.superviser:
                manager_qs = Manager.objects.select_related().filter(Q(moderator__superviser=user) | Q(moderator=user))
            else:
                manager_qs = user.manager_set.all()
        elif user.type == User.UserType.manager:
            manager_qs = user.manager_user.moderator.manager_set.all()

        r_email = self.request.GET.get('email')
        r_moderator = self.request.GET.get('moderator')
        r_last_name = self.request.GET.get('last_name')
        r_first_name = self.request.GET.get('first_name')
        r_phone = self.request.GET.get('phone')
        r_date_s = self.request.GET.get('date_s')
        r_date_e = self.request.GET.get('date_e')

        if r_moderator and int(r_moderator) != 0:
            manager_qs = manager_qs.filter(moderator=int(r_moderator))
        if r_email:
            manager_qs = manager_qs.filter(user__email__icontains=r_email)
        if r_last_name:
            manager_qs = manager_qs.filter(user__last_name__icontains=r_last_name)
        if r_first_name:
            manager_qs = manager_qs.filter(user__first_name__icontains=r_first_name)

        for manager in manager_qs:
            manager.client_count = manager.client_set.count()
            task_qs = manager.task_set.all()
            saleorder_qs = SaleOrder.objects.filter(sale__manager=manager)
            payment_qs = SaleOrderPayment.objects.filter(sale__manager=manager)
            if r_date_s:
                task_qs = task_qs.filter(date__gte=datetime.datetime.strptime(r_date_s, '%d.%m.%Y'))
                saleorder_qs = saleorder_qs.filter(date_start__gte=datetime.datetime.strptime(r_date_s, '%d.%m.%Y'))
                payment_qs = payment_qs.filter(created__gte=datetime.datetime.strptime(r_date_s, '%d.%m.%Y'))
            if r_date_e:
                task_qs = task_qs.filter(date__lte=datetime.datetime.strptime(r_date_e, '%d.%m.%Y'))
                saleorder_qs = saleorder_qs.filter(date_end__lte=datetime.datetime.strptime(r_date_e, '%d.%m.%Y'))
                payment_qs = payment_qs.filter(created__lte=datetime.datetime.strptime(r_date_e, '%d.%m.%Y'))
            manager.task_count = task_qs.count()
            manager.call_count = task_qs.filter(type=1).count()
            manager.meet_count = task_qs.filter(type=0).count()
            manager.sale_count = task_qs.filter(type=2).count()
            manager.deny_count = task_qs.filter(type=3).count()
            manager.total_sale = 0
            for saleorder in saleorder_qs:
                manager.total_sale += saleorder.total_sum()
            manager.total_payment = payment_qs.aggregate(Sum('sum'))['sum__sum'] or 0

        if r_phone:
            manager_qs = manager_qs.filter(user__phone__icontains=r_phone)

        return manager_qs

    def get_context_data(self, **kwargs):
        context = super(ManagerReportView, self).get_context_data(**kwargs)

        user = self.request.user
        moderator_qs = None
        if user.type == User.UserType.administrator:
            moderator_qs = User.objects.filter(type=2)
        elif user.type == User.UserType.moderator:
            if user.superviser:
                moderator_qs = User.objects.select_related().filter(
                    Q(moderator_user__superviser=user, type=User.UserType.moderator) |
                    Q(moderator_user__user=user, type=User.UserType.moderator))

        r_email = self.request.GET.get('email')
        r_moderator = self.request.GET.get('moderator')
        r_last_name = self.request.GET.get('last_name')
        r_first_name = self.request.GET.get('first_name')
        r_phone = self.request.GET.get('phone')
        r_date_s = self.request.GET.get('date_s')
        r_date_e = self.request.GET.get('date_e')

        if r_moderator and int(r_moderator) != 0:
            context.update({
                'r_moderator': int(r_moderator)
            })
        if r_email:
            context.update({
                'r_email': r_email
            })
        if r_last_name:
            context.update({
                'r_last_name': r_last_name
            })
        if r_first_name:
            context.update({
                'r_first_name': r_first_name
            })
        if r_date_s:
            context.update({
                'r_date_s': r_date_s
            })
        if r_date_e:
            context.update({
                'r_date_e': r_date_e
            })
        if r_phone:
            context.update({
                'r_phone': r_phone
            })

        context.update({
            'moderator_list': moderator_qs,
        })

        return context


def manager_report_excel(request):
    """
    Экспорт отчёта по выбранным менеджерам в xls файл
    :param request:
    :return:
    """
    manager_qs = None
    date_from = request.POST.get('date_from')
    date_to = request.POST.get('date_to')
    if request.POST.getlist('chk_group[]'):
        manager_list = [int(i) for i in request.POST.getlist('chk_group[]')]
        manager_qs = Manager.objects.filter(pk__in=manager_list)
    font0 = xlwt.Font()
    font0.name = 'Calibri'
    font0.height = 200

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
    ws = wb.add_sheet(u'Менеджеры')
    ws.write(0, 0, u'Отчёт по менеджерам', style0)
    ws.write(1, 0, u'Выбранный период:', style0)
    ws.write(1, 1, u'%s' % date_from, style0)
    ws.write(1, 2, u'%s' % date_to, style0)

    ws.write(3, 0, u'ФИО', style1)
    ws.write(3, 1, u'Клиенты', style1)
    ws.write(3, 2, u'Задачи', style1)
    ws.write(3, 3, u'Звонки', style1)
    ws.write(3, 4, u'Встречи', style1)
    ws.write(3, 5, u'Продажи', style1)
    ws.write(3, 6, u'Отказы', style1)
    ws.write(3, 7, u'Сумма продаж', style1)
    ws.write(3, 8, u'Сумма поступлений', style1)
    total_client = total_task = total_call = total_meet = total_sale = total_deny = total_sale_sum = 0
    total_payment_sum = 0
    i = 4
    if manager_qs:
        for manager in manager_qs:
            manager.client_count = manager.client_set.count()
            task_qs = manager.task_set.all()
            saleorder_qs = SaleOrder.objects.filter(sale__manager=manager)
            payment_qs = SaleOrderPayment.objects.filter(sale__manager=manager)
            if date_from:
                task_qs = task_qs.filter(date__gte=datetime.datetime.strptime(date_from, '%d.%m.%Y'))
                saleorder_qs = saleorder_qs.filter(date_start__gte=datetime.datetime.strptime(date_from, '%d.%m.%Y'))
                payment_qs = payment_qs.filter(created__gte=datetime.datetime.strptime(date_from, '%d.%m.%Y'))
            if date_to:
                task_qs = task_qs.filter(date__lte=datetime.datetime.strptime(date_to, '%d.%m.%Y'))
                saleorder_qs = saleorder_qs.filter(date_end__lte=datetime.datetime.strptime(date_to, '%d.%m.%Y'))
                payment_qs = payment_qs.filter(created__lte=datetime.datetime.strptime(date_to, '%d.%m.%Y'))
            manager.task_count = task_qs.count()
            manager.call_count = task_qs.filter(type=1).count()
            manager.meet_count = task_qs.filter(type=0).count()
            manager.sale_count = task_qs.filter(type=2).count()
            manager.deny_count = task_qs.filter(type=3).count()
            manager.total_sale = 0
            manager.total_payment = 0
            for saleorder in saleorder_qs:
                manager.total_sale += saleorder.total_sum()
            manager.total_payment = payment_qs.aggregate(Sum('sum'))['sum__sum'] or 0
            total_client += manager.client_count
            total_task += manager.task_count
            total_call += manager.call_count
            total_meet += manager.meet_count
            total_sale += manager.sale_count
            total_deny += manager.deny_count
            total_sale_sum += manager.total_sale
            total_payment_sum += manager.total_payment

            ws.write(i, 0, manager.__unicode__(), style1)
            ws.write(i, 1, manager.client_count, style1)
            ws.write(i, 2, manager.task_count, style1)
            ws.write(i, 3, manager.call_count, style1)
            ws.write(i, 4, manager.meet_count, style1)
            ws.write(i, 5, manager.sale_count, style1)
            ws.write(i, 6, manager.deny_count, style1)
            ws.write(i, 7, manager.total_sale, style1)
            ws.write(i, 8, manager.total_payment, style1)
            i += 1
        ws.write(i, 0, u'Итого', style0)
        ws.write(i, 1, total_client, style0)
        ws.write(i, 2, total_task, style0)
        ws.write(i, 3, total_call, style0)
        ws.write(i, 4, total_meet, style0)
        ws.write(i, 5, total_sale, style0)
        ws.write(i, 6, total_deny, style0)
        ws.write(i, 7, total_sale_sum, style0)
        ws.write(i, 8, total_payment_sum, style0)

    ws.col(0).width = 10000
    ws.col(1).width = 3000
    ws.col(2).width = 3000
    ws.col(3).width = 3000
    ws.col(4).width = 3000
    ws.col(5).width = 3000
    ws.col(6).width = 3000
    ws.col(7).width = 5100
    ws.col(8).width = 6000
    for count in range(i + 1):
        ws.row(count).height = 400

    fname = 'manager_report.xls'
    response = HttpResponse(content_type="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename=%s' % fname
    wb.save(response)
    return response


def manager_detail_report_excel(request, pk):
    """
    Экспорт детального отчёта по выбранному менеджеру
    :param request:
    :param pk:
    :return:
    """
    manager = get_object_or_None(Manager, pk=int(pk))
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    font0 = xlwt.Font()
    font0.name = 'Calibri'
    font0.height = 200

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
    ws = wb.add_sheet(u'CRM')
    ws1 = wb.add_sheet(u'Продажи')
    ws2 = wb.add_sheet(u'Поступления')
    ws.write(0, 0, u'Отчёт по менеджеру:', style0)
    ws1.write(0, 0, u'Отчёт по продажам менеджера:', style0)
    ws2.write(0, 0, u'Отчёт по поступлениям менеджера:', style0)
    if manager:
        ws.write(0, 1, manager.__unicode__(), style0)
        ws1.write(0, 1, manager.__unicode__(), style0)
        ws2.write(0, 1, manager.__unicode__(), style0)
    ws.write(1, 0, u'Выбранный период:', style0)
    ws.write(1, 1, u'%s' % date_from, style0)
    ws.write(1, 2, u'%s' % date_to, style0)
    ws1.write(1, 0, u'Выбранный период:', style0)
    ws1.write(1, 1, u'%s' % date_from, style0)
    ws1.write(1, 2, u'%s' % date_to, style0)
    ws2.write(1, 0, u'Выбранный период:', style0)
    ws2.write(1, 1, u'%s' % date_from, style0)
    ws2.write(1, 2, u'%s' % date_to, style0)

    ws.write(3, 0, u'Дата', style1)
    ws.write(3, 1, u'Клиент', style1)
    ws.write(3, 2, u'Контактное лици', style1)
    ws.write(3, 3, u'Тип задачи', style1)
    ws.write(3, 4, u'Статус задачи', style1)

    ws1.write(3, 0, u'Дата', style1)
    ws1.write(3, 1, u'Клиент', style1)
    ws1.write(3, 2, u'Сумма продажи, руб.', style1)
    ws1.write(3, 3, u'Сумма поступлений, руб.', style1)

    ws2.write(3, 0, u'Дата', style1)
    ws2.write(3, 1, u'Клиент', style1)
    ws2.write(3, 2, u'Продажа', style1)
    ws2.write(3, 3, u'Сумма поступлений, руб.', style1)
    i = j = k = 4
    if manager:
        task_qs = manager.task_set.all()
        saleorder_qs = SaleOrder.objects.filter(sale__manager=manager)
        payment_qs = SaleOrderPayment.objects.filter(sale__manager=manager)
        if date_from:
            task_qs = task_qs.filter(date__gte=datetime.datetime.strptime(date_from, '%d.%m.%Y'))
            saleorder_qs = saleorder_qs.filter(created__gte=datetime.datetime.strptime(date_from, '%d.%m.%Y'))
            payment_qs = payment_qs.filter(created__gte=datetime.datetime.strptime(date_from, '%d.%m.%Y'))
        if date_to:
            task_qs = task_qs.filter(date__lte=datetime.datetime.strptime(date_to, '%d.%m.%Y'))
            saleorder_qs = saleorder_qs.filter(created__lte=datetime.datetime.strptime(date_to, '%d.%m.%Y'))
            payment_qs = payment_qs.filter(created__lte=datetime.datetime.strptime(date_to, '%d.%m.%Y'))
        for task in task_qs:
            ws.write(i, 0, task.date.strftime('%d.%m.%Y'), style1)
            ws.write(i, 1, task.client.__unicode__(), style1)
            if task.clientcontact:
                ws.write(i, 2, task.clientcontact.__unicode__(), style1)
            else:
                ws.write(i, 2, u'не указано', style1)
            ws.write(i, 3, task.get_type_display(), style1)
            ws.write(i, 4, task.get_status_display(), style1)
            i += 1
        ws.write(i, 0, u'задач: %s' % task_qs.count(), style0)
        ws.write(i, 1, u'назначено звонков: %s' % task_qs.filter(type=1).count(), style0)
        ws.write(i, 2, u'назначено встреч: %s' % task_qs.filter(type=0).count(), style0)
        ws.write(i, 3, u'продаж: %s' % task_qs.filter(type=2).count(), style0)
        ws.write(i, 4, u'отказов: %s' % task_qs.filter(type=3).count(), style0)

        total_saleorder_cost = total_sale_payment = total_payment = 0
        for saleorder in saleorder_qs:
            ws1.write(j, 0, u'%s - %s' % (saleorder.date_start.strftime('%d.%m.%Y'),
                      saleorder.date_start.strftime('%d.%m.%Y')), style1)
            ws1.write(j, 1, saleorder.__unicode__(), style1)
            ws1.write(j, 2, saleorder.total_sum(), style1)
            ws1.write(j, 3, saleorder.current_payment(), style1)
            total_saleorder_cost += saleorder.total_sum()
            total_sale_payment += saleorder.current_payment()
            j += 1
        ws1.write(j, 0, u'Итого:', style0)
        ws1.write(j, 1, u'продаж: %s' % saleorder_qs.count(), style0)
        ws1.write(j, 2, total_saleorder_cost, style0)
        ws1.write(j, 3, total_sale_payment, style0)

        for payment in payment_qs:
            ws2.write(k, 0, payment.created.strftime('%d.%m.%Y'), style1)
            ws2.write(k, 1, payment.sale.__unicode__(), style1)
            ws2.write(k, 2, payment.saleorder.__unicode__(), style1)
            ws2.write(k, 3, payment.sum, style1)
            total_payment += payment.sum
            k += 1
        ws2.write(k, 0, u'Итого:', style0)
        ws2.write(k, 1, u'кол-во поступлений: %s' % payment_qs.count(), style0)
        ws2.write(k, 3, total_payment, style0)
    ws.col(0).width = 6000
    ws.col(1).width = 10000
    ws.col(2).width = 6000
    ws.col(3).width = 6000
    ws.col(4).width = 6000
    ws1.col(0).width = 8000
    ws1.col(1).width = 10000
    ws1.col(2).width = 6000
    ws1.col(3).width = 8000
    ws2.col(0).width = 10000
    ws2.col(1).width = 10000
    ws2.col(2).width = 10000
    ws2.col(3).width = 8000
    for count in range(i + 1):
        ws.row(count).height = 400
    for count in range(j + 1):
        ws1.row(count).height = 400
    for count in range(k + 1):
        ws2.row(count).height = 400

    fname = 'manager_detail_report.xls'
    response = HttpResponse(content_type="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename=%s' % fname
    wb.save(response)
    return response
