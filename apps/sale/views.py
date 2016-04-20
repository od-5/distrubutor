# coding=utf-8
import datetime
from django.conf import settings
from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

import xlwt
from datetime import date
from annoying.decorators import ajax_request
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from apps.city.models import City
from .forms import SaleAddForm, SaleUpdateForm, SaleOrderForm, SaleMaketForm, ReviewForm
from apps.manager.models import Manager
from apps.moderator.models import Moderator
from core.forms import UserAddForm, UserUpdateForm
from .models import Sale, SaleOrder, SaleMaket

__author__ = 'alexy'


def sale_add(request):
    context = {}
    user = request.user
    if request.method == 'POST':
        user_form = UserAddForm(request.POST)
        sale_form = SaleAddForm(request.POST, user=user)
        if user_form.is_valid() and sale_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.type = 3
            new_user.save()
            sale = sale_form.save(commit=False)
            sale.user = new_user
            sale.save()
            return HttpResponseRedirect(reverse('sale:update', args=(sale.id, )))
        else:
            context.update({
                'error': u'Проверьте правильность ввода полей'
            })
    else:
        user_form = UserAddForm()
        sale_form = SaleAddForm(user=user)
    context.update({
        'user_form': user_form,
        'sale_form': sale_form
    })
    return render(request, 'sale/sale_add.html', context)


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
            context.update({
                'success': u'Изменения успешно сохранены'
            })
        else:
            context.update({
                'error': u'Проверьте правильность ввода полей'
            })
    else:
        user_form = UserAddForm(instance=sale.user)
        sale_form = SaleUpdateForm(user=user, instance=sale)
    context.update({
        'object': sale,
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
            qs = qs.filter(legal_name=self.request.GET.get('legal_name'))
        if self.request.GET.get('city') and int(self.request.GET.get('city')) != 0:
            qs = qs.filter(city=int(self.request.GET.get('city')))
        if self.request.GET.get('manager') and int(self.request.GET.get('manager')) != 0:
            qs = qs.filter(manager=int(self.request.GET.get('manager')))
        return qs

    def get_context_data(self, **kwargs):
        context = super(SaleListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.type == 1:
            city_qs = City.objects.all()
            manager_qs = Manager.objects.all()
        elif user.type == 2:
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
            'manager_list': manager_qs
        })
        if self.request.GET.get('city'):
            context.update({
                'city_id': int(self.request.GET.get('city'))
            })
        if self.request.GET.get('manager'):
            context.update({
                'manager_id': int(self.request.GET.get('manager'))
            })
        context.update({
            'r_email': self.request.GET.get('email'),
            'r_legal_name': self.request.GET.get('legal_name')
        })
        return context


def sale_order(request, pk):
    context = {}
    error = u''
    sale = Sale.objects.get(pk=int(pk))
    order_list_qs = sale.saleorder_set.all()
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
            return HttpResponseRedirect(reverse('sale:order-update', args=(order.id,)))
        else:
            context.update({
                'error': u'Проверьте правильность ввода полей'
            })
    else:
        form = SaleOrderForm(initial={
            'sale': sale
        })
    context.update({
        'error': error,
        'form': form,
        'object': sale,
        'order_list': order_list
    })
    return render(request, 'sale/sale_order.html', context)


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
    context.update({
        'form': form,
        'object': order,
    })
    return render(request, 'sale/sale_order_update.html', context)


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
        'success': success,
        'error': error,
        'form': form,
        'object': sale,
        'maket_list': maket_list
    })
    return render(request, 'sale/sale_maket.html', context)


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


def review_add(request):
    user = request.user
    if user.type == 3 and request.method == 'POST':
        form = ReviewForm(request.POST, user=user)
        if form.is_valid():
            form.save()
    return HttpResponseRedirect(reverse('dashboard:index'))
