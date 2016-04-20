# coding=utf-8
from PIL import Image
from django.db import models
from django.conf import settings
from apps.city.models import City
from apps.moderator.models import Moderator, ModeratorArea
from apps.sale.models import Sale
from core.files import upload_to
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
    distribution_cost = models.PositiveIntegerField(
        verbose_name=u'Олата за распространение, руб/шт',
        default=0,
        null=True,
        blank=True
    )
    posting_cost = models.PositiveIntegerField(
        verbose_name=u'Олата за расклеивание, руб/шт',
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
        return u'Задача: %s, %sшт. %s' % (self.get_type_display(), self.material_count, self.date)

    def total_cost(self):
        if self.type == 1:
            price = self.distributor.posting_cost
        else:
            price = self.distributor.distribution_cost
        try:
            return price * self.material_count
        except:
            return 0

    def get_area_name(self):
        return self.area.name

    def get_sale_name(self):
        return self.sale.legal_name

    def get_sale_city(self):
        return self.sale.city.name

    TYPE_CHOICES = (
        (0, u'Расклейка'),
        (1, u'Распространение')
    )

    distributor = models.ForeignKey(
        to=Distributor,
        verbose_name=u'Распространитель'
    )
    sale = models.ForeignKey(
        to=Sale,
        verbose_name=u'Клиент'
    )
    area = models.ForeignKey(
        to=ModeratorArea,
        verbose_name=u'Район'
    )
    type = models.PositiveSmallIntegerField(
        verbose_name=u'Тип задачи',
        choices=TYPE_CHOICES,
        default=0
    )
    material_count = models.PositiveIntegerField(
        verbose_name=u'Кол-во рекламной продукции',
        default=0
    )
    date = models.DateField(
        verbose_name=u'Дата'
    )
    comment = models.TextField(verbose_name=u'Комментарий', blank=True, null=True)
    closed = models.BooleanField(default=False)


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
        try:
            print self.coord_x
            print self.coord_y
            name = api.geocodeName(api_key, self.coord_y, self.coord_x)
            print name
            self.name = name
        except:
            pass
        super(GPSPoint, self).save()

    task = models.ForeignKey(to=DistributorTask, verbose_name=u'Задача')
    name = models.CharField(max_length=150, verbose_name=u'Название', blank=True, null=True)
    coord_x = models.DecimalField(max_digits=8, decimal_places=6, verbose_name=u'Ширина')
    coord_y = models.DecimalField(max_digits=8, decimal_places=6, verbose_name=u'Долгота')
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
            self.name = self.point.name
        except:
            pass
        super(PointPhoto, self).save()
        if self.photo:
            image = Image.open(self.photo)
            (width, height) = image.size
            size = (200, 200)
            "Max width and height 200"
            if width > 200:
                image.thumbnail(size, Image.ANTIALIAS)
                image.save(self.photo.path, "PNG")

    point = models.ForeignKey(to=GPSPoint, verbose_name=u'GPS точка')
    name = models.CharField(max_length=150, verbose_name=u'Название', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name=u'Временная метка')
    photo = models.ImageField(verbose_name=u'Фотография', upload_to=upload_to)