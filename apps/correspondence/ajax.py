# coding=utf-8
from annoying.decorators import ajax_request

from django.views.decorators.csrf import csrf_exempt

from apps.moderator.models import Moderator

__author__ = 'alexy'


@csrf_exempt
@ajax_request
def find_moderators(request):
    if request.GET.get('city'):
        moderator_list = []
        moderator_qs = Moderator.objects.filter(city=int(request.GET.get('city')))
        for moderator in moderator_qs:
            moderator_list.append({
                'id': moderator.id,
                'name': moderator.__unicode__()
            })
        return {
            'success': True,
            'moderator_list': moderator_list
        }
    return {
        'success': False
    }
