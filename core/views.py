# coding=utf-8
from annoying.decorators import ajax_request
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import UpdateView
from core.forms import UserUpdateForm, SetupForm
from core.models import User, Setup

__author__ = 'alexy'


def cms_login(request, usertype=None):
    error = None
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('dashboard:index'))
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            try:
                user = authenticate(username=username, password=password)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return HttpResponseRedirect(reverse('dashboard:index'))
                        # return HttpResponseRedirect('/')
                    else:
                        error = u'Пользователь заблокирован'
                else:
                    error = u'Вы ввели неверный e-mail или пароль'
            except:
                if usertype == 2:
                    error = u'Модератора с таким e-mail не зарегистрировано в системе. Проверьте правильность ввода даных.'
                elif usertype == 3:
                    error = u'Клиента с таким e-mail не зарегистрировано в системе. Проверьте правильность ввода даных.'
                elif usertype == 4:
                    error = u'Исполнителя с таким e-mail не зарегистрировано в системе. Проверьте правильность ввода даных.'
                elif usertype == 5:
                    error = u'Менеджера с таким e-mail не зарегистрировано в системе. Проверьте правильность ввода даных.'
        context = {'error': error}
        return render(request, 'core/login.html', context)


@ajax_request
def password_change(request):
    user_id = request.POST.get('user_id')
    password1 = request.POST.get('password1')
    password2 = request.POST.get('password2')
    try:
        user = User.objects.get(pk=int(user_id))
        if password1 and password2 and password1 == password2:
            user.set_password(password1)
            user.save()
            return {
                'success': u'Ваш пароль был успешно изменён'
            }
        else:
            return {
                'error': u'Введённые пароли не совпадают'
            }
    except:
        return {
            'error': u'Произошла ошибка. Обновите страницу и попробуйте ещё раз'
        }


def setup_view(request):
    context = {}
    try:
        instance = Setup.objects.first()
    except:
        instance = Setup(meta_title=u'Рекламное агенство Дружба', email=u'direktor@vlifte.pro')
        instance.save()
    if request.method == 'POST':
        form = SetupForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
        else:
            context.update({
                'error': u'Проверьте правильность ввода данных'
            })
    else:
        form = SetupForm(instance=instance)
    context.update({
        'form': form
    })
    return render(request, 'core/site_setup.html', context)


def get_robots_txt(request):
    """
    Функция отображения robots.txt
    """
    try:
        setup = Setup.objects.first()
        content = setup.robots_txt
    except:
        content = u'User-agent: *'
    robots_response = HttpResponse(content, content_type='text/plain')
    return robots_response


class UserUpdateView(UpdateView):
    model = User
    template_name = 'core/profile.html'
    form_class = UserUpdateForm
    # success_url = '/profile/'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('profile')
