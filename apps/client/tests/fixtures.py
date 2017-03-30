# coding=utf-8
from datetime import datetime

import factory

from apps.geolocation.tests.fixtures import CityFactory
from apps.manager.tests.fixtures import ManagerFactory
from apps.moderator.tests.fixtures import ModeratorFactory
from ..models import Client, ClientContact, Task


class ClientFactory(factory.DjangoModelFactory):
    class Meta:
        model = Client

    name = factory.Sequence(lambda n: u'Клиент{}'.format(n))
    moderator = factory.SubFactory(ModeratorFactory)
    manager = factory.SubFactory(ManagerFactory, moderator=factory.SelfAttribute('..moderator.user'))
    city = factory.SubFactory(CityFactory)


class ClientContactFactory(factory.DjangoModelFactory):
    class Meta:
        model = ClientContact

    name = factory.Sequence(lambda n: 'Контактное лицо {}'.format(n))
    phone = factory.Sequence(lambda n: '+7{:0>10d}'.format(n))
    email = factory.Sequence(lambda n: 'contact{}@contact.co'.format(n))


class TaskFactory(factory.DjangoModelFactory):
    class Meta:
        model = Task

    type = Task.TaskType.planned_meet
    client = factory.SubFactory(ClientFactory)
    clientcontact = factory.SubFactory(ClientContactFactory, client=factory.SelfAttribute('..client'))
    manager = factory.SelfAttribute('client.manager')
    date = factory.LazyFunction(datetime.now)
