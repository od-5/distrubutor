# coding=utf-8
from annoying.decorators import ajax_request
from annoying.functions import get_object_or_None
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView
from .forms import ModeratorForm
from .models import Moderator
from core.forms import UserAddForm, UserUpdateForm
from core.models import User

__author__ = 'alexy'


class ModeratorListView(ListView):
    queryset = User.objects.filter(type=2)
    template_name='moderator/moderator_list.html'
    paginate_by = 50

    def get_queryset(self):
        qs = User.objects.filter(type=2)
        if self.request.GET.get('email'):
            qs = qs.filter(email=self.request.GET.get('email'))
        if self.request.GET.get('last_name'):
            qs = qs.filter(last_name=self.request.GET.get('last_name'))
        if self.request.GET.get('first_name'):
            qs = qs.filter(first_name=self.request.GET.get('first_name'))
        if self.request.GET.get('patronymic'):
            qs = qs.filter(patronymic=self.request.GET.get('patronymic'))
        if self.request.GET.get('phone'):
            qs = qs.filter(phone=self.request.GET.get('phone'))
        return qs

    def get_context_data(self, **kwargs):
        context = super(ModeratorListView, self).get_context_data(**kwargs)
        context.update({
            'r_email': self.request.GET.get('email', ''),
            'r_last_name': self.request.GET.get('last_name', ''),
            'r_first_name': self.request.GET.get('first_name', ''),
            'r_patronymic': self.request.GET.get('patronymic', ''),
            'r_phone': self.request.GET.get('phone', '')
        })
        return context


@login_required()
def moderator_add(request):
    context = {}
    if request.method == "POST":
        form = UserAddForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.type = 2
            user.is_staff = True
            user.is_active = True
            user.save()
            return HttpResponseRedirect(reverse('moderator:update', args=(user.id,)))
            # return HttpResponseRedirect(reverse('moderator:list'))
        else:
            context.update({
                'error': u'Проверьте правильность ввода полей'
            })
    else:
        form = UserAddForm()
    context.update({
        'form': form,
    })
    return render(request, 'moderator/moderator_add.html', context)


def moderator_view(request, pk):
    context = {}
    user = User.objects.get(pk=int(pk))
    success_msg = u''
    error_msg = u''
    try:
        moderator = Moderator.objects.get(user=user)
    except:
        moderator = Moderator(user=user)
        moderator.save()
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        if user_form.is_valid():
            user_form.save()
            success_msg += u' Изменения успешно сохранены'
        else:
            error_msg = u'Проверьте правильность ввода полей!'
    else:
        user_form = UserUpdateForm(instance=user)
    moderator_form = ModeratorForm(instance=moderator)
    context.update({
        'user_form': user_form,
        'moderator_form': moderator_form,
        'success': success_msg,
        'error': error_msg,
        'object': moderator
    })
    return render(request, 'moderator/moderator_update.html', context)



@ajax_request
def moderator_update(request):
    if request.method == 'POST':
        try:
            moderator = Moderator.objects.get(moderator=int(request.POST.get('moderator')))
        except:
            return {
                'error': True
            }
        form = ModeratorForm(request.POST, instance=moderator)
        if form.is_valid():
            form.save()
            return {
                'success': True
            }
        else:
            print form
            return {
                'error': True
            }
    return {
        'error': True
    }
