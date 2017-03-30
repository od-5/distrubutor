# coding=utf-8
from datetime import datetime

import factory

from core.models import User
from core.tests.fixtures import UserFactory
from apps.moderator.tests.fixtures import ModeratorFactory
from apps.sale.tests.fixtures import SaleFactory, SaleOrderFactory
from ..models import Distributor, DistributorTask


class DistributorFactory(factory.DjangoModelFactory):
    class Meta:
        model = Distributor

    user = factory.SubFactory(UserFactory, type=User.UserType.distributor)
    moderator = factory.SubFactory(ModeratorFactory)


class DistributorTaskFactory(factory.DjangoModelFactory):
    class Meta:
        model = DistributorTask

    distributor = factory.SubFactory(DistributorFactory)
    sale = factory.SubFactory(SaleFactory)
    order = factory.SubFactory(SaleOrderFactory)
    date = factory.LazyFunction(datetime.now)
