# coding=utf-8
import factory

from core.models import User
from core.tests.fixtures import UserFactory
from apps.moderator.tests.fixtures import ModeratorFactory
from apps.moderator.models import Moderator
from ..models import Manager


class ManagerFactory(factory.DjangoModelFactory):
    class Meta:
        model = Manager

    user = factory.SubFactory(UserFactory, type=User.UserType.manager)
    moderator = factory.SubFactory(UserFactory, type=User.UserType.moderator)

    @classmethod
    def _after_postgeneration(cls, obj, create, results=None):
        super(ManagerFactory, cls)._after_postgeneration(obj, create, results)

        if obj.moderator and not Moderator.objects.filter(user=obj.moderator).exists():
            ModeratorFactory(user=obj.moderator)
