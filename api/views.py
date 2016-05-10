# coding=utf-8
import json
import datetime
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from api.serializers import UserSerializer, DistributorTaskSerializer, GPSPointSerializer, PointPhotoSerializer
from core.common import str_to_bool
from core.models import User
from apps.distributor.models import Distributor, DistributorTask, GPSPoint

__author__ = 'alexy'


@api_view(['GET', ])
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
        if request.data.get('closed'):
            task.closed = str_to_bool(request.data.get('closed'))
            task.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def gpspoint_add(request):
    if request.method == 'POST':
        try:
            serializer = GPSPointSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'point': serializer.instance.id}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
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
    try:
        serializer = PointPhotoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
