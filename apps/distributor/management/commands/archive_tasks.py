# coding=utf-8
import datetime

from django.core.management.base import BaseCommand
from apps.distributor.models import DistributorTask

__author__ = 'alexy'


class Command(BaseCommand):
    """
    Автозакрытие задач с момента открытия которых прошло 90 дней
    """
    def handle(self, *args, **options):
        search_date = datetime.datetime.now() - datetime.timedelta(days=90)
        DistributorTask.objects.filter(date__lt=search_date, closed=False).update(closed=True)
