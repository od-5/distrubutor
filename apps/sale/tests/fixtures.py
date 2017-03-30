# coding=utf-8
from datetime import datetime

import factory

from core.models import User
from core.tests.fixtures import UserFactory
from apps.moderator.tests.fixtures import ModeratorFactory
from apps.geolocation.tests.fixtures import CityFactory
from ..models import Sale, SaleOrder


class SaleFactory(factory.DjangoModelFactory):
    class Meta:
        model = Sale

    user = factory.SubFactory(UserFactory, type=User.UserType.client)
    moderator = factory.SubFactory(ModeratorFactory)
    city = factory.SubFactory(CityFactory)
    legal_name = u'Клиент'


class SaleOrderFactory(factory.DjangoModelFactory):
    class Meta:
        model = SaleOrder

    sale = factory.SubFactory(SaleFactory)
    date_start = factory.LazyFunction(datetime.now)
