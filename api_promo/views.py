# coding=utf-8
import json
import datetime
from django.conf import settings
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import CitySerializer, CountrySerializer, ModeratorSerializer
from apps.geolocation.models import City, Country
from apps.moderator.models import Moderator
# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger('django.request')

__author__ = 'alexy'


@api_view(['GET'])
def country_list(request, format=None):
    """
    Отображение списка стран
    """
    if request.method == 'GET':
        country_qs = Country.objects.all()
        if country_qs:
            serializer = CountrySerializer(country_qs, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def city_list(request, format=None):
    """
    Отображение списка городов
    """
    if request.method == 'GET':
        city_qs = City.objects.all()
        if city_qs:
            serializer = CitySerializer(city_qs, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def moderator_list(request, format=None):
    """
    Отображение списка модераторов
    """
    if request.method == 'GET':
        moderator_qs = Moderator.objects.all()
        if moderator_qs:
            serializer = ModeratorSerializer(moderator_qs, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
