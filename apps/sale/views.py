# coding=utf-8
import datetime
import os
import zipfile
import StringIO
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Q, Sum
import xlwt

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


from datetime import date
from annoying.decorators import ajax_request
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from django.forms import HiddenInput
from apps.city.models import City
from apps.distributor.models import GPSPoint
from apps.ticket.models import PreSale
from .forms import SaleAddForm, SaleUpdateForm, SaleOrderForm, SaleMaketForm
from apps.manager.models import Manager
from apps.moderator.models import Moderator
from core.forms import UserAddForm, UserUpdateForm
from .models import Sale, SaleOrder, SaleMaket, CommissionOrder

__author__ = 'alexy'


@login_required
def sale_add(request):
    context = {}
    user = request.user
    if request.GET.get('presale'):
        presale = PreSale.objects.get(pk=int(request.GET.get('presale')))
    else:
        presale = None
    if request.method == 'POST':
        user_form = UserAddForm(request.POST)
        sale_form = SaleAddForm(request.POST, user=user)
        if user_form.is_valid() and sale_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.type = 3
            new_user.save()
            sale = sale_form.save(commit=False)
            sale.user = new_user
            sale.password = request.POST.get('password1')
            sale.save()
            if presale:
                presale.accept = True
                presale.save()
            return HttpResponseRedirect(reverse('sale:update', args=(sale.id, )))
        else:
            context.update({
                'error': u'Проверьте правильность ввода полей'
            })
    else:
        user_form = UserAddForm()
        sale_form = SaleAddForm(user=user)
    if presale:
        sale_form.fields['moderator'].initial = presale.moderator
        sale_form.fields['city'].initial = presale.ticket.city
        sale_form.fields['presale'].initial = presale
        sale_form.fields['legal_name'].initial = presale.legal_name
        user_form.fields['email'].initial = presale.ticket.mail
        user_form.fields['phone'].initial = presale.ticket.phone
        user_form.fields['first_name'].initial = presale.ticket.name
        user_form.fields['last_name'].initial = presale.ticket.name
    context.update({
        'user_form': user_form,
        'sale_form': sale_form
    })
    return render(request, 'sale/sale_add.html', context)


@login_required
def sale_view(request, pk):
    context = {}
    user = request.user
    sale = Sale.objects.get(pk=int(pk))
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=sale.user)
        sale_form = SaleUpdateForm(user=user, instance=sale)
        # sale_form = SaleAddForm(request.POST, user=user, instance=sale)
        # if user_form.is_valid() and sale_form.is_valid():
        if user_form.is_valid():
            user_form.save()
            context.update({
                'success': u'Изменения успешно сохранены'
            })
        else:
            context.update({
                'error': u'Проверьте правильность ввода полей'
            })
    else:
        user_form = UserUpdateForm(instance=sale.user)
        sale_form = SaleUpdateForm(user=user, instance=sale)
    context.update({
        'object': sale,
        'sale': sale,
        'user_form': user_form,
        'sale_form': sale_form
    })
    return render(request, 'sale/sale_update.html', context)


@ajax_request
def sale_update(request):
    if request.method == 'POST':
        user = request.user
        try:
            sale = Sale.objects.get(user=int(request.POST.get('user')))
        except:
            return {
                'error': True
            }
        form = SaleUpdateForm(request.POST, user=user, instance=sale)
        if form.is_valid():
            form.save()
            return {
                'success': True
            }
        else:
            return {
                'error': True
            }
    return {
        'error': True
    }


