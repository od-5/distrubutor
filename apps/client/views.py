# coding=utf-8
import datetime
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import xlwt
from datetime import date, datetime
from annoying.decorators import ajax_request
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from django.utils import timezone
from apps.city.models import City
from apps.manager.models import Manager
from core.forms import UserAddForm, UserUpdateForm
from core.models import User
from .models import Client, Task, ClientContact, ClientManager
from .forms import ClientAddForm, ClientUpdateForm, TaskForm, ClientContactForm

__author__ = 'alexy'


class ClientListView(ListView):
    model = Client
    template_name = 'client/client_list.html'
    paginate_by = 25

    def get_queryset(self):
        user = self.request.user
        name = self.request.GET.get('name')
        phone = self.request.GET.get('phone')
        contact = self.request.GET.get('contact')
        if user.type == 1:
            qs = Client.objects.all()
        elif user.type == 2:
            qs = Client.objects.filter(moderator=user.moderator_user)
        elif user.type == 5:
            if user.manager_user.leader:
                qs = Client.objects.filter(moderator=user.manager_user.moderator.moderator_user)
            else:
                qs = Client.objects.filter(manager=user.manager_user)
        else:
            qs = None
        if name:
            qs = qs.filter(name=name)
        if phone or name:
            client_id_list = [int(i.id) for i in qs]
            c_qs = ClientContact.objects.filter(client__in=client_id_list)
            if phone:
                c_qs = c_qs.filter(phone=phone)
            if contact:
                c_qs = c_qs.filter(name__icontains=contact)
                # qs = qs.filter(name=self.request.GET.get('name'))
            client_id_list = [int(i.incomingclient.id) for i in c_qs]
            qs = qs.filter(id__in=client_id_list)

        return qs

    def get_context_data(self, **kwargs):
        context = super(ClientListView, self).get_context_data(**kwargs)
        if self.request.GET.get('name'):
            context.update({
                'r_name': self.request.GET.get('name')
            })
        if self.request.GET.get('phone'):
            context.update({
                'r_phone': self.request.GET.get('phone')
            })
        if self.request.GET.get('contact'):
            context.update({
                'r_contact': self.request.GET.get('contact')
            })
        queryset = self.get_queryset()
        manager_client_count = queryset.count()
        manager_task_count = 0
        for client in queryset:
            manager_task_count += client.task_set.count()
        context.update({
            'manager_client_count': manager_client_count,
            'manager_task_count': manager_task_count
        })
        user = self.request.user
        if user.type == 1:
            manager_qs = Manager.objects.all()
        elif user.type == 2:
            manager_qs = Manager.objects.filter(moderator=user.moderator_user)
        elif user.type == 5:
            current_manager = Manager.objects.get(user=user)
            context.update({
                'current_manager': current_manager
            })
            manager_qs = Manager.objects.filter(moderator=current_manager.moderator.moderator_user)
        else:
            manager_qs = None
        context.update({
            'manager_list': manager_qs
        })
        return context


def client_add(request):
    context = {}
    user = request.user
    if request.method == "POST":
        form = ClientAddForm(request.POST, user=user)
        if form.is_valid():
            client = form.save(commit=False)
            client.save()
            clientmanager = ClientManager(manager=client.manager, client=client)
            clientmanager.save()
            # return HttpResponseRedirect(reverse('client:update', args=(incoming.id,)))
            context.update({
                'success': u'Клиент добавлен!'
            })
        else:
            context.update({
                'error': u'Проверьте правильность ввода полей'
            })
    else:
        form = ClientAddForm(user=user)
    context.update({
        'form': form,
    })
    return render(request, 'client/client_add.html', context)


def client_update(request, pk):
    context = {}
    client = Client.objects.get(pk=int(pk))
    old_manager_id = client.manager.id
    success_msg = u''
    error_msg = u''
    user = request.user
    if request.method == 'POST':
        form = ClientUpdateForm(request.POST, user=user, instance=client)
        if form.is_valid():
            client = form.save(commit=False)
            client.save()
            if old_manager_id != client.manager.id:
                client.type = 2
                client.save()
                clientmanager = ClientManager(manager=client.manager, gclient=client)
                clientmanager.save()
            success_msg = u' Изменения успешно сохранены'
        else:
            error_msg = u'Проверьте правильность ввода полей!'
    else:
        form = ClientUpdateForm(user=user, instance=client)

    context.update({
        'success': success_msg,
        'error': error_msg,
        'form': form,
        'object': client,
    })
    return render(request, 'client/client_update.html', context)


def clientmanager_history(request, pk):
    client = Client.objects.get(pk=int(pk))
    context = {
        'object': client,
        'object_list': client.clientmanager_set.all()
    }
    return render(request, 'client/clientmanager_history.html', context)


def clientcontact_list(request, pk):
    client = Client.objects.get(pk=int(pk))
    context = {
        'object': client,
        'object_list': client.clientcontact_set.all()
    }
    return render(request, 'client/clientcontact_list.html', context)


def clientcontact_add(request, pk):
    success_msg = None
    error_msg = None
    client = Client.objects.get(pk=int(pk))
    if request.method == 'POST':
        form = ClientContactForm(request.POST)
        if form.is_valid():
            form.save()
            success_msg = u'Контактное лицо успешно добавлено'
            return HttpResponseRedirect(reverse('client:contact-list', args=(client.id,)))
        else:
            error_msg = u'Проверьте правильность ввода полей!'
    else:
        form = ClientContactForm(
            initial={
                'client': client
            }
        )
    context = {
        'object': client,
        'form': form,
        'success_msg': success_msg,
        'error_msg': error_msg
    }
    return render(request, 'client/clientcontact_add.html', context)


def clientcontact_update(request, pk):
    context = {}
    success_msg = None
    error_msg = None
    contact = ClientContact.objects.get(pk=int(pk))
    if request.method == 'POST':
        form = ClientContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            success_msg = u'Изменения сохранены'
            return HttpResponseRedirect(reverse('client:contact-list', args=(contact.client.id,)))
        else:
            error_msg = u'Проверьте правильность ввода полей!'
    else:
        form = ClientContactForm(instance=contact)
    context = {
        'contact': contact,
        'object': contact.client,
        'form': form,
        'success_msg': success_msg,
        'error_msg': error_msg
    }
    return render(request, 'client/clientcontact_update.html', context)

