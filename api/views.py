# coding=utf-8
from __future__ import unicode_literals
import datetime
import logging

from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.conf import settings

import core.geotagging as api
from api.serializers import UserSerializer, DistributorTaskSerializer, GPSPointSerializer, PointPhotoSerializer, DistributorSerializer, \
    QuestionarySerializer, QuestionaryCompletedSerializer, QuestionaryQuestionCompletedSerializer, PointAudioSerializer
from apps.sale.models import Questionary
from apps.distributor.models import Distributor, DistributorTask, GPSPoint

# import the logging library
# Get an instance of a logger
logger = logging.getLogger('django.request')

__author__ = 'alexy'
api_key = settings.YANDEX_MAPS_API_KEY


@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def api_root(request, format=None):
    """
    Точка входа в Api.
    Получение данных авторизованного пользователя
    """
    user = request.user
    if request.method == 'GET':
        try:
            Distributor.objects.get(user=user)
        except Distributor.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        return Response(serializer.data)


@api_view(['PUT'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def confirm_address(request):
    """
    Подтверждение адреса
    """
    address = request.data.get('address')
    point = request.data.get('point')
    logger.error(u'user=%s confirm_address. Address: %s, Point: %s' % (request.user, address, point))
    try:
        item = GPSPoint.objects.get(pk=int(point))
        if address:
            if item.name != address:
                pos = api.geocode(api_key, address)
                coord_y = float(pos[0])
                coord_x = float(pos[1])
                item.coord_x = coord_x
                item.coord_y = coord_y
                item.name = address
                logger.error(u'user=%s confirm_address. coord_x: %s, coord_y: %s' % (request.user, coord_x, coord_y))
                item.save()
                logger.error(u'confirm_address. Save complete')
        context = {
            'point': item.id,
            'address': item.name
        }
        return Response(context, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_205_RESET_CONTENT)


@api_view(['PUT'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def location_view(request):
    if request.method == 'PUT':
        user = request.user
        try:
            distributor = user.distributor_user
            coord_x = request.data.get('coord_x')
            coord_y = request.data.get('coord_y')
            try:
                distributor.coord_x = float(coord_x)
                distributor.coord_y = float(coord_y)
                distributor.coord_time = datetime.datetime.now()
                distributor.save()
                serializer = DistributorSerializer(distributor)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except:
                serializer = DistributorSerializer(distributor)
                return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def task_list(request):
    """
    Получение списка задач авторизованного пользователя(распространителя)
    """
    user = request.user
    if request.method == 'GET':
        tasks = user.distributor_user.distributortask_set.filter(closed=False)
        if not tasks:
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            serializer = DistributorTaskSerializer(tasks, many=True)
            return Response(serializer.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def questionary_detail(request, pk):
    """
    Детализация анкеты по id задачи

    """
    try:
        questionary = Questionary.objects.get(id=pk)
    except Questionary.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = QuestionarySerializer(questionary)
    return Response(serializer.data)


@api_view(['GET', 'PUT'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def task_detail(request, pk):
    """
    Детализация задачи

    """
    try:
        task = DistributorTask.objects.get(id=pk)
    except DistributorTask.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = DistributorTaskSerializer(task)
        return Response(serializer.data)
    if request.method == 'PUT':
        if True in map(lambda x: x in request.data, ('closed', 'start_time', 'end_time')):
            serializer = DistributorTaskSerializer(task, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_304_NOT_MODIFIED)
            # if request.data.get('closed'):
            #     task.closed = str_to_bool(request.data.get('closed'))
            #     task.save()
            #     return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def gpspoint_add(request):
    if request.method == 'POST':
        serializer = GPSPointSerializer(data=request.data)
        logger.error(u'user=%s GPSPoint add. Data: %s' % (request.user, request.data))
        if serializer.is_valid():
            serializer.save()
            context = {
                'point': serializer.instance.id,
                'address': serializer.instance.name
            }
            logger.error(u'user=%s GPSPoint add. coord_x: %s, coord_y: %s, name: %s' % (request.user, serializer.instance.coord_x, serializer.instance.coord_y, serializer.instance.name))
            return Response(context, status=status.HTTP_201_CREATED)
        else:
            return Response({'fail': 'true'}, status=status.HTTP_205_RESET_CONTENT)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def gpspoint_comment(request, pk):
    if request.method == 'GET':
        try:
            point = GPSPoint.objects.get(pk=int(pk))
            serializer = GPSPointSerializer(point)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'PUT':
        try:
            point = GPSPoint.objects.get(pk=int(pk))
            count = request.data.get('count', None)
            comment = request.data.get('comment', None)
            try:
                point.comment = comment
                point.count = count
                point.save()
                serializer = GPSPointSerializer(point)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except:
                serializer = GPSPointSerializer(point)
                return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def photo_add(request):
    logger.error(u'user=%s photo add. request.data= %s' % (request.user, request.data))
    if request.method == 'POST':
        data = request.data.copy()
        # fixme: придумать решение проблемы - на лифтах аналогично
        data['photo'] = '1.jpg'
        serializer = PointPhotoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            logger.error(u'user=%s photo FAIL. request.data= %s' % (request.user, request.data))
            return Response({'fail': 'true'}, status=status.HTTP_205_RESET_CONTENT)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def audio_add(request):
    try:
        serializer = PointAudioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def questionary_completed(request):
    try:
        serializer = QuestionaryCompletedSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            context = {
                'questionary_completed': serializer.instance.id
            }
            return Response(context, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def questionary_completed_answer(request):
    try:
        serializer = QuestionaryQuestionCompletedSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