class SaleListView(ListView):
    model = Sale
    paginate_by = 25

    def get_queryset(self):
        user = self.request.user
        if user.type == 1:
            qs = Sale.objects.all()
        elif user.type == 2:
            if user.superviser:
                qs = Sale.objects.filter(Q(moderator__superviser=user) | Q(moderator=user.moderator_user))
            else:
                qs = Sale.objects.filter(moderator=user.moderator_user)
        elif user.type == 5:
            if user.manager_user.leader:
                qs = Sale.objects.filter(moderator=user.manager_user.moderator.moderator_user)
            else:
                qs = Sale.objects.filter(manager=user.manager_user)
        else:
            qs = None
        if self.request.GET.get('email'):
            qs = qs.filter(user__email=self.request.GET.get('email'))
        if self.request.GET.get('legal_name'):
            qs = qs.filter(legal_name__icontains=self.request.GET.get('legal_name'))
        if self.request.GET.get('moderator') and int(self.request.GET.get('moderator')) != 0:
            qs = qs.filter(moderator=int(self.request.GET.get('moderator')))
        if self.request.GET.get('city') and int(self.request.GET.get('city')) != 0:
            qs = qs.filter(city=int(self.request.GET.get('city')))
        if self.request.GET.get('manager') and int(self.request.GET.get('manager')) != 0:
            qs = qs.filter(manager=int(self.request.GET.get('manager')))
        return qs

    def get_context_data(self, **kwargs):
        context = super(SaleListView, self).get_context_data(**kwargs)
        user = self.request.user
        moderator_qs = None
        if user.type == 1:
            city_qs = City.objects.all()
            manager_qs = Manager.objects.all()
        elif user.type == 2:
            if user.superviser:
                city_qs = City.objects.select_related().filter(
                    Q(moderator__superviser=user) | Q(moderator=user.moderator_user)).distinct()
                moderator_qs = Moderator.objects.filter(Q(superviser=user) | Q(user=user))
                manager_qs = Manager.objects.select_related().filter(Q(moderator__superviser=user) | Q(moderator=user))
            else:
                city_qs = user.moderator_user.city.all()
                manager_qs = user.manager_set.all()
        elif user.type == 5:
            manager = Manager.objects.get(user=user)
            city_qs = City.objects.filter(moderator=manager.moderator)
            manager_qs = Manager.objects.filter(moderator=manager.moderator)
        else:
            city_qs = None
            manager_qs = None
        context.update({
            'city_list': city_qs,
            'manager_list': manager_qs,
            'moderator_list': moderator_qs

        })
        if self.request.GET.get('city'):
            context.update({
                'city_id': int(self.request.GET.get('city'))
            })
        if self.request.GET.get('manager'):
            context.update({
                'manager_id': int(self.request.GET.get('manager'))
            })
        if self.request.GET.get('moderator'):
            context.update({
                'moderator_id': int(self.request.GET.get('moderator'))
            })
        context.update({
            'r_email': self.request.GET.get('email'),
            'r_legal_name': self.request.GET.get('legal_name')
        })
        return context


