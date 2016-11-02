# coding=utf-8
from annoying.decorators import ajax_request
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from .forms import ReviewForm
from core.models import User

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
