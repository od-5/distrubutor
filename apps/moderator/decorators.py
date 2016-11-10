# coding: utf-8
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

__author__ = 'alexy'


def blocked(f):
    """
    Декоратор, который проверяет - авторизировался ли пользователь
    и разрешён ли ему доступ к функционалу системы
    """
    def wrapped_f(request):
        user = request.user
        if user.is_authenticated():
            if user.deny_access:
                # fixme: сделать редирект на рабочий стол
                return HttpResponseRedirect(reverse('dashboard:index'))
            return f(request)
        else:
            return HttpResponseRedirect(reverse('login'))
    return wrapped_f
