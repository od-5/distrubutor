# coding=utf-8
import factory

from core.tests.fixtures import UserFactory
from core.models import User
from apps.geolocation.tests.fixtures import CityFactory
from apps.packages.tests.fixtures import PackageFactory
from ..models import Moderator, Review, ModeratorArea, Order


class ModeratorFactory(factory.DjangoModelFactory):
    class Meta:
        model = Moderator

    company = u'Компания'
    user = factory.SubFactory(UserFactory, type=User.UserType.moderator)


class ReviewFactory(factory.DjangoModelFactory):
    class Meta:
        model = Review

    moderator = factory.SubFactory(ModeratorFactory)
    name = u'Имя'
    mail = 'example@example.el'


class ModeratorAreaFactory(factory.DjangoModelFactory):
    class Meta:
        model = ModeratorArea

    city = factory.SubFactory(CityFactory)
    moderator = factory.SubFactory(ModeratorFactory)
    name = u'Район'


class OrderFactory(factory.DjangoModelFactory):
    class Meta:
        model = Order

    moderator = factory.SubFactory(ModeratorFactory)
    package = factory.SubFactory(PackageFactory)
