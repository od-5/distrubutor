# coding=utf-8
from pytils.translit import slugify

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models

import core.geotagging as api

__author__ = '2mitrij'

api_key = settings.YANDEX_MAPS_API_KEY


class Country(models.Model):
    class Meta:
        verbose_name = u'Страна'
        verbose_name_plural = u'Страны'
        app_label = 'geolocation'

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('country:update', args=(self.pk,))

    name = models.CharField(max_length=100, verbose_name=u'Название')
    code = models.CharField(max_length=10, verbose_name=u'Код')


class Region(models.Model):
    class Meta:
        verbose_name = u'Регион'
        verbose_name_plural = u'Регионы'
        app_label = 'geolocation'

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('region:update', args=(self.pk,))

    name = models.CharField(max_length=100, verbose_name=u'Название')
    country = models.ForeignKey(Country, verbose_name=u'Страна')


class City(models.Model):
    class Meta:
        verbose_name = u'Город'
        verbose_name_plural = u'Города'
        app_label = 'geolocation'

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('city:update', args=(self.pk,))

    def save(self, *args, **kwargs):
        address = u'город %s' % self.name
        pos = api.geocode(api_key, address)
        self.slug = slugify(self.name)
        self.coord_x = float(pos[0])
        self.coord_y = float(pos[1])
        super(City, self).save()

    TIME_ZONE_CHOICE = (
        (0, 0),
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 7),
        (8, 8),
        (9, 9),
        (10, 10),
        (11, 11),
        (12, 12),
    )

    country = models.ForeignKey(to=Country, verbose_name=u'Страна', blank=True, null=True, on_delete=models.SET_NULL)
    region = models.ForeignKey(Region, verbose_name=u'Регион', blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=100, verbose_name=u'Название')
    slug = models.SlugField(max_length=100, verbose_name=u'URL', blank=True, null=True)
    coord_x = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, verbose_name=u'Ширина')
    coord_y = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, verbose_name=u'Долгота')
    timezone = models.SmallIntegerField(
        verbose_name=u'Часовой пояс',
        choices=TIME_ZONE_CHOICE,
        default=TIME_ZONE_CHOICE[0][0]
    )