#
# def incomingtask_list(request):
#     context = {}
#     if request.GET.get('error') and int(request.GET.get('error')) == 1:
#         context.update({
#             'error': True
#         })
#
#     user = request.user
#     if user.type == 1:
#         qs = IncomingTask.objects.all()
#     elif user.type == 2:
#         qs = IncomingTask.objects.filter(manager__moderator=user)
#     elif user.type == 5:
#         if user.is_leader_manager():
#             manager = Manager.objects.get(user=user)
#             qs = IncomingTask.objects.filter(manager__moderator=manager.moderator)
#         else:
#             qs = IncomingTask.objects.filter(manager__user=user)
#     else:
#         qs = None
#
#     r_name = request.GET.get('name')
#     r_date_s = request.GET.get('date_s')
#     r_date_e = request.GET.get('date_e')
#     r_all = request.GET.get('all')
#     r_type = request.GET.get('type')
#     r_status = request.GET.get('status')
#     if r_all and int(r_all) == 1:
#         request.session['show_all_incomingtask'] = True
#     elif r_all and int(r_all) == 0:
#         request.session['show_all_incomingtask'] = False
#     try:
#         show_all = request.session['show_all_incomingtask']
#     except:
#         show_all = False
#
#     if not r_name and not r_date_s and not r_date_e and not show_all:
#         qs = qs.filter(date=timezone.localtime(timezone.now()))
#     else:
#         if r_name:
#             qs = qs.filter(incomingclient__name__icontains=r_name)
#         if r_date_s:
#             qs = qs.filter(date__gte=datetime.strptime(r_date_s, '%d.%m.%Y'))
#         if r_date_e:
#             qs = qs.filter(date__lte=datetime.strptime(r_date_e, '%d.%m.%Y'))
#
#     if r_type:
#         qs = qs.filter(type=int(r_type))
#         context.update({
#             'r_type': True
#         })
#     if r_status:
#         qs = qs.filter(status=int(r_status))
#         context.update({
#             'r_status': int(r_status)
#         })
#     if r_name:
#         context.update({
#             'r_name': r_name
#         })
#
#     if r_date_s:
#         context.update({
#             'r_date_s': r_date_s
#         })
#     if r_date_e:
#         context.update({
#             'r_date_e': r_date_e
#         })
#     if show_all:
#         context.update({
#             'show_all': True
#         })
#     paginator = Paginator(qs, 25)
#     page = request.GET.get('page')
#     try:
#         object_list = paginator.page(page)
#     except PageNotAnInteger:
#         object_list = paginator.page(1)
#     except EmptyPage:
#         object_list = paginator.page(paginator.num_pages)
#     context.update({
#         'object_list': object_list
#     })
#     return render(request, 'incoming/incomingtask_list.html', context)
#
# def incomingtask_add(request):
#     context = {}
#     initial = {}
#     user = request.user
#     if user.type == 1:
#         manager_qs = Manager.objects.all()
#         incomingclient_qs = IncomingClient.objects.all()
#     elif user.type == 2:
#         manager_qs = Manager.objects.filter(moderator=user)
#         incomingclient_qs = IncomingClient.objects.filter(manager__moderator=user)
#     elif user.type == 5:
#         manager = Manager.objects.get(user=user)
#         manager_qs = Manager.objects.filter(moderator=manager.moderator)
#         if user.is_leader_manager():
#             incomingclient_qs = IncomingClient.objects.filter(manager__moderator=manager.moderator)
#         else:
#             incomingclient_qs = IncomingClient.objects.filter(manager=manager)
#             initial = {
#                 'manager': manager
#             }
#     else:
#         manager_qs = None
#         incomingclient_qs = None
#     if request.method == "POST":
#         form = IncomingTaskForm(request.POST, initial=initial)
#         if form.is_valid():
#             instance = form.save(commit=False)
#             instance.save()
#             return HttpResponseRedirect(reverse('incoming:task-update', args=(instance.id,)))
#         else:
#             context.update({
#                 'error': u'Проверьте правильность ввода полей'
#             })
#     else:
#         form = IncomingTaskForm(initial=initial)
#     form.fields['manager'].queryset = manager_qs
#     form.fields['incomingclient'].queryset = incomingclient_qs
#     context.update({
#         'form': form,
#     })
#     return render(request, 'incoming/incomingtask_add.html', context)
#
#
# def incomingtask_update(request, pk):
#     context = {}
#     object = IncomingTask.objects.get(pk=int(pk))
#     success_msg = u''
#     error_msg = u''
#     user = request.user
#     if user.type == 1:
#         manager_qs = Manager.objects.all()
#     elif user.type == 2:
#         manager_qs = Manager.objects.filter(moderator=user)
#     elif user.type == 5:
#         manager = Manager.objects.get(user=user)
#         manager_qs = Manager.objects.filter(moderator=manager.moderator)
#     else:
#         manager_qs = None
#     if request.method == 'POST':
#         form = IncomingTaskForm(request.POST, instance=object)
#         if form.is_valid():
#             form.save()
#             success_msg = u' Изменения успешно сохранены'
#         else:
#             error_msg = u'Проверьте правильность ввода полей!'
#     else:
#         form = IncomingTaskForm(instance=object)
#
#     form.fields['manager'].queryset = manager_qs
#     form.fields['incomingclientcontact'].queryset = object.incomingclient.incomingclientcontact_set.all()
#
#     context.update({
#         'success': success_msg,
#         'error': error_msg,
#         'form': form,
#         'object': object,
#     })
#     return render(request, 'incoming/incomingtask_update.html', context)
