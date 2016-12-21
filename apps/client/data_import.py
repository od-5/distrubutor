# coding=utf-8
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
import pyexcel
from apps.city.models import City
from apps.client.models import Client, ClientManager, ClientContact
import pyexcel_xls
import pyexcel_xlsx

__author__ = 'alexy'


def client_list_import(request):
    if request.method == 'POST' and 'file' in request.FILES:
        filename = request.FILES['file'].name
        extension = filename.split(".")[1]
        sheet = pyexcel.load_from_memory(extension, request.FILES['file'].read())
        data = pyexcel.to_dict(sheet)
        user = request.user
        error = []
        success = []
        i = 1
        for row in data:
            if row != 'Series_1':
                city = data[row][0]
                name = data[row][1]
                kind_of_activity = data[row][2]
                actual_address = data[row][3]
                site = data[row][4]
                contact_name = data[row][5]
                contact_function = data[row][6]
                contact_phone = data[row][7]
                contact_email = data[row][8]
                try:
                    # проверяем город
                    city_instance = user.manager_user.moderator.moderator_user.city.get(name__iexact=city)
                    try:
                        client = Client.objects.get(name__iexact=name)
                        error.append(u'Строка: %s .Клиент %s уже есть в системе' % (i, client.name))
                    except:
                        client = Client(
                            city=city_instance,
                            name=name,
                            manager=user.manager_user,
                            moderator=user.manager_user.moderator.moderator_user
                        )
                        if kind_of_activity:
                            client.kind_of_activity = kind_of_activity
                        if actual_address:
                            client.actual_address = actual_address
                        if site:
                            client.site = site
                        client.save()
                        success.append(u'Клиент %s добавлен в систему' % name)
                        if contact_name:
                            contact = ClientContact(
                                client=client,
                                name=contact_name
                            )
                        if contact_email:
                            contact.email = contact_email
                        if contact_phone:
                            contact.phone = contact_phone
                        if contact_function:
                            contact.function = contact_function
                        contact.save()
                        clientmanager = ClientManager(
                            manager=user.manager_manager,
                            client=client
                        )
                        clientmanager.save()
                except:
                    error.append(u'Строка %s, Город %s не доступен для модератора %s' % (i, city, user.manager_user.moderator.moderator_user))
            i += 1
        context = {
            'error_list': error,
            'error_count': len(error),
            'success_list': success,
            'success_count': len(success)
        }
        return render(request, 'client/import_error.html', context)
    else:
        return HttpResponseRedirect(reverse('client:list'))
