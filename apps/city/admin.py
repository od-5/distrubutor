# coding=utf-8
from django.contrib import admin
from .models import Country

__author__ = 'alexy'


class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')


admin.site.register(Country, CountryAdmin)
