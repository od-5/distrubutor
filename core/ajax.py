# coding=utf-8
from annoying.decorators import ajax_request
from django.shortcuts import get_object_or_404
from core.models import User


__author__ = 'alexy'

#
# @ajax_request
# def ymap(request):
#     request.encoding = 'utf-8'
#     if request.is_ajax():
#         query = City.objects.all()
#         try:
#             if request.user.type == 2:
#                 query = query.filter(moderator=request.user)
#         except:
#             pass
#         result = []
#         for item in query:
#             result_json = {}
#             result_json['name'] = u'%s (%s)' % (item.name, item.surface_count())
#             result_json['coord_x'] = float(item.coord_x)
#             result_json['coord_y'] = float(item.coord_y)
#             result.append(result_json)
#         data = result
#     else:
#         data = {'msg': 'fail'}
#     return data
#
#
# @ajax_request
# def ymap_surface(request):
#     user = request.user
#     request.encoding = 'utf-8'
#     if request.is_ajax():
#         if user.type == 1:
#             query = Surface.objects.all()
#         elif user.type == 2:
#             query = Surface.objects.filter(city__moderator=request.user)
#         elif user.type == 5:
#             manager = Manager.objects.get(user=user)
#             query = Surface.objects.filter(city__moderator=manager.moderator)
#         result = []
#         for item in query:
#             result_json = {}
#             result_json['name'] = u'%s %s' % (item.street.name, item.house_number)
#             result_json['porch'] = item.porch_set.count()
#             result_json['coord_x'] = float(item.coord_x)
#             result_json['coord_y'] = float(item.coord_y)
#             result.append(result_json)
#         data = result
#
#     else:
#         data = {'msg': 'fail'}
#     return data


@ajax_request
def ajax_remove_item(request):
    if request.method == 'GET':
        if request.GET.get('item_id') and request.GET.get('item_model'):
            model = request.GET.get('item_model')
            item_id = request.GET.get('item_id')
            # client = Client.objects.get(id=int(request.GET.get('item_id')))
            # user = User.objects.get(pk=client.user.id)
            item = get_object_or_404(eval(model), pk=int(item_id))
            # if model == 'Client':
            #     user = User.objects.get(pk=item.user.id)
            #     user.delete()
            # if model == 'Manager':
            #     user = User.objects.get(pk=item.user.id)
            #     user.delete()
            # if model == 'Adjuster':
            #     user = User.objects.get(pk=item.user.id)
            #     user.delete()
            # if model == 'ClientOrderSurface':
            #     surface = Surface.objects.get(pk=item.surface.id)
            #     surface.free = True
            #     surface.save()
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
