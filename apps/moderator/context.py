# coding=utf-8
import datetime

from core.models import User

__author__ = 'alexy'


def deny_notification(request):
    user = request.user
    message = None
    if user.is_authenticated():
        today = datetime.date.today()
        deny_date = None
        if user.type == User.UserType.moderator and user.moderator_user.deny_date:
            deny_date = user.moderator_user.deny_date
        elif user.type == User.UserType.manager and user.manager_user.moderator.moderator_user.deny_date:
            deny_date = user.manager_user.moderator.moderator_user.deny_date
        if deny_date:
            delta = deny_date - today
            if delta.days <= 5:
                message = u'До окончания действия подписки осталось дней: %s' % delta.days
    return {
        'DENY_NOTIFY': message
    }
