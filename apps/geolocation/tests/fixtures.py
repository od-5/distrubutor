# coding=utf-8
import factory

from ..models import City


class CityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = City

    name = u'Город'
