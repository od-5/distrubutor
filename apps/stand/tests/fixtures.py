# coding=utf-8
from datetime import datetime

import factory

from apps.moderator.tests.fixtures import ModeratorFactory
from ..models import Stand


class StandFactory(factory.DjangoModelFactory):
    class Meta:
        model = Stand

    moderator = factory.SubFactory(ModeratorFactory)
    name = u'Стэнд'
    date_start = factory.LazyFunction(datetime.now)
    date_end = factory.LazyFunction(datetime.now)
