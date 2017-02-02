# coding=utf-8
from annoying.decorators import ajax_request
from django.shortcuts import get_object_or_404
from core.models import User
from apps.manager.models import Manager
from apps.moderator.models import Moderator, ModeratorArea, Review, Order
from apps.distributor.models import Distributor, DistributorTask, GPSPoint
from apps.sale.models import Sale, SaleOrder, SaleMaket
from apps.city.models import City, Country
from apps.client.models import Client, ClientContact, Task
from apps.ticket.models import Ticket
from apps.packages.models import Package
from apps.correspondence.models import Message
from apps.stand.models import Stand

__author__ = 'alexy'


@ajax_request
def ajax_remove_item(request):
    """
    ajax удаление данных
    В GET запросе приходят название модели и id элемента.
    Модели должны быть импортированы в начале файла.
    """
    if request.method == 'GET':
        if request.GET.get('item_id') and request.GET.get('item_model'):
            model = request.GET.get('item_model')
            item_id = request.GET.get('item_id')
            item = get_object_or_404(eval(model), pk=int(item_id))
            if model == 'City':
                if item.moderatorarea_set.all():
                    for area in item.moderatorarea_set.all():
                        area.delete()
            if model == 'Sale':
                if item.saleorder_set.all():
                    for order in item.saleorder_set.all():
                        order.delete()
                if item.salemaket_set.all():
                    for maket in item.salemaket_set.all():
                        maket.delete()
                user = User.objects.get(pk=item.user.id)
                user.delete()
            if model == 'Moderator':
                if item.review_set.all():
                    for review in item.review_set.all():
                        review.delete()
                user = User.objects.get(pk=item.user.id)
                user.delete()
            if model == 'Manager':
                user = User.objects.get(pk=item.user.id)
                user.delete()
            if model == 'Distributor':
                for task in item.distributortask_set.all():
                    task.delete()
                user = User.objects.get(pk=item.user.id)
                user.delete()
            if model == 'Client':
                for contact in item.clientcontact_set.all():
                    contact.delete()
                for task in item.task_set.all():
                    task.delete()
            if model == 'GPSPoint':
                for photo in item.pointphoto_set.all():
                    photo.delete()
            item.delete()
            return {
                'id': int(request.GET.get('item_id')),
                'model': request.GET.get('item_model'),
            }
        else:
            return {
                'error': True
            }
    else:
        return {
            'error': True
        }
