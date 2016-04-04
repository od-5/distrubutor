# coding=utf-8
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
import core.geotagging as api

__author__ = 'alexy'

api_key = settings.YANDEX_MAPS_API_KEY


class City(models.Model):
    class Meta:
        verbose_name = u'Город'
        verbose_name_plural = u'Города'
        app_label = 'city'

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('city:update', args=(self.pk,))

    def save(self, *args, **kwargs):
        address = u'город %s' % self.name
        pos = api.geocode(api_key, address)
        self.coord_x = float(pos[0])
        self.coord_y = float(pos[1])
        super(City, self).save()

    name = models.CharField(max_length=100, verbose_name=u'Город')
    coord_x = models.DecimalField(max_digits=8, decimal_places=6, blank=True, null=True, verbose_name=u'Ширина')
    coord_y = models.DecimalField(max_digits=8, decimal_places=6, blank=True, null=True, verbose_name=u'Долгота')

