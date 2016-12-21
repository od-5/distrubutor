# coding: utf-8
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

__author__ = 'alexy'


def administrator_required(f):
    """
    Декоратор, который проверяет - авторизировался ли пользователь
    и является ли он админинстратором
    """
    def wrapped_f(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated():
            if user.type != 1:
                return HttpResponseRedirect(reverse('dashboard:index'))
            return f(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('login'))
    return wrapped_f