class JournalListView(ListView):
    model = SaleOrder
    paginate_by = 25
    template_name = 'sale/journal_list.html'

    def get_queryset(self):
        user = self.request.user
        if user.type == 1:
            qs = SaleOrder.objects.select_related().all()
        elif user.type == 2:
            if user.superviser:
                qs = SaleOrder.objects.select_related().filter(
                    Q(sale__moderator__superviser=user) | Q(sale__moderator=user.moderator_user))
            else:
                qs = SaleOrder.objects.select_related().filter(sale__moderator=user.moderator_user)
        elif user.type == 5:
            if user.manager_user.leader:
                qs = SaleOrder.objects.select_related().filter(sale__moderator=user.manager_user.moderator.moderator_user)
            else:
                qs = SaleOrder.objects.select_related().filter(sale__manager=user.manager_user)
        elif user.type == 6:
            qs = SaleOrder.objects.select_related().filter(sale__moderator__ticket_forward=True)
        else:
            qs = SaleOrder.objects.none()
        if self.request.GET.get('legal_name'):
            qs = qs.filter(sale__legal_name=self.request.GET.get('legal_name'))
        if self.request.GET.get('city') and int(self.request.GET.get('city')) != 0:
            qs = qs.filter(sale__city=int(self.request.GET.get('city')))
        if self.request.GET.get('moderator') and int(self.request.GET.get('moderator')) != 0:
            qs = qs.filter(sale__moderator=int(self.request.GET.get('moderator')))
        if self.request.GET.get('manager') and int(self.request.GET.get('manager')) != 0:
            qs = qs.filter(sale__manager=int(self.request.GET.get('manager')))
        if self.request.GET.get('date_start'):
            datetime.datetime.strptime(self.request.GET.get('date_start'), '%d.%m.%Y')
            qs = qs.filter(date_start__gte=datetime.datetime.strptime(self.request.GET.get('date_start'), '%d.%m.%Y'))
        if self.request.GET.get('date_end'):
            datetime.datetime.strptime(self.request.GET.get('date_end'), '%d.%m.%Y')
            qs = qs.filter(date_end__lte=datetime.datetime.strptime(self.request.GET.get('date_end'), '%d.%m.%Y'))
        if self.request.GET.get('payment'):
            payment = int(self.request.GET.get('payment'))
            if payment == 0:
                qs = qs.filter(has_payment=False)
            elif payment == 1:
                qs = qs.filter(full_payment=True)
            elif payment == 2:
                qs = qs.filter(full_payment=False, has_payment=True)
            elif payment == 3:
                qs = qs.filter(has_payment=True)
        return qs

    def get_context_data(self, **kwargs):
        context = super(JournalListView, self).get_context_data(**kwargs)
        user = self.request.user
        moderator_qs = None
        if user.type == 1:
            city_qs = City.objects.all()
            manager_qs = Manager.objects.all()
            moderator_qs = Moderator.objects.all()
        elif user.type == 2:
            if user.superviser:
                city_qs = City.objects.select_related().filter(
                    Q(moderator__superviser=user) | Q(moderator=user.moderator_user)).distinct()
                moderator_qs = Moderator.objects.filter(Q(superviser=user) | Q(user=user))
                manager_qs = Manager.objects.select_related().filter(Q(moderator__superviser=user) | Q(moderator=user))
            else:
                city_qs = user.moderator_user.city.all()
                manager_qs = user.manager_set.all()
        elif user.type == 5:
            city_qs = City.objects.filter(moderator=user.manager.moderator)
            manager_qs = Manager.objects.filter(moderator=user.manager.moderator)
        elif user.type == 6:
            manager_qs = Manager.objects.none()
            city_qs = City.objects.filter(moderator__ticket_forward=True)
        else:
            city_qs = City.objects.none()
            manager_qs = Manager.objects.none()
        context.update({
            'city_list': city_qs,
            'moderator_list': moderator_qs,
            'manager_list': manager_qs,
        })
        if self.request.GET.get('payment'):
            context.update({
                'r_payment': int(self.request.GET.get('payment'))
            })
        if self.request.GET.get('date_start'):
            context.update({
                'r_date_start': self.request.GET.get('date_start')
            })
        if self.request.GET.get('date_end'):
            context.update({
                'r_date_end': self.request.GET.get('date_end')
            })
        if self.request.GET.get('city'):
            context.update({
                'city_id': int(self.request.GET.get('city'))
            })
        if self.request.GET.get('moderator'):
            context.update({
                'moderator_id': int(self.request.GET.get('moderator'))
            })
        if self.request.GET.get('manager'):
            context.update({
                'manager_id': int(self.request.GET.get('manager'))
            })
        context.update({
            'r_legal_name': self.request.GET.get('legal_name')
        })
        order_qs = self.get_queryset()
        total_sum = 0
        payments_sum = 0
        for order in order_qs:
            if order.total_sum():
                total_sum += order.total_sum()
            payments_sum += order.current_payment()
        context.update({
            'total_sum': total_sum,
            'payments_sum': payments_sum
        })
        return context


@login_required
def sale_order(request, pk):
    context = {}
    error = u''
    sale = Sale.objects.get(pk=int(pk))
    order_list_qs = sale.saleorder_set.all()
    total_sum = 0
    for order in order_list_qs:
        if order.total_sum():
            total_sum += order.total_sum()
    page = request.GET.get('page')
    paginator = Paginator(order_list_qs, 25)
    page = request.GET.get('page')
    try:
        order_list = paginator.page(page)
    except PageNotAnInteger:
        order_list = paginator.page(1)
    except EmptyPage:
        order_list = paginator.page(paginator.num_pages)
    if request.method == 'POST':
        form = SaleOrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            if sale.presale:
                percent = sale.presale.commission
                sum = (float(order.total_sum()) / 100 ) * float(percent)
                commissionorder = CommissionOrder(
                    moderator=order.sale.moderator,
                    sale=order.sale,
                    saleorder=order,
                    cost=round(sum, 2)
                )
                commissionorder.save()
            return HttpResponseRedirect(reverse('sale:order-update', args=(order.id,)))
        else:
            context.update({
                'error': u'Проверьте правильность ввода полей'
            })
    else:
        form = SaleOrderForm(initial={
            'sale': sale
        })
    form.fields['type'].queryset = sale.moderator.moderatoraction_set.all()
    form.fields['closed'].widget = HiddenInput()
    context.update({
        'total_sum': total_sum,
        'error': error,
        'form': form,
        'object': sale,
        'sale': sale,
        'order_list': order_list
    })
    return render(request, 'sale/sale_order.html', context)


