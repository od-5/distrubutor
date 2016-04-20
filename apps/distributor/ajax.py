# coding=utf-8
from annoying.decorators import ajax_request
from apps.moderator.models import ModeratorArea
from apps.sale.models import Sale
from .forms import DistributorPaymentForm
from .models import Distributor

__author__ = 'alexy'


@ajax_request
def distributor_payment_update(request):
    if request.method == 'POST':
        print 'method=post'
        r_user = request.POST.get('user')
        distributor = Distributor.objects.get(user=int(r_user))
        form = DistributorPaymentForm(request.POST, instance=distributor)
        if form.is_valid():
            print 'form valid'
            form.save()
            return {
                'success': u'Изменения успешно сохранены.'
            }
        else:
            print 'form invalid'
            print form
            return {
                'error': u'Проверьте правильность ввода данных.'
            }
    else:
        print 'method != post'
        return {
            'error': u'Проверьте правильность ввода данных.'
        }


@ajax_request
def get_distr_and_area_for_sale(request):
    r_sale = request.GET.get('sale')
    distributor_list = []
    area_list = []
    if r_sale:
        sale = Sale.objects.get(pk=int(r_sale))
        distributor_qs = Distributor.objects.filter(moderator=sale.moderator)
        area_qs = ModeratorArea.objects.filter(moderator=sale.moderator, city=sale.city)
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
        print distributor_list
        print area_list

        return {
            'distributor_list': distributor_list,
            'area_list': area_list,
        }
    else:
        return {
            'error': u'Произошла ошибка. Приносим свои извинения. Обновите страницу и попробуйте ещё раз.'
        }
