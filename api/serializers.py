# coding=utf-8
from rest_framework import serializers
from core.models import User
from apps.distributor.models import Distributor, DistributorTask, GPSPoint, PointPhoto
from apps.sale.models import Questionary, QuestionaryAnswer, QuestionaryQuestion

__author__ = 'alexy'


class QuestionaryAnswerSerializer(serializers.ModelSerializer):
    """
    Сериализация модели вопроса анкеты
    """
    class Meta:
        model = QuestionaryAnswer
        fields = (
            'id',
            'text'
        )


class QuestionaryQuestionSerializer(serializers.ModelSerializer):
    """
    Сериализация модели вопроса анкеты
    """
    answers = QuestionaryAnswerSerializer(many=True, read_only=True)

    class Meta:
        model = QuestionaryQuestion
        fields = (
            'id',
            'text',
            'question_type',
            'answers'
        )


class QuestionarySerializer(serializers.ModelSerializer):
    """
    Сериализация модели анкеты
    """
    questions = QuestionaryQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Questionary
        fields = (
            'id',
            'title',
            'questions'
        )


class DistributorSerializer(serializers.ModelSerializer):
    """
    Сериализация модели исполнителя
    """

    class Meta:
        model = Distributor
        fields = (
            'id',
            'user',
            'moderator',
            'coord_x',
            'coord_y',
            'coord_time'
        )


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализация модели пользователя
    """
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'last_name',
            'first_name',
            'patronymic',
            'phone'
        )


class DistributorTaskSerializer(serializers.ModelSerializer):
    """
    Сериализация модели задач
    """

    class Meta:
        model = DistributorTask
        fields = (
            'id',
            'distributor',
            'get_sale_name',
            'get_sale_city',
            'get_area_name',
            'get_type_display',
            'category',
            'material_count',
            'date',
            'coord_x',
            'coord_y',
            'radius',
            'start_time',
            'end_time',
            'comment',
            'define_address',
            'closed',
            'get_questionary'
        )


class GPSPointSerializer(serializers.ModelSerializer):
    """
    Сериализация модели GPS точек
    """
    class Meta:
        model = GPSPoint
        fields = (
            'task',
            'count',
            'comment',
            'coord_x',
            'coord_y',
            'name',
        )


class PointPhotoSerializer(serializers.ModelSerializer):
    """
    Сериализация модели фотографий
    """
    class Meta:
        model = PointPhoto
        fields = (
            'point',
            'photo'
        )