@login_required
def sale_order_update(request, pk):
    context = {}
    order = SaleOrder.objects.get(pk=int(pk))
    sale = order.sale
    if request.method == 'POST':
        form = SaleOrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('sale:order', args=(sale.id, )))
        else:
            context.update({
                'error': u'Проверьте правильность ввода полей'
            })
    else:
        form = SaleOrderForm(instance=order)
    form.fields['type'].queryset = sale.moderator.moderatoraction_set.all()
    context.update({
        'form': form,
        'object': order,
        'sale': sale
    })
    return render(request, 'sale/sale_order_update.html', context)


@login_required
def saleorderpayment_list(request, pk):
    context = {}
    sale = Sale.objects.get(pk=int(pk))
    success_msg = u''
    error_msg = u''
    qs = sale.saleorderpayment_set.all()
    paginator = Paginator(qs, 25)
    page = request.GET.get('page')
    try:
        qs_list = paginator.page(page)
    except PageNotAnInteger:
        qs_list = paginator.page(1)
    except EmptyPage:
        qs_list = paginator.page(paginator.num_pages)
    context.update({
        'object': sale,
        'sale': sale,
        'object_list': qs_list
    })
    return render(request, 'sale/saleorderpayment_list.html', context)


@login_required
def sale_maket(request, pk):
    context = {}
    sale = Sale.objects.get(pk=int(pk))
    success = u''
    error = u''
    if request.method == 'POST':
        form = SaleMaketForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            context.update({
                'success': u'Макет клиента успешно добавлен'
            })
            form = SaleMaketForm(initial={'sale': sale})
        else:
            context.update({
                'error': u'Проверьте правильность ввода полей'
            })
    else:
        form = SaleMaketForm(
            initial={
                'sale': sale
            }
        )
    maket_list_qs = sale.salemaket_set.all()
    paginator = Paginator(maket_list_qs, 25)
    page = request.GET.get('page')
    try:
        maket_list = paginator.page(page)
    except PageNotAnInteger:
        maket_list = paginator.page(1)
    except EmptyPage:
        maket_list = paginator.page(paginator.num_pages)
    context.update({
        'sale': sale,
        'success': success,
        'error': error,
        'form': form,
        'object': sale,
        'maket_list': maket_list
    })
    return render(request, 'sale/sale_maket.html', context)


@login_required
def sale_maket_update(request, pk):
    context = {}
    maket = SaleMaket.objects.get(pk=int(pk))
    success_msg = u''
    error_msg = u''
    if request.method == 'POST':
        form = SaleMaketForm(request.POST, request.FILES, instance=maket)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('sale:maket', args=(maket.sale.id,)))
    else:
        form = SaleMaketForm(instance=maket, initial={
            'file': maket.file
        })
    context.update({
        'success': success_msg,
        'error': error_msg,
        'form': form,
        'object': maket,
    })
    return render(request, 'sale/sale_maket_update.html', context)


