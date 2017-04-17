# coding=utf-8
import factory

from ..models import Package


class PackageFactory(factory.DjangoModelFactory):
    class Meta:
        model = Package

    name = u'Платежный пакет'
    cost = 100
