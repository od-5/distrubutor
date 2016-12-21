# coding=utf-8
from django.core.management.base import BaseCommand, CommandError
from pytils.translit import slugify
import datetime
from apps.moderator.models import Moderator

__author__ = 'alexy'


class Command(BaseCommand):

    def handle(self, *args, **options):
        Moderator.objects.filter(deny_date__lt=datetime.date.today(), deny_access=False).update(deny_access=True)


