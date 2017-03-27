# coding=utf-8
import factory

from core.models import User
from core.tests.fixtures import UserFactory
from ..models import Manager


class ManagerFactory(factory.DjangoModelFactory):
    class Meta:
        model = Manager

    user = factory.SubFactory(UserFactory, type=User.UserType.manager)
