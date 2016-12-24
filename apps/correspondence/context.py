# coding=utf-8
import datetime
from .models import UserMessage

__author__ = 'alexy'


def message_notification(request):
    user = request.user
    qs = None
    if user.is_authenticated():
        if user.type == 2:
            qs = UserMessage.objects.filter(recipient=user, is_view=False)
    return {
        'MESSAGE_NOTIFY': qs
    }
