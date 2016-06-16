# coding=utf-8
from annoying.decorators import ajax_request
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from apps.distributor.models import DistributorTask

__author__ = 'alexy'


@ajax_request
@csrf_exempt
def get_client_coord_list(request):
    coord_list = []
    address_list = []
    all_address_list = []
    center = []
    task_qs = DistributorTask.objects.select_related().filter(sale=request.user.sale_user)
    task = request.POST.get('task') or None
    order = request.POST.get('order') or None
    date_start = request.POST.get('date_start') or None
    date_end = request.POST.get('date_end') or None
    first_point = task_qs.first().gpspoint_set.first()
    if order and order != '0':
        task_qs = task_qs.filter(order=int(order))
    if date_start:
        task_qs = task_qs.filter(date__gte=datetime.strptime(date_start, '%d.%m.%Y'))
    if date_end:
        task_qs = task_qs.filter(date__lte=datetime.strptime(date_end, '%d.%m.%Y'))
    center = [first_point.coord_x, first_point.coord_y]
    if task and task != '0':
        task_qs = DistributorTask.objects.select_related().get(pk=int(task))
        qs = task_qs.gpspoint_set.all()
        center = [qs.first().coord_x, qs.first().coord_y]
        if task_qs.define_address:
            for i in qs:
                address_list.append(i.name)
        else:
            for i in qs:
                coord_list.append([float(i.coord_x), float(i.coord_y)])
    else:
        for i in task_qs:
            for point in i.gpspoint_set.all():
                all_address_list.append({
                    'name': point.name,
                    'coord_x': point.coord_x,
                    'coord_y': point.coord_y
                })
    return {
        'center': center,
        'coord_list': coord_list,
        'address_list': address_list,
        'all_address_list': all_address_list
    }