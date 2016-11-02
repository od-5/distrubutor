# coding=utf-8
from annoying.decorators import ajax_request
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from apps.distributor.models import DistributorTask
from apps.sale.models import SaleOrder, Sale, SaleOrderPayment

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
    if order and order != '0':
        task_qs = task_qs.filter(order=int(order))
    if date_start:
        task_qs = task_qs.filter(date__gte=datetime.strptime(date_start, '%d.%m.%Y'))
    if date_end:
        task_qs = task_qs.filter(date__lte=datetime.strptime(date_end, '%d.%m.%Y'))
    if task_qs and task_qs.first().gpspoint_set.all():
        center = [task_qs.first().gpspoint_set.first().coord_x, task_qs.first().gpspoint_set.first().coord_y]
    else:
        center = [request.user.sale_user.city.coord_y, request.user.sale_user.city.coord_x]
    if task and task != '0':
        task_qs = DistributorTask.objects.select_related().get(pk=int(task))
        qs = task_qs.gpspoint_set.all()
        if qs:
            center = [qs.first().coord_x, qs.first().coord_y]
        else:
            center = [task_qs.sale.city.coord_y, task_qs.sale.city.coord_x]
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


@ajax_request
def payment_add(request):
    try:
        print request.META.get('HTTP_REFERER')
        print request.POST.get('p_sale')
        print request.POST.get('p_saleorder')
        print request.POST.get('p_sum')
        sale = Sale.objects.get(pk=int(request.POST.get('p_sale')))
        print '1'*10
        saleorder = SaleOrder.objects.get(pk=int(request.POST.get('p_saleorder')))
        print '2'*10
        sum = request.POST.get('p_sum')
        print '3'*10
        payment = SaleOrderPayment(
            sale=sale,
            saleorder=saleorder,
            sum=sum
        )
        print '4'*10
        payment.save()
        print '5'*10
        return {
            'success': True
        }
    except:
        return {
            'error': True
        }

