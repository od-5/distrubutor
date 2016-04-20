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
from apps.distributor.models import Distributor, DistributorTask

__author__ = 'alexy'


@api_view(['GET', ])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def api_root(request, format=None):
    """
    Точка входа в Api.
    Получение данных авторизованного пользователя
    """
    print 'point 1'
    user = request.user
    if request.method == 'GET':
        print 'point GET'
        try:
            Distributor.objects.get(user=user)
            print 'point TRY'
        except Distributor.DoesNotExist:
            print 'point EXCEPT'
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        print 'point serializer'
        return Response(serializer.data)


@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def task_list(request):
    """
    Получение списка задач авторизованного пользователя(распространителя)
    """
    user = request.user
    print user
    if request.method == 'GET':
        tasks = user.distributor_user.distributortask_set.filter(closed=False)
        if not tasks:
            print len(tasks)
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
        print 'request.method = POST'
        try:
            print request.data
            serializer = GPSPointSerializer(data=request.data)
            print serializer
            print 'end serializer'
            if serializer.is_valid():
                serializer.save()
                print serializer.instance.id
                return Response({'point': serializer.instance.id}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)
        except:
            print 'except'
            return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def photo_add(request):
    print 'start'
    try:
        print request.data
        print 'serializer'
        serializer = PointPhotoSerializer(data=request.data)
        print serializer
        print 'end serializer'
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)
    except:
        print 'except'
        return Response(status=status.HTTP_400_BAD_REQUEST)
