# coding=utf-8
from django.contrib import admin

from .models import GPSPoint, PointPhoto, DistributorTask

__author__ = 'alexy'


class PointPhotoInline(admin.TabularInline):
    model = PointPhoto


class GPSPointAdmin(admin.ModelAdmin):
    list_display = ('name', 'count', 'comment', 'coord_x', 'coord_y')
    inlines = [
        PointPhotoInline,
    ]


admin.site.register(PointPhoto)
admin.site.register(DistributorTask)
admin.site.register(GPSPoint, GPSPointAdmin)
