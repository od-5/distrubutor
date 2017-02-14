# coding=utf-8
from .models import UserMessage

__author__ = 'alexy'


def message_notification(request):
    user = request.user
    qs = None
    if user.is_authenticated():
        if user.type == 2:
            qs = UserMessage.objects.filter(recipient=user, is_view=False)
        elif user.type == 1 or user.type == 6:
            qs = UserMessage.objects.select_related().filter(
                usermessageanswer__recipient=user, usermessageanswer__is_view=False)
    return {
        'MESSAGE_NOTIFY': qs
    }
