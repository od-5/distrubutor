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
    center = []
    if request.POST.get('task'):
        task = DistributorTask.objects.get(id=int(request.POST.get('task')))
        qs = task.gpspoint_set.all()
        center = [qs.first().coord_x, qs.first().coord_y]
        if task.define_address:
            for i in qs:
                address_list.append(i.name)
        else:
            for i in qs:
                if i.coord_x and i.coord_y:
                    coord_list.append([float(i.coord_x), float(i.coord_y)])
    return {
        'center': center,
        'coord_list': coord_list,
        'address_list': address_list
    }


@ajax_request
@csrf_exempt
def get_current_location(request):
    email = request.POST.get('email') or None
    moderator = request.POST.get('moderator') or None
    last_name = request.POST.get('last_name') or None
    first_name = request.POST.get('first_name') or None
    phone = request.POST.get('phone') or None
    user = request.user
    data_list = []
    if user.type == 1:
        qs = Distributor.objects.select_related().filter(coord_x__isnull=False, coord_y__isnull=False)
        if moderator:
            qs = qs.filter(moderator__company__iexact=moderator)
    elif user.type == 2:
        qs = Distributor.objects.select_related().filter(moderator=user.moderator_user, coord_x__isnull=False, coord_y__isnull=False)
    elif user.type == 5:
        qs = Distributor.objects.select_related().filter(moderator=user.manager_user.moderator, coord_x__isnull=False, coord_y__isnull=False)
    else:
        qs = None
    if email:
        qs = qs.filter(user__email__iexact=email)
    if last_name:
        qs = qs.filter(user__last_name__iexact=last_name)
    if first_name:
        qs = qs.filter(user__first_name__iexact=first_name)
    if phone:
        qs = qs.filter(user__phone__iexact=phone)
    for item in qs:
        # if item.coord_x and item.coord_y:
        data_list.append({
            'name': item.__unicode__(),
            'coord_x': item.coord_x,
            'coord_y': item.coord_y,
            'coord_time': item.coord_time.strftime("%H:%M:%S %d.%m.%Y"),
        })
    center = [qs.first().coord_x, qs.first().coord_y]
    return {
        'data_list': data_list,
        'center': center
    }
