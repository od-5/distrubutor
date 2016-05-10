# coding=utf-8
from annoying.decorators import ajax_request
from django.forms import inlineformset_factory
from django.views.decorators.csrf import csrf_exempt
from apps.moderator.models import ModeratorArea
from apps.sale.models import Sale
from .forms import DistributorPaymentForm
from .models import Distributor, DistributorPayment, DistributorTask

__author__ = 'alexy'


@ajax_request
def distributor_payment_update(request):
    distributor_formset = inlineformset_factory(Distributor, DistributorPayment, form=DistributorPaymentForm)
    if request.method == 'POST':
        distributor = Distributor.objects.get(pk=int(request.POST.get('user')))
        formset = distributor_formset(request.POST, instance=distributor)
        if formset.is_valid():
            formset.save()
            return {
                'success': u'Изменения успешно сохранены.'
            }
        else:
            return {
                'error': u'Проверьте правильность ввода данных.()'
            }
    else:
        return {
            'error': u'Проверьте правильность ввода данных.'
        }


@ajax_request
def get_task_initial(request):
    r_sale = request.GET.get('sale')
    distributor_list = []
    area_list = []
    order_list = []
    if r_sale:
        sale = Sale.objects.get(pk=int(r_sale))
        distributor_qs = Distributor.objects.filter(moderator=sale.moderator)
        area_qs = ModeratorArea.objects.filter(moderator=sale.moderator, city=sale.city)
        order_qs = sale.saleorder_set.filter(closed=False)
        for order in order_qs:
            order_list.append({
                'id': order.id,
                'name': order.__unicode__()
            })
        for distributor in distributor_qs:
            distributor_list.append({
                'id': distributor.id,
                'name': distributor.__unicode__()
            })
        for area in area_qs:
            area_list.append({
                'id': area.id,
                'name': area.name
            })

        return {
            'order_list': order_list,
            'distributor_list': distributor_list,
            'area_list': area_list,
        }
    else:
        return {
            'error': u'Произошла ошибка. Приносим свои извинения. Обновите страницу и попробуйте ещё раз.'
        }


@ajax_request
@csrf_exempt
def get_task_cord_list(request):
    coord_list = []
    address_list = []
    if request.POST.get('task'):
        task = DistributorTask.objects.get(id=int(request.POST.get('task')))
        if task.define_address:
            for i in task.gpspoint_set.all():
                address_list.append(i.name)
        else:
            for i in task.gpspoint_set.all():
                coord_list.append([i.coord_x, i.coord_y])
    return {
        'coord_list': coord_list,
        'address_list': address_list
    }
