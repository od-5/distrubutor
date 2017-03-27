# coding=utf-8
import factory

from core.tests.fixtures import UserFactory
from core.models import User
from ..models import Moderator


class ModeratorFactory(factory.DjangoModelFactory):
    class Meta:
        model = Moderator

    company = u'Компания'
    user = factory.SubFactory(UserFactory, type=User.UserType.moderator)
