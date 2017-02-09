# coding=utf-8
from django.contrib import admin

from .models import Message

__author__ = 'alexy'


class MessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'created')


admin.site.register(Message, MessageAdmin)
