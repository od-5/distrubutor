# coding=utf-8
import uuid
from datetime import datetime
from os import path as op
from pytils.translit import slugify


__author__ = 'aser'


def upload_to(instance, filename, prefix=None):
        """
        Auto generate name for File and Image fields.
        :param instance: Instance of Model
        :param filename: Name of uploaded file
        :param prefix: Add to path
        :return:
        """
        name, ext = op.splitext(filename)
        filename = "%s%s" % (uuid.uuid4(), ext or '.jpg')
        basedir = op.join(instance._meta.app_label, instance._meta.model_name)
        if prefix:
            basedir = op.join(basedir, prefix)
        return op.join(basedir, filename[:2], filename[2:4], filename)


def pointphoto_upload(instance, filename, prefix=None):
        """
        Auto generate name for File and Image fields.
        :param instance: Instance of Model
        :param filename: Name of uploaded file
        :param prefix: Add to path
        :return:
        """
        name, ext = op.splitext(filename)
        try:
            time = instance.timestamp.strftime("%H-%M")
            if len(instance.name.split(',')) > 2:
                instance.name = ','.join(instance.name.split(',')[2:])
            name = slugify(instance.name)
            filename = "%s-%s%s" % (time, name, ext or '.jpg')
            date = instance.timestamp.strftime("%d-%m-%Y")
        except:
            filename = "%s%s" % (uuid.uuid4(), ext or '.jpg')
            date = datetime.today().strftime('%d-%m-%Y')
        basedir = op.join(instance._meta.app_label, instance._meta.model_name)
        if prefix:
            basedir = op.join(basedir, prefix)
        return op.join(basedir, date, filename)
