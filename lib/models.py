# coding=utf-8
class ChoiceItem(object):
    """
    Класс для определения наборов перечислений.
    """
    def __init__(self, value, name):
        self.name = name
        self.value = value

    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        raise AttributeError


class Choices(object):
    """
    Класс для определения перечислений в полях моделей.
    """
    class ChoicesDescriptor(object):
        def __get__(self, instance, owner):
            attrs_dict = owner._get_choiceitem_attrs()
            return tuple([
                tuple([
                    attrs_dict[attr_key].value,
                    attrs_dict[attr_key].name
                ]) for attr_key in attrs_dict.keys()
            ])

        def __set__(self, instance, value):
            raise AttributeError

    class LabelsDescriptor(object):
        def __get__(self, instance, owner):
            attrs_dict = owner._get_choiceitem_attrs()
            return {attrs_dict[attr_key].value: attr_key for attr_key in attrs_dict.keys()}

        def __set__(self, instance, value):
            raise AttributeError

    choices = ChoicesDescriptor()
    labels = LabelsDescriptor()

    @classmethod
    def _get_choiceitem_attrs(cls):
        """
        Возвращает словарь с атрибутами, являющимися экземплярами ChoiceItem, включая унаследованные.
        """
        all_attrs = {
            attr_key: cls.__dict__[attr_key] for attr_key in cls.__dict__.keys() if isinstance(
                cls.__dict__[attr_key], ChoiceItem)
        }
        for base_cls in cls.__bases__:
            if issubclass(base_cls, Choices):
                all_attrs.update(base_cls._get_choiceitem_attrs())
        return all_attrs

    def __getattribute__(self, attr):
        attr_instance = object.__getattribute__(self, attr)
        if attr_instance.__class__ is ChoiceItem:
            return attr_instance.value

        return attr_instance
