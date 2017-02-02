# coding=utf-8
from annoying.functions import get_object_or_None
from datetime import datetime
from django import forms
from django.conf import settings
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from apps.geolocation.models import City
from apps.manager.models import Manager
from apps.moderator.models import Moderator
from apps.ticket.forms import TicketChangeForm, PreSaleForm, TicketAddForm
from core.models import User, Setup
from .models import Ticket, PreSale

__author__ = 'alexy'


def percent_count(total, current):
    if total:
        percent = (float(current)/float(total)) * 100
        return int(percent)
    else:
        return 0


@csrf_exempt
def ticket_send(request):
    """
    Сохранение заявки с сайте в базе.
    Отправка письма с уведомлением о новой заявке модератору или рекламному агенству.
    Отправка письма с благодарностью на email, указанный в заявке
    """
    try:
        email = Setup.objects.all()[0].email
    except:
        email = 'od-5@yandex.ru'
    if request.method == "POST":
        form = TicketAddForm(data=request.POST)
        if request.POST.get('moderator'):
            moderator = Moderator.objects.get(pk=int(request.POST.get('moderator')))
            if not moderator.ticket_forward:
                email = Moderator.objects.select_related().get(pk=int(request.POST.get('moderator'))).user.email
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.type = 0
            ticket.save()
            theme = request.POST.get('theme')
            mail_title_msg = u'Новая заявка на сайте reklamadoma.com'
            message = u'Тема: %s\nИмя: %s\nТелефон: %s\n' % (theme, ticket.name, ticket.phone)
            if email:
                send_mail(
                    mail_title_msg,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [email, ]
                )
            if ticket.mail:
                subject = u'Спасибо за заявку на сайте reklamadoma.com'
                # msg_plain = render_to_string('email.txt', {'name': name})
                msg_html = render_to_string('ticket/mail.html')
                try:
                    send_mail(
                        subject,
                        msg_html,
                        settings.DEFAULT_FROM_EMAIL,
                        [ticket.mail, ],
                        html_message=msg_html,
                    )
                except:
                    pass
    return HttpResponseRedirect(reverse('landing:thnx'))


def ticket_add(request):
    """
    Добавление заявки внутри системы.
    Нужно только для рекламного агенства (user.type=6)
    """
    context = {}
    error = None
    if request.method == 'POST':
        form = TicketChangeForm(request.POST)
        if form.is_valid():
            instance = form.save()
            return HttpResponseRedirect(reverse('ticket:detail', args=(instance.pk, )))
        else:
            context.update({
                'error': u'Проверьте правильность ввода данных'
            })
    else:
        form = TicketChangeForm()
    form.fields['city'].queryset = City.objects.all()
    form.fields['moderator'].queryset = Moderator.objects.filter(ticket_forward=True)
    form.fields['type'].widget = forms.HiddenInput()
    context.update({
        'form': form,
        'error': error
    })
    return render(request, 'ticket/ticket_add.html', context)


class TicketListView(ListView):
    model = Ticket
    paginate_by = 25
    template_name = 'ticket/ticket_list.html'

    def get_queryset(self):
        user = self.request.user
        if user.type == 1:
            qs = Ticket.objects.all()
        elif user.type == 2:
            if user.superviser:
                qs = Ticket.objects.filter(Q(moderator__superviser=user) | Q(moderator=user.moderator_user))
            else:
                if user.moderator_user.ticket_forward:
                    qs = Ticket.objects.none()
                else:
                    qs = Ticket.objects.filter(moderator=user.moderator_user)
        elif user.type == 5:
            qs = Ticket.objects.filter(
                moderator=user.manager_user.moderator.moderator_user, moderator__ticket_forward=False)
        elif user.type == 6:
            qs = Ticket.objects.select_related().filter(
                Q(type=0, moderator__ticket_forward=True) | Q(type=0, moderator__isnull=True)
            )
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
            if user.superviser:
                city_qs = City.objects.select_related().filter(
                    Q(moderator__superviser=user) | Q(moderator=user.moderator_user))
                moderator_qs = Moderator.objects.filter(Q(superviser=user) | Q(user=user))
                context.update({
                    'moderator_list': moderator_qs
                })
            else:
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
            'city_list': city_qs.distinct()
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
                Q(type__in=[1, 2], moderator__ticket_forward=True) | Q(type__in=[1, 2], moderator__isnull=True)
            )
        else:
            qs = Ticket.objects.select_related().filter(type__in=[1, 2], agency_manager=user).filter(
                Q(moderator__ticket_forward=True) | Q(moderator__isnull=True)
            )
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
                Q(type=3, moderator__ticket_forward=True) | Q(type=3, moderator__isnull=True)
            )
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
        form.fields['agency_manager'].widget = forms.HiddenInput()
    else:
        form.fields['moderator'].queryset = Moderator.objects.filter(ticket_forward=True)
    if user.type in [2,5]:
        form.fields['moderator'].widget = forms.HiddenInput()
    context.update({
        'form': form,
        'object': ticket
    })
    return render(request, 'ticket/ticket_detail.html', context)


