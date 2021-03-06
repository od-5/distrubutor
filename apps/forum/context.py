# coding=utf-8
from .models import Notification

__author__ = 'alexy'


def forum_notification(request):
    user = request.user
    if user.is_authenticated():
        qs = Notification.objects.filter(user=user)
    else:
        qs = None
    return {
        'NOTIFICATION_LIST': qs
    }
