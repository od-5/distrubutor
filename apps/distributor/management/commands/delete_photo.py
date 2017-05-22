# coding=utf-8
from django.core.management.base import BaseCommand, CommandError
import datetime
from apps.distributor.models import PointPhoto

__author__ = 'alexy'


class Command(BaseCommand):

    def handle(self, *args, **options):
        search_date = datetime.datetime.now() - datetime.timedelta(days=60)
        qs = PointPhoto.objects.filter(timestamp__lt=search_date)
        if qs:
            qs.delete()
