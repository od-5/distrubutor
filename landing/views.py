# coding=utf-8
from annoying.decorators import ajax_request
from annoying.functions import get_object_or_None
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from apps.city.models import City
from apps.moderator.models import Moderator
from core.models import Setup

__author__ = 'alexy'


class LandingView(TemplateView):
    template_name = 'landing/index.html'

    def get_context_data(self, **kwargs):
        try:
            self.request.session['current_city']
        except:
            self.request.session['current_city'] = City.objects.first().id
        try:
            current_city = City.objects.get(pk=int(self.request.session['current_city']))
        except:
            current_city = None
        setup = Setup.objects.first()
        context = {
            'city_list': City.objects.all(),
            'moderator_list': current_city.moderator_set.all(),
            # 'moderator_list': Moderator.objects.all(),
            'current_city': current_city,
            'SETUP': setup
        }
        return context


@csrf_exempt
@ajax_request
def set_current_city(request):
    if request.POST.get('city'):
        print request.POST.get('city')
        try:
            current_city = City.objects.get(name__iexact=request.POST.get('city'))
            print 1
        except:
            current_city = None
            print 2
        print current_city
        request.session['current_city'] = current_city.id
    return {
        'success': True
    }

@csrf_exempt
def set_current_city_from_input(request):
    if request.POST.get('city'):
        print request.POST.get('city')
        try:
            current_city = City.objects.get(name__iexact=request.POST.get('city'))
            request.session['current_city'] = current_city.id
        except:
            pass
    return HttpResponseRedirect(reverse('landing:index'))

# def cms_login(request, usertype=None):
#     error = None
#     if request.user.is_authenticated():
#         return HttpResponseRedirect(reverse('dashboard:index'))
#     else:
#         if request.method == "POST":
#             username = request.POST.get('username')
#             password = request.POST.get('password')
#             try:
#                 user = authenticate(username=username, password=password)
#                 if user is not None:
#                     if user.is_active:
#                         login(request, user)
#                         return HttpResponseRedirect(reverse('dashboard:index'))
#                         # return HttpResponseRedirect('/')
#                     else:
#                         error = u'Пользователь заблокирован'
#                 else:
#                     error = u'Вы ввели неверный e-mail или пароль'
#             except:
#                 if usertype == 2:
#                     error = u'Модератора с таким e-mail не зарегистрировано в системе. Проверьте правильность ввода даных.'
#                 elif usertype == 3:
#                     error = u'Клиента с таким e-mail не зарегистрировано в системе. Проверьте правильность ввода даных.'
#                 elif usertype == 4:
#                     error = u'Исполнителя с таким e-mail не зарегистрировано в системе. Проверьте правильность ввода даных.'
#                 elif usertype == 5:
#                     error = u'Менеджера с таким e-mail не зарегистрировано в системе. Проверьте правильность ввода даных.'
#         context = {'error': error}
#         return render(request, 'core/login.html', context)
