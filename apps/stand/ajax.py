# coding=utf-8
import datetime
from annoying.decorators import ajax_request
from apps.manager.models import Manager
from .models import StandItem, Stand

__author__ = 'alexy'


@ajax_request
def delete_standitem(request):
    stand = request.POST.get('stand', None)
    if stand:
        instance = Stand.objects.get(pk=int(stand))
        instance.standitem_set.all().delete()
        return {
            'success': True
        }
    else:
        return {
            'success': False
        }


@ajax_request
def update_standitem(request):
    width = request.POST.get('width', None)
    stand = request.POST.get('stand', None)
    height = request.POST.get('height', None)
    side = request.POST.get('side', None)
    summa = request.POST.get('sum', None)
    position = request.POST.get('position', None)
    top = request.POST.get('top', None)
    left = request.POST.get('left', None)
    client = request.POST.get('client', None)
    manager = request.POST.get('manager', None)
    created = request.POST.get('created', None)
    if stand and width and height and top and left and side and position:
        if created:
            created = datetime.datetime.strptime(created.strip(), '%d.%m.%Y')
        else:
            created = datetime.date.today()
        stand = Stand.objects.get(pk=int(stand))
        item = StandItem(stand=stand, width=int(width), height=int(height), top=int(top), left=int(left), side=side,
                         position=position, created=created)
        if client:
            client = client.strip()
            item.client = client
            if manager and manager.isdigit():
                manager = Manager.objects.get(pk=int(manager))
                item.manager = manager
            try:
                summa = float(summa)
            except (ValueError, TypeError):
                summa = None
            print summa
            if summa:
                print summa
                item.sum = summa
        item.save()
        return {
            'success': True
        }
    else:
        return {
            'success': False
        }
