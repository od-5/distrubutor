# coding=utf-8
from os import path as op
from os import makedirs
from django.conf import settings
from PIL import Image
from django.core.management.base import BaseCommand, CommandError
from pytils.translit import slugify
import datetime
from apps.distributor.models import PointPhoto

__author__ = 'alexy'


class Command(BaseCommand):

    def handle(self, *args, **options):
        qs = PointPhoto.objects.all()
        list = []
        for instance in qs:
            if not instance.photo.path.endswith('.jpg'):
                list.append(instance)
        if list:
            for instance in list:
                time = (instance.timestamp).strftime("%H-%M")
                name = slugify(','.join(instance.name.split(',')[2:]))
                short_name = slugify(','.join(instance.name.split(',')[3:]))
                filename = "%s-%s%s" % (time, name, '.jpg')
                short_filename = "%s-%s%s" % (time, short_name, '.jpg')
                date = instance.timestamp.strftime("%d-%m-%Y")
                basedir = op.join(instance._meta.app_label, instance._meta.model_name)
                prefix = '/'.join(instance.photo.path.split('/')[:6])
                path = op.join(prefix, basedir, date, filename)
                new_full_path = op.join(prefix, basedir, date, short_filename)
                new_short_path = op.join(basedir, date, short_filename)
                try:
                    image = Image.open(path)
                    image.save(new_full_path, "PNG")
                    print 'image save complete'
                except:
                    print 'image save fail'
                try:
                    print 'set new path for instance'
                    instance.photo = new_short_path
                    instance.save()
                    print 'instance save ok'
                except:
                    print 'instance save fail'