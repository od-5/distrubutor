# coding=utf-8
import factory

from apps.moderator.tests.fixtures import ModeratorFactory
from ..models import Ticket, PreSale


class TicketFactory(factory.DjangoModelFactory):
    class Meta:
        model = Ticket

    moderator = factory.SubFactory(ModeratorFactory)


class PreSaleFactory(factory.DjangoModelFactory):
    class Meta:
        model = PreSale

    ticket = factory.SubFactory(TicketFactory)
    moderator = factory.SubFactory(ModeratorFactory)
    legal_name = u'Название организации'
    commission = 0