def address_export(request):
    sale = request.user.sale_user
    point_qs = GPSPoint.objects.filter(task__sale=sale)
    # ловим значения из формы поиска
    r_task = request.GET.get('task') or None
    r_date_start = request.GET.get('date_start') or None
    r_date_end = request.GET.get('date_end') or None
    r_order = request.GET.get('order') or None
    if r_task and r_task != '0':
        point_qs = point_qs.filter(task=int(r_task))
    if r_order and r_order != '0':
        point_qs = point_qs.filter(task__order=int(r_order))
    if r_date_start:
        point_qs = point_qs.filter(timestamp__gte=datetime.datetime.strptime(r_date_start, '%d.%m.%Y'))
    if r_date_end:
        point_qs = point_qs.filter(timestamp__lte=datetime.datetime.strptime(r_date_end, '%d.%m.%Y'))

    font0 = xlwt.Font()
    font0.name = 'Times New Roman'
    font0.height = 240

    alignment_center = xlwt.Alignment()
    alignment_center.horz = xlwt.Alignment.HORZ_CENTER
    alignment_center.vert = xlwt.Alignment.VERT_TOP

    borders = xlwt.Borders()
    borders.left = xlwt.Borders.THIN
    borders.right = xlwt.Borders.THIN
    borders.top = xlwt.Borders.THIN
    borders.bottom = xlwt.Borders.THIN

    style0 = xlwt.XFStyle()
    style0.font = font0
    style0.alignment = alignment_center

    style1 = xlwt.XFStyle()
    style1.font = font0

    style2 = xlwt.XFStyle()
    style2.font = font0
    style2.borders = borders

    wb = xlwt.Workbook()
    ws = wb.add_sheet(u'Список контрольных точек')
    ws.write_merge(0, 0, 0, 3, u'Отчёт о распространении рекламных материалов', style0)
    ws.write(1, 0, u'Город: %s' % sale.city, style1)
    ws.write(2, 0, u'Исполнитель: %s' % sale.moderator, style1)
    ws.write(3, 0, u'Заказчик: %s' % sale, style1)
    ws.write_merge(5, 5, 0, 3, u'Список адресов контрольных точек', style0)
    ws.write(7, 0, u'Адрес', style2)
    ws.write(7, 1, u'Время', style2)
    ws.write(7, 2, u'Комментарий', style2)
    ws.write(7, 3, u'Кол-во материала', style2)
    i = 8
    material_count = 0
    for point in point_qs:
        if point.pointphoto_set.all():
            ws.write(i, 0, point.name, style2)
            ws.write(i, 1, str(point.timestamp), style2)
            ws.write(i, 2, point.comment, style2)
            ws.write(i, 3, point.count, style2)
            i += 1
            if point.count:
                material_count += point.count
    ws.write(i+1, 0, u'Итого указанное кол-во материала', style1)
    ws.write(i+1, 1, material_count, style1)
    # i = 6
    # porch_total = 0
    # for item in order.clientordersurface_set.all():
    #     ws.write(i, 0, item.surface.city.name, style1)
    #     ws.write(i, 1, item.surface.street.area.name, style1)
    #     ws.write(i, 2, item.surface.street.name, style1)
    #     ws.write(i, 3, item.surface.house_number, style1)
    #     ws.write(i, 4, item.surface.porch_count(), style1)
    #     i += 1
    #     porch_total += item.surface.porch_count()
    # ws.write(i + 1, 0, u'Кол-во домов: %d' % order.clientordersurface_set.all().count(), style0)
    # ws.write(i + 2, 0, u'Кол-во стендов: %d' % porch_total, style0)
    #
    ws.col(0).width = 12000
    ws.col(1).width = 8000
    ws.col(2).width = 15000
    ws.col(3).width = 5000
    # ws.col(4).width = 5000
    for count in range(i):
        ws.row(count).height = 300

    fname = 'address_list.xls'
    response = HttpResponse(content_type="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename=%s' % fname
    wb.save(response)
    return response


def get_files(request):
    # Files (local path) to put in the .zip
    sale = request.user.sale_user
    point_qs = GPSPoint.objects.select_related().filter(task__sale=sale)
    # ловим значения из формы поиска
    r_task = request.GET.get('task') or None
    r_date_start = request.GET.get('date_start') or None
    r_date_end = request.GET.get('date_end') or None
    r_order = request.GET.get('order') or None
    if r_task and r_task != '0':
        point_qs = point_qs.filter(task=int(r_task))
    if r_order and r_order != '0':
        point_qs = point_qs.filter(task__order=int(r_order))
    if r_date_start:
        point_qs = point_qs.filter(timestamp__gte=datetime.datetime.strptime(r_date_start, '%d.%m.%Y'))
    if r_date_end:
        point_qs = point_qs.filter(timestamp__lte=datetime.datetime.strptime(r_date_end, '%d.%m.%Y'))
    filenames = []
    for point in point_qs:
        for q in point.pointphoto_set.all():
            filenames.append(q.photo.path)

    # filenames = ["/tmp/file1.txt", "/tmp/file2.txt"]

    # Folder name in ZIP archive which contains the above files
    # E.g [thearchive.zip]/somefiles/file2.txt
    zip_subdir = "photoarchive"
    zip_filename = "%s.zip" % zip_subdir

    # Open StringIO to grab in-memory ZIP contents
    s = StringIO.StringIO()

    # The zip compressor
    zf = zipfile.ZipFile(s, "w")

    for fpath in filenames:
        # Calculate path for file in zip
        fdir, fname = os.path.split(fpath)
        zip_path = os.path.join(zip_subdir, fname)

        # Add file, at correct path
        zf.write(fpath, zip_path)

    # Must close zip for all contents to be written
    zf.close()

    # Grab ZIP file from in-memory, make response with correct MIME-type
    resp = HttpResponse(s.getvalue(), content_type="application/x-zip-compressed")
    # ..and correct content-disposition
    resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename

    return resp


class CommissionOrderListView(ListView):
    model = CommissionOrder
    paginate_by = 25
    template_name = 'sale/commissionorder_list.html'

    def get_queryset(self):
        user = self.request.user
        if user.type == 1 or user.type == 6:
            qs = CommissionOrder.objects.all()
        else:
            qs = CommissionOrder.objects.none()
        if self.request.GET.get('sale') and int(self.request.GET.get('sale')) != 0:
            qs = qs.filter(sale=int(self.request.GET.get('sale')))
        if self.request.GET.get('city') and int(self.request.GET.get('city')) != 0:
            qs = qs.filter(sale__city=int(self.request.GET.get('city')))
        if self.request.GET.get('moderator') and int(self.request.GET.get('moderator')) != 0:
            qs = qs.filter(moderator=int(self.request.GET.get('moderator')))
        if self.request.GET.get('date_start'):
            qs = qs.filter(timestamp__gte=datetime.datetime.strptime(self.request.GET.get('date_start'), '%d.%m.%Y'))
        if self.request.GET.get('date_end'):
            qs = qs.filter(timestamp__lte=datetime.datetime.strptime(self.request.GET.get('date_end'), '%d.%m.%Y'))
        if self.request.GET.get('pay') and self.request.GET.get('pay').isdigit():
            payment = int(self.request.GET.get('pay'))
            qs = qs.filter(pay=bool(payment))
        return qs

    def get_context_data(self, **kwargs):
        context = super(CommissionOrderListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.type == 1 or user.type == 6:
            city_qs = City.objects.all()
            moderator_qs = Moderator.objects.filter(ticket_forward=True)
            sale_qs = Sale.objects.filter(presale__isnull=False)
        else:
            city_qs = City.objects.none()
            moderator_qs = Moderator.objects.none()
            sale_qs = Moderator.objects.none()
        context.update({
            'city_list': city_qs,
            'moderator_list': moderator_qs,
            'sale_list': sale_qs,
        })
        if self.request.GET.get('pay') and self.request.GET.get('pay').isdigit():
            context.update({
                'r_pay': int(self.request.GET.get('pay'))
            })
        if self.request.GET.get('date_start'):
            context.update({
                'r_date_start': self.request.GET.get('date_start')
            })
        if self.request.GET.get('date_end'):
            context.update({
                'r_date_end': self.request.GET.get('date_end')
            })
        if self.request.GET.get('city'):
            context.update({
                'city_id': int(self.request.GET.get('city'))
            })
        if self.request.GET.get('moderator'):
            context.update({
                'moderator_id': int(self.request.GET.get('moderator'))
            })
        if self.request.GET.get('sale'):
            context.update({
                'sale_id': int(self.request.GET.get('sale'))
            })
        qs = self.object_list
        total_sum = qs.aggregate(Sum('cost'))['cost__sum']
        context.update({
            'total_sum': total_sum
        })
        return context
