# coding=utf-8
from django import template
from apps.distributor.models import DistributorTask
from apps.distributor.task_calendar import TaskCalendar
from apps.manager.models import Manager

register = template.Library()


@register.simple_tag
def calendar(user, year, month):
    task_qs = DistributorTask.objects.select_related('sale', 'distributor').order_by('date').filter(
        date__year=year, date__month=month, closed=False
    )
    if user.type == 2:
        task_qs = task_qs.filter(distributor__moderator=user.moderator_user)
    elif user.type == 4:
        task_qs = task_qs.filter(distributor=user.distributor_user)
    elif user.type == 5:
        if user.manager_user.leader:
            task_qs = task_qs.filter(distributor__moderator=user.manager_user.moderator.moderator_user)
        else:
            task_qs = task_qs.filter(sale__manager=user.manager_user)
    cal = TaskCalendar(task_qs, ('ru_RU', 'UTF-8')).formatmonth(year, month)
    return cal
