# coding=utf-8
from annoying.decorators import ajax_request
from datetime import datetime
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, JsonResponse
from apps.client.models import Client
from apps.sale.models import Sale
from core.models import User
from .models import Client, Task, ClientContact
from apps.manager.models import Manager
from .models import Client, ClientManager

__author__ = 'alexy'


@ajax_request
def reassign_manager(request):
    old_id = int(request.GET.get('manager'))
    new_id = int(request.GET.get('new_manager'))
    client_id = int(request.GET.get('client'))
    if old_id != new_id:
        client = Client.objects.get(pk=client_id)
        new_manager = Manager.objects.get(pk=new_id)
        client.manager = new_manager
        client.type = 2
        client.save()
        new_clientmanager = ClientManager(manager=new_manager, client=client)
        new_clientmanager.save()
        tasks = Task.objects.filter(client=client_id)
        if tasks.count() != 0:
            for task in tasks:
                task.manager = new_manager
                task.save()
        return {
            'success': True,
            'old_id': old_id,
            'client_id': client.id,
            'id': new_id,
            'name': client.manager.user.get_full_name(),
        }
    else:
        return {
            'success': False,
        }


@ajax_request
def get_available_manager_list(request):
    manager_list = []
    current_manager = Manager.objects.get(pk=int(request.GET.get('manager')))
    manager_qs = Manager.objects.filter(moderator=current_manager.moderator.id)
    for manager in manager_qs:
        manager_list.append({
            'id': manager.id,
            'name': manager.user.get_full_name()
        })
    return {
        'manager_list': manager_list
    }


@ajax_request
def get_contact_list(request):
    contact_list = []
    client = Client.objects.get(pk=int(request.GET.get('client')))
    for contact in client.clientcontact_set.all():
        contact_list.append({
            'id': contact.id,
            'name': contact.name,
            'function': contact.function,
            'phone': contact.phone,
            'email': contact.email,
        })
    if len(contact_list) != 0:
        return {
            'contact_list': contact_list
        }
    else:
        return {
            'contact_list': True
        }


@ajax_request
def get_task_info(request):
    task = Task.objects.get(pk=int(request.GET.get('task')))
    contact_list = []
    for i in task.client.clientcontact_set.all():
        contact_list.append({
            'id': i.id,
            'name': i.name
        })
    return {
        'task_id': task.id,
        'client_id': task.client.id,
        'client_name': task.client.name,
        'manager_id': task.manager.id,
        'client_type': task.client.get_type_display(),
        'contact_list': contact_list
    }



# ПОКА НЕ ПРОВЕРЕНО

@ajax_request
def get_client_info(request):
    client = Client.objects.get(pk=int(request.GET.get('client')))
    contact_list = []
    for i in client.clientcontact_set.all():
        contact_list.append({
            'id': i.id,
            'name': i.name
        })
    return {
        'id': client.id,
        'name': client.name,
        'manager': client.manager.id,
        'type': client.get_type_display(),
        'contact_list': contact_list
    }


@ajax_request
def ajax_task_add(request):
    try:
        client = Client.objects.get(pk=int(request.GET.get('client')))
        type_id = int(request.GET.get('type'))
        date = datetime.strptime(request.GET.get('date'), '%d.%m.%Y')
        comment = request.GET.get('comment')
        manager = Manager.objects.get(pk=int(request.GET.get('manager')))
        clientcontact = ClientContact.objects.get(pk=int(request.GET.get('client_contact')))
        task = Task(
            manager=manager,
            client=client,
            clientcontact=clientcontact,
            type=type_id,
            date=date,
            comment=comment,
            status=0
        )
        task.save()
        return {
            'success': True
        }
    except:
        return {
            'success': False
        }


@ajax_request
def ajax_task_update(request):
    print request.GET
    try:
        manager_id = int(request.GET.get('manager'))
        client_id = int(request.GET.get('client'))
        task_id = int(request.GET.get('task'))
        client_contact_id = int(request.GET.get('client_contact'))
        type_id = int(request.GET.get('type'))
        comment = request.GET.get('comment')
        date = datetime.strptime(request.GET.get('date'), '%d.%m.%Y')

        client = Client.objects.get(pk=client_id)
        task = Task.objects.get(pk=task_id)
        manager = Manager.objects.get(pk=manager_id)
        clientcontact = ClientContact.objects.get(pk=client_contact_id)
        new_task = Task(
            manager=manager,
            client=client,
            clientcontact=clientcontact,
            type=type_id,
            date=date,
            comment=comment,
            status=0
        )
        new_task.save()
        task.status = 1
        task.save()
        return {
            'success': True
        }
    except:
        return {
            'success': False
        }


def ajax_sale_add(request):
    r_client = request.POST.get('client')
    r_manager = request.POST.get('manager')
    r_task = request.POST.get('task')
    r_email = request.POST.get('email')
    r_password = request.POST.get('password')
    client = Client.objects.get(pk=int(r_client))
    task = Task.objects.get(pk=int(r_task))
    manager = Manager.objects.get(pk=int(r_manager))
    try:
        User.objects.get(email=r_email)
    except User.DoesNotExist:
        user = User(email=r_email, password=r_password, type=3)
        user.set_password(r_password)
        user.save()
        sale = Sale(
            user=user,
            city=client.city,
            manager=client.manager,
            moderator=client.moderator,
            legal_name=client.name,
            actual_name=client.name,
            legal_address=client.actual_address
        )
        sale.save()
        task.status = 1
        task.save()
        return HttpResponseRedirect(reverse('sale:update', args=(sale.id, )))
    return_url = reverse('client:task-list') + '?error=1'
    return HttpResponseRedirect(return_url)
