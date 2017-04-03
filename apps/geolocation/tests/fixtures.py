# coding=utf-8
import factory

from ..models import City, Region, Country


class CityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = City

    name = u'Город'


class CountryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Country

    name = u'Страна'


class RegionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Region

    name = u'Регион'
    country = factory.SubFactory(CountryFactory)
