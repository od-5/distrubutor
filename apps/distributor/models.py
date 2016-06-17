# coding=utf-8
from PIL import Image
from os import path as op
from django.db import models
from django.conf import settings
from pytils.translit import slugify
from apps.city.models import City
from apps.moderator.models import Moderator, ModeratorArea, ModeratorAction
from apps.sale.models import Sale, SaleOrder
from core.files import upload_to, pointphoto_upload
from core.models import User
import core.geotagging as api

__author__ = 'alexy'


api_key = settings.YANDEX_MAPS_API_KEY


class Distributor(models.Model):
    class Meta:
        verbose_name = u'Распространитель'
        verbose_name_plural = u'Распространители'
        app_label = 'distributor'

    def __unicode__(self):
        return self.user.get_full_name()

    user = models.OneToOneField(
        to=User,
        limit_choices_to={'type': 4},
        verbose_name=u'Пользователь',
        related_name='distributor_user'
    )
    moderator = models.ForeignKey(
        to=Moderator,
        verbose_name=u'Модератор'
    )
    coord_x = models.DecimalField(max_digits=9, decimal_places=6, verbose_name=u'Ширина', blank=True, null=True)
    coord_y = models.DecimalField(max_digits=9, decimal_places=6, verbose_name=u'Долгота', blank=True, null=True)
    coord_time = models.DateTimeField(verbose_name=u'Временная метка', blank=True, null=True)


class DistributorPayment(models.Model):
    class Meta:
        verbose_name = u'Стоимость работы'
        verbose_name_plural = u'Стоимость работ'
        app_label = 'distributor'
        unique_together = (("distributor", "type"),)

    def __unicode__(self):
        return u'Оплата %s' % self.type

    distributor = models.ForeignKey(to=Distributor)
    type = models.ForeignKey(to=ModeratorAction, verbose_name=u'Тип работы')
    cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=u'Олата, руб/шт',
        default=0,
        null=True,
        blank=True
    )


class DistributorTask(models.Model):
    class Meta:
        verbose_name = u'Задача для распространителя'
        verbose_name_plural = u'Задачи для распространителей'
        app_label = 'distributor'

    def __unicode__(self):
        return u'%s, %sшт. %s' % (self.get_type_display(), self.material_count, self.date)

    def get_type_display(self):
        return self.type.name

    def total_cost(self):
        payment = DistributorPayment.objects.get(distributor=self.distributor, type=self.type)
        try:
            return payment.cost * self.material_count
        except:
            return 0

    def get_area_name(self):
        return self.area.name

    def get_sale_name(self):
        return self.sale.legal_name

    def get_sale_city(self):
        return self.sale.city.name

    distributor = models.ForeignKey(
        to=Distributor,
        verbose_name=u'Распространитель'
    )
    sale = models.ForeignKey(
        to=Sale,
        verbose_name=u'Клиент'
    )
    order = models.ForeignKey(
        to=SaleOrder,
        verbose_name=u'Заказ клиента'
    )
    area = models.ForeignKey(
        to=ModeratorArea,
        verbose_name=u'Район'
    )
    type = models.ForeignKey(
        to=ModeratorAction,
        verbose_name=u'Тип задачи',
    )
    material_count = models.PositiveIntegerField(
        verbose_name=u'Кол-во рекламной продукции',
        default=0
    )
    date = models.DateField(
        verbose_name=u'Дата'
    )
    comment = models.TextField(verbose_name=u'Комментарий', blank=True, null=True)
    define_address = models.BooleanField(default=True, verbose_name=u'Определять адреса')
    closed = models.BooleanField(default=False, verbose_name=u'Задача закрыта')


class GPSPoint(models.Model):
    class Meta:
        verbose_name = u'GPS точка'
        verbose_name_plural = u'GPS точки'
        ordering = ['-timestamp', ]
        app_label = 'distributor'

    def __unicode__(self):
        if self.name:
            return self.name
        else:
            return u'%s, %s' % (self.coord_x, self.coord_y)

    def save(self, *args, **kwargs):
        if self.task.define_address:
            try:
                name = api.geocodeName(api_key, self.coord_y, self.coord_x)
                self.name = name
            except:
                self.name = u'%s, %s' % (self.coord_y, self.coord_x)
        else:
            self.name = u'%s, %s' % (self.coord_y, self.coord_x)
        super(GPSPoint, self).save()

    task = models.ForeignKey(to=DistributorTask, verbose_name=u'Задача')
    name = models.CharField(max_length=150, verbose_name=u'Название', blank=True, null=True)
    count = models.PositiveIntegerField(verbose_name=u'Кол-во материала', blank=True, null=True)
    comment = models.TextField(verbose_name=u'Комментарий', blank=True, null=True)
    coord_x = models.DecimalField(max_digits=9, decimal_places=6, verbose_name=u'Ширина')
    coord_y = models.DecimalField(max_digits=9, decimal_places=6, verbose_name=u'Долгота')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name=u'Временная метка')


class PointPhoto(models.Model):
    class Meta:
        verbose_name = u'Фотография'
        verbose_name_plural = u'Фотографии'
        ordering = ['timestamp', ]
        app_label = 'distributor'

    def __unicode__(self):
        return u'Фотография %s' % self.name

    def save(self, *args, **kwargs):
        try:
            self.name = self.point.__unicode__()
        except:
            pass
        super(PointPhoto, self).save()
        if self.photo:
            image = Image.open(self.photo)
            (width, height) = image.size
            size = (800, 800)
            "Max width and height 200"
            if width > 800:
                image.thumbnail(size, Image.ANTIALIAS)
                image.save(self.photo.path, "PNG")

    point = models.ForeignKey(to=GPSPoint, verbose_name=u'GPS точка')
    name = models.CharField(max_length=150, verbose_name=u'Название', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name=u'Временная метка')
    photo = models.ImageField(verbose_name=u'Фотография', upload_to=pointphoto_upload)