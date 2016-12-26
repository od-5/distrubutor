# coding=utf-8
from annoying.functions import get_object_or_None
from datetime import datetime
from django import forms
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView
from apps.city.models import City
from apps.manager.models import Manager
from apps.moderator.models import Moderator
from apps.ticket.forms import TicketChangeForm
from core.models import User
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
        elif user.type == 6:
            qs = Ticket.objects.select_related().filter(moderator__ticket_forward=True, agency_manager__isnull=True)
        else:
            qs = Ticket.objects.none()
        if self.request.GET.get('name'):
            qs = qs.filter(name=self.request.GET.get('name'))
        if self.request.GET.get('phone'):
            qs = qs.filter(phone=self.request.GET.get('phone'))
        if self.request.GET.get('city') and int(self.request.GET.get('city')) != 0:
            qs = qs.filter(city__id=int(self.request.GET.get('city')))
        if self.request.GET.get('moderator') and int(self.request.GET.get('moderator')) != 0:
            qs = qs.filter(moderator__id=int(self.request.GET.get('moderator')))
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
        elif user.type == 6:
            city_qs = City.objects.select_related().filter(moderator__ticket_forward=True)
            moderator_qs = Moderator.objects.filter(ticket_forward=True)
            context.update({
                'moderator_list': moderator_qs
            })
        else:
            city_qs = City.objects.none()
        context.update({
            'city_list': city_qs,
        })
        if self.request.GET.get('city') and self.request.GET.get('city').isdigit():
            context.update({
                'r_city': int(self.request.GET.get('city'))
            })
        if self.request.GET.get('moderator') and self.request.GET.get('moderator').isdigit():
            context.update({
                'r_moderator': int(self.request.GET.get('moderator'))
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
        if user.type == 6:
            pass
        else:
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


class TicketAgencyListView(ListView):
    model = Ticket
    paginate_by = 25
    template_name = 'ticket/ticketagency_list.html'

    def get_queryset(self):
        user = self.request.user
        if user.agency_leader:
            qs = Ticket.objects.select_related().filter(
                type__in=[0, 1, 2], moderator__ticket_forward=True, agency_manager__isnull=False)
        else:
            qs = Ticket.objects.select_related().filter(
                type__in=[0, 1, 2], moderator__ticket_forward=True, agency_manager=user)
        if self.request.GET.get('city') and int(self.request.GET.get('city')) != 0:
            qs = qs.filter(city__id=int(self.request.GET.get('city')))
        if self.request.GET.get('agency') and int(self.request.GET.get('agency')) != 0:
            qs = qs.filter(agency_manager__id=int(self.request.GET.get('agency')))
        if self.request.GET.get('moderator') and int(self.request.GET.get('moderator')) != 0:
            qs = qs.filter(moderator__id=int(self.request.GET.get('moderator')))
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
        context = super(TicketAgencyListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.type == 6:
            city_qs = City.objects.select_related().filter(moderator__ticket_forward=True)
            moderator_qs = Moderator.objects.filter(ticket_forward=True)
            if user.agency_leader:
                agency_qs = User.objects.filter(type=6)
                context.update({
                    'agency_list': agency_qs,
                })
            context.update({
                'city_list': city_qs,
                'moderator_list': moderator_qs
            })
            if self.request.GET.get('city') and self.request.GET.get('city').isdigit():
                context.update({
                    'r_city': int(self.request.GET.get('city'))
                })
            if self.request.GET.get('moderator') and self.request.GET.get('moderator').isdigit():
                context.update({
                    'r_moderator': int(self.request.GET.get('moderator'))
                })
            if self.request.GET.get('agency') and self.request.GET.get('agency').isdigit():
                context.update({
                    'r_agency': int(self.request.GET.get('agency'))
                })
            if self.request.GET.get('type') and self.request.GET.get('type').isdigit():
                context.update({
                    'r_type': int(self.request.GET.get('type'))
                })
            if self.request.GET.get('date_s'):
                context.update({
                    'r_date_s': self.request.GET.get('date_s')
                })
            if self.request.GET.get('date_e'):
                context.update({
                    'r_date_e': self.request.GET.get('date_e')
                })
        return context


class TicketSaleListView(ListView):
    model = Ticket
    paginate_by = 25
    template_name = 'ticket/ticketagency_list.html'

    def get_queryset(self):
        user = self.request.user
        if user.agency_leader:
            qs = Ticket.objects.select_related().filter(
                type=3, moderator__ticket_forward=True, agency_manager__isnull=False)
        else:
            qs = Ticket.objects.select_related().filter(
                type=3, moderator__ticket_forward=True, agency_manager=user)
        if self.request.GET.get('city') and int(self.request.GET.get('city')) != 0:
            qs = qs.filter(city__id=int(self.request.GET.get('city')))
        if self.request.GET.get('moderator') and int(self.request.GET.get('moderator')) != 0:
            qs = qs.filter(moderator__id=int(self.request.GET.get('moderator')))
        if self.request.GET.get('agency') and int(self.request.GET.get('agency')) != 0:
            qs = qs.filter(agency_manager__id=int(self.request.GET.get('agency')))
        r_date_s = self.request.GET.get('date_s')
        r_date_e = self.request.GET.get('date_e')
        if r_date_s:
            qs = qs.filter(created__gte=datetime.strptime(r_date_s, '%d.%m.%Y'))
        if r_date_e:
            qs = qs.filter(created__lte=datetime.strptime(r_date_e, '%d.%m.%Y'))
        return qs

    def get_context_data(self, **kwargs):
        context = super(TicketSaleListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.type == 6:
            city_qs = City.objects.select_related().filter(moderator__ticket_forward=True)
            moderator_qs = Moderator.objects.filter(ticket_forward=True)
            if user.agency_leader:
                agency_qs = User.objects.filter(type=6)
                context.update({
                    'agency_list': agency_qs,
                })
            context.update({
                'city_list': city_qs,
                'moderator_list': moderator_qs
            })
            if self.request.GET.get('city') and self.request.GET.get('city').isdigit():
                context.update({
                    'r_city': int(self.request.GET.get('city'))
                })
            if self.request.GET.get('moderator') and self.request.GET.get('moderator').isdigit():
                context.update({
                    'r_moderator': int(self.request.GET.get('moderator'))
                })
            if self.request.GET.get('agency') and self.request.GET.get('agency').isdigit():
                context.update({
                    'r_agency': int(self.request.GET.get('agency'))
                })
            if self.request.GET.get('date_s'):
                context.update({
                    'r_date_s': self.request.GET.get('date_s')
                })
            if self.request.GET.get('date_e'):
                context.update({
                    'r_date_e': self.request.GET.get('date_e')
                })
            total_sum = self.object_list.aggregate(Sum('price'))['price__sum'] or 0
            print total_sum
            context.update({
                'total_sum': total_sum
            })
        context.update({
            'sale': True
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
        city_qs = city_qs.filter(moderator=user.manager.moderator)
    elif user.type == 6:
        city_qs = city_qs.select_related().filter(moderator__ticket_forward=True)
    ticket = get_object_or_None(Ticket, pk=int(pk))
    if request.method == 'POST':
        form = TicketChangeForm(request.POST, instance=ticket)
        if form.is_valid():
            instance = form.save()
            if user.type == 6:
                if instance.type == 3:
                    return HttpResponseRedirect(reverse('ticket:sale'))
                else:
                    if instance.agency_manager:
                        return HttpResponseRedirect(reverse('ticket:sale'))
            return HttpResponseRedirect(reverse('ticket:list'))
        else:
            context.update({
                'error': u'Проверьте правильность ввода данных'
            })
    else:
        form = TicketChangeForm(instance=ticket)
    form.fields['city'].queryset = city_qs
    if user.type != 6:
        form.fields['city'].widget = forms.HiddenInput()
    context.update({
        'form': form,
        'object': ticket
    })
    return render(request, 'ticket/ticket_detail.html', context)
