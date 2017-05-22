# coding=utf-8
from core.models import User
from .models import UserMessage

__author__ = 'alexy'


def message_notification(request):
    user = request.user
    qs = UserMessage.objects.select_related('recipient').only('recipient')
    if user.is_authenticated():
        if user.type == User.UserType.moderator:
            qs = qs.filter(recipient=user, is_view=False)
        elif user.type == User.UserType.administrator or user.type == User.UserType.agency:
            qs = qs.filter(
                usermessageanswer__recipient=user, usermessageanswer__is_view=False)
    return {
        'MESSAGE_NOTIFY': qs
    }
