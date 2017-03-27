# coding=utf-8
import factory

from ..models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    type = User.UserType.administrator
    password = '123456'

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        return manager.create_user(*args, **kwargs)

    @factory.lazy_attribute_sequence
    def email(self, n):
        type_name = User.UserType.labels[self.type]
        user_name = '{}{}'.format(type_name, n)
        return '{}@{}.{}'.format(user_name, type_name, type_name[:2])
