# coding=utf-8
try:
    import pytz
except ImportError:
    pytz = None
from calendar import LocaleHTMLCalendar
from datetime import datetime
from itertools import groupby
import _locale

from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.timezone import UTC

__author__ = 'alexy'


def next_month(origin_date):
    month = origin_date.month
    year = origin_date.year
    if origin_date.month == 12:
        return datetime(year + 1, 1, 1)
    else:
        return datetime(year, month + 1, 1)


def get_months():
    # получаем значение текущего месяца
    utc = pytz.utc if pytz else UTC()
    if settings.USE_TZ:
        current = datetime.utcnow().replace(tzinfo=utc)
    else:
        current = datetime.now()
    date1 = next_month(current)
    date2 = next_month(date1)
    date3 = next_month(date2)
    return {
        'months': [current, date1, date2, date3],
    }


class TaskCalendar(LocaleHTMLCalendar):
    def __init__(self, tasks, locale=None):
        super(TaskCalendar, self).__init__()
        self.tasks = self.group_by_day(tasks)
        if locale is None:
            locale = _locale.getdefaultlocale()
        self.locale = locale

    def formatday(self, day, weekday):
        if day != 0:
            cssclass = self.cssclasses[weekday]
            # if date.today() == date(self.year, self.month, day):
            #     cssclass += ' today'
            if day in self.tasks:
                cssclass += ' filled'
                # body = ['<ul>']
                # for workout in self.workouts[day]:
                #     body.append('<li>')
                #     body.append('<a href="%s">' % workout.id)
                #     body.append(workout.name)
                #     body.append('</a></li>')
                # body.append('</ul>')
                url = reverse('distributor:task-list')
                return self.day_cell(cssclass, '<a href="%s?date__day=%d&date__month=%d&date__year=%d">%d</a>' % (
                    url, day, self.month, self.year, day))
            return self.day_cell(cssclass, day)
        return self.day_cell('noday', '&nbsp;')

    def formatmonth(self, year, month):
        self.year, self.month = year, month
        return super(TaskCalendar, self).formatmonth(year, month)

    def group_by_day(self, tasks):
        field = lambda task: task.date.day
        return dict(
            [(day, list(items)) for day, items in groupby(tasks, field)]
        )

    def day_cell(self, cssclass, body):
        return '<td class="%s">%s</td>' % (cssclass, body)
