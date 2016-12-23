# coding=utf-8
import datetime
from .models import MessageNotify

__author__ = 'alexy'


def message_notification(request):
    user = request.user
    qs = None
    if user.is_authenticated():
        if user.type == 2:
            qs = MessageNotify.objects.filter(moderator=user.moderator_user, is_view=False)
    return {
        'MESSAGE_NOTIFY': qs
    }
