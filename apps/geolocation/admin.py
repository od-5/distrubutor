# coding=utf-8
from django.contrib import admin

from .models import Country, City

__author__ = '2mitrij'


class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')


class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')


admin.site.register(Country, CountryAdmin)
admin.site.register(City, CityAdmin)
