# coding=utf-8
from annoying.functions import get_object_or_None
from datetime import datetime
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView
from apps.city.models import City
from apps.manager.models import Manager
from apps.ticket.forms import TicketChangeForm
from .models import Ticket

__author__ = 'alexy'


def percent_count(total, current):
    if total:
        percent = (float(current)/float(total)) * 100
        return int(percent)
    else:
        return 0


class TicketListView(ListView):
    model = Ticket
    paginate_by = 25
    template_name = 'ticket/ticket_list.html'

    def get_queryset(self):
        user = self.request.user
        if user.type == 1:
            qs = Ticket.objects.all()
        elif user.type == 2:
            if user.moderator_user.ticket_forward:
                qs = Ticket.objects.filter(pk=-1)
            else:
                qs = Ticket.objects.filter(moderator=user.moderator_user)
        elif user.type == 5:
            qs = Ticket.objects.filter(moderator=user.manager_user.moderator.moderator_user)
        else:
            qs = None
        if self.request.GET.get('name'):
            qs = qs.filter(name=self.request.GET.get('name'))
        if self.request.GET.get('phone'):
            qs = qs.filter(phone=self.request.GET.get('phone'))
        if self.request.GET.get('city') and int(self.request.GET.get('city')) != 0:
            qs = qs.filter(city__id=int(self.request.GET.get('city')))
        if self.request.GET.get('type') and self.request.GET.get('type').isdigit():
            qs = qs.filter(type=int(self.request.GET.get('type')))
        r_date_s = self.request.GET.get('date_s')
        r_date_e = self.request.GET.get('date_e')
        if r_date_s:
            qs = qs.filter(created__gte=datetime.strptime(r_date_s, '%d.%m.%Y'))
        if r_date_e:
            qs = qs.filter(created__lte=datetime.strptime(r_date_e, '%d.%m.%Y'))
        return qs

    def get_context_data(self, **kwargs):
        context = super(TicketListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.type == 1:
            city_qs = City.objects.all()
        elif user.type == 2:
            city_qs = user.moderator_user.city.all()
        elif user.type == 5:
            city_qs = user.manager_user.moderator.moderator_user.city.all()
        else:
            city_qs = None
        context.update({
            'city_list': city_qs,
        })
        if self.request.GET.get('city'):
            context.update({
                'r_city': int(self.request.GET.get('city'))
            })
        if self.request.GET.get('type') and self.request.GET.get('type').isdigit():
            context.update({
                'r_type': int(self.request.GET.get('type'))
            })
        if self.request.GET.get('phone'):
            context.update({
                'r_phone': self.request.GET.get('phone')
            })
        if self.request.GET.get('name'):
            context.update({
                'r_name': self.request.GET.get('name')
            })
        if self.request.GET.get('date_s'):
            context.update({
                'r_date_s': self.request.GET.get('date_s')
            })
        if self.request.GET.get('date_e'):
            context.update({
                'r_date_e': self.request.GET.get('date_e')
            })
        total_count = self.object_list.count()
        new_count = self.object_list.filter(type=0).count()
        action_count = self.object_list.filter(type=1).count()
        sale_count = self.object_list.filter(type=3).count()
        new_count_p = percent_count(total_count, new_count)
        action_count_p = percent_count(total_count, action_count)
        sale_count_p = percent_count(total_count, sale_count)
        price_sum = 0
        for i in self.object_list.filter(type=3):
            if i.price:
                price_sum += i.price
        context.update({
            'total_count': total_count,
            'new_count': new_count,
            'action_count': action_count,
            'sale_count': sale_count,
            'new_count_p': new_count_p,
            'action_count_p': action_count_p,
            'sale_count_p': sale_count_p,
            'price_sum': price_sum
        })
        return context


@login_required
def ticket_detail(request, pk):
    context = {}
    user = request.user
    city_qs = City.objects.all()
    if user.type == 2:
        city_qs = city_qs.filter(moderator=user)
    elif user.type == 5:
        manager = Manager.objects.get(user=user)
        city_qs = city_qs.filter(moderator=manager.moderator)
    ticket = get_object_or_None(Ticket, pk=int(pk))
    if request.method == 'POST':
        form = TicketChangeForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('ticket:list'))
        else:
            context.update({
                'error': u'Проверьте правильность ввода данных'
            })
    else:
        form = TicketChangeForm(instance=ticket)
    form.fields['city'].queryset = city_qs
    context.update({
        'form': form,
        'object': ticket
    })
    return render(request, 'ticket/ticket_detail.html', context)