class PreSaleListView(ListView):
    model = PreSale
    paginate_by = 25
    template_name = 'ticket/presale_list.html'

    def get_queryset(self):
        user = self.request.user
        if user.type == 1 or user.type == 6:
            qs = PreSale.objects.all()
        elif user.type == 2:
            if user.superviser:
                qs = PreSale.objects.filter(Q(moderator__superviser=user) | Q(moderator=user.moderator_user))
            else:
                qs = PreSale.objects.filter(moderator=user.moderator_user)
        elif user.type == 5:
            qs = PreSale.objects.filter(
                moderator=user.manager_user.moderator.moderator_user)
        else:
            qs = PreSale.objects.none()
        if self.request.GET.get('legal_name'):
            qs = qs.filter(legal_name=self.request.GET.get('legal_name'))
        if self.request.GET.get('city') and int(self.request.GET.get('city')) != 0:
            qs = qs.filter(ticket__city__id=int(self.request.GET.get('city')))
        if self.request.GET.get('moderator') and int(self.request.GET.get('moderator')) != 0:
            qs = qs.filter(moderator__id=int(self.request.GET.get('moderator')))
        if self.request.GET.get('accept') and self.request.GET.get('accept').isdigit():
            qs = qs.filter(accept=bool(int(self.request.GET.get('accept'))))
        r_date_s = self.request.GET.get('date_s')
        r_date_e = self.request.GET.get('date_e')
        if r_date_s:
            qs = qs.filter(created__gte=datetime.strptime(r_date_s, '%d.%m.%Y'))
        if r_date_e:
            qs = qs.filter(created__lte=datetime.strptime(r_date_e, '%d.%m.%Y'))
        return qs

    def get_context_data(self, **kwargs):
        context = super(PreSaleListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.type == 1:
            city_qs = City.objects.all()
        elif user.type == 2:
            if user.superviser:
                city_qs = City.objects.select_related().filter(
                    Q(moderator__superviser=user) | Q(moderator=user.moderator_user))
                moderator_qs = Moderator.objects.filter(Q(superviser=user) | Q(user=user))
                context.update({
                    'moderator_list': moderator_qs
                })
            else:
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
            'city_list': city_qs.distinct()
        })
        if self.request.GET.get('city') and self.request.GET.get('city').isdigit():
            context.update({
                'r_city': int(self.request.GET.get('city'))
            })
        if self.request.GET.get('moderator') and self.request.GET.get('moderator').isdigit():
            context.update({
                'r_moderator': int(self.request.GET.get('moderator'))
            })
        if self.request.GET.get('accept') and self.request.GET.get('accept').isdigit():
            context.update({
                'r_accept': bool(int(self.request.GET.get('accept')))
            })
        if self.request.GET.get('legal_name'):
            context.update({
                'r_legal_name': self.request.GET.get('legal_name')
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


@login_required
def presale_add(request, pk):
    context = {}
    ticket = Ticket.objects.get(pk=int(pk))
    error = None
    if request.method == 'POST':
        form = PreSaleForm(request.POST)
        if form.is_valid():
            instance = form.save()
            return HttpResponseRedirect(reverse('ticket:presale-update', args=(instance.pk, )))
        else:
            error = u'Проверьте правильность заполнения полей'
    else:
        form = PreSaleForm(initial={
            'ticket': ticket,
            'moderator': ticket.moderator
        })
    form.fields['ticket'].queryset = Ticket.objects.filter(pk=ticket.pk)
    form.fields['moderator'].queryset = Moderator.objects.filter(pk=ticket.moderator.pk)
    context.update({
        'form': form,
        'error': error
    })
    return render(request, 'ticket/presale_form.html', context)


@login_required
def presale_update(request, pk):
    context = {}
    presale = PreSale.objects.get(pk=int(pk))
    error = None
    if request.method == 'POST':
        form = PreSaleForm(request.POST, instance=presale)
        if form.is_valid():
            instance = form.save()
            return HttpResponseRedirect(reverse('ticket:presale-update', args=(instance.pk, )))
        else:
            error = u'Проверьте правильность заполнения полей'
    else:
        form = PreSaleForm(instance=presale)
    form.fields['ticket'].queryset = Ticket.objects.filter(pk=presale.ticket.pk)
    form.fields['moderator'].queryset = Moderator.objects.filter(pk=presale.ticket.moderator.pk)
    context.update({
        'form': form,
        'error': error,
        'object': presale
    })
    return render(request, 'ticket/presale_form.html', context)


@login_required
def presale_detail(request, pk):
    context = {}
    presale = PreSale.objects.get(pk=int(pk))
    context.update({
        'object': presale
    })
    return render(request, 'ticket/presale_detail.html', context)
