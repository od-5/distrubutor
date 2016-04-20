# coding=utf-8
from django import forms
from django.contrib import admin
from .models import GPSPoint, PointPhoto

__author__ = 'alexy'


class PointPhotoInline(admin.TabularInline):
    model = PointPhoto


class GPSPointAdmin(admin.ModelAdmin):
    list_display = ('name', 'coord_x', 'coord_y')
    inlines = [
        PointPhotoInline,
    ]


admin.site.register(GPSPoint, GPSPointAdmin)
