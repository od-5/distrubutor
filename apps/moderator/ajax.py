# coding=utf-8
from annoying.decorators import ajax_request
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from .forms import ReviewForm
from core.models import User
from .models import ModeratorAction

__author__ = 'alexy'


@ajax_request
def moderator_remove(request):
    if request.method == 'GET':
        if request.GET.get('item_id'):
            user = User.objects.get(id=int(request.GET.get('item_id')))
            user.delete()
            return {
                'success': int(request.GET.get('item_id'))
            }
        else:
            return {
                'error': True
            }
    else:
        return {
            'error': True
        }


@ajax_request
def moderator_review_add(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return {
                'success': True
            }
        else:
            return {
                'success': False
            }
    else:
        return {
                'success': False
        }


@ajax_request
def get_action_list(request):
    r_moderator = request.GET.get('moderator', '')
    if r_moderator and r_moderator.isdigit():
        moderatoraction_qs = ModeratorAction.objects.filter(moderator__id=int(r_moderator))
        return {
            'success': True,
            'action_list': [
                {
                    'id': item.id,
                    'name': item.name
                } for item in moderatoraction_qs
            ]
        }

    return {
        'success': False
    }


@ajax_request
def get_cost_by_action(request):
    r_action = request.GET.get('action', '')
    if r_action and r_action.isdigit():
        action = ModeratorAction.objects.get(id=int(r_action))
        return {
            'success': True,
            'cost': action.cost
        }

    return {
        'success': False
    }