# coding=utf-8
from rest_framework import serializers

from apps.geolocation.models import Country, Region, City
from apps.moderator.models import Moderator

__author__ = 'alexy'


class CountrySerializer(serializers.ModelSerializer):
    """
    Сериализация модели страны
    """
    class Meta:
        model = Country
        fields = (
            'id',
            'name'
        )


class RegionSerializer(serializers.ModelSerializer):
    """
    Сериализация модели региона
    """
    class Meta:
        model = Region
        fields = (
            'id',
            'name',
            'country'
        )


class CitySerializer(serializers.ModelSerializer):
    """
    Сериализация модели города
    """
    class Meta:
        model = City
        fields = (
            'id',
            'name',
            'slug',
            'region',
            'country'
        )


class ModeratorSerializer(serializers.ModelSerializer):
    """
    Сериализация модели исполнителя
    """
    class Meta:
        model = Moderator
        fields = (
            'id',
            'company',
            'city',
            'phone',
            'contact',
        )
