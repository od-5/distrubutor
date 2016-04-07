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
from .models import Distributor
from .forms import DistributorAddForm, DistributorUpdateForm
from core.forms import UserAddForm, UserUpdateForm
from core.models import User

__author__ = 'alexy'


class DistributorListView(ListView):
    queryset = User.objects.filter(type=4)
    template_name = 'distributor/distributor_list.html'
    paginate_by = 50

    def get_queryset(self):
        user = self.request.user
        # qs = User.objects.filter(type=4)
        if user.type == 1:
            qs = User.objects.filter(type=4)
        elif user.type == 2:
            # qs = user.moderator_user.distributor_set.all()
            qs = User.objects.filter(distributor_user__moderator=user.moderator_user)
        elif user.type == 5:
            if user.manager_user.leader:
                qs = User.objects.filter(distributor_user__moderator=user.manager_user.moderator.moderator_user)
                # qs = user.manager_user.moderator.moderator_user.distributor_set.all()
            else:
                qs = None
        else:
            qs = None
        if self.request.GET.get('email'):
            qs = qs.filter(email=self.request.GET.get('email'))
        if self.request.GET.get('last_name'):
            qs = qs.filter(last_name=self.request.GET.get('last_name'))
        if self.request.GET.get('first_name'):
            qs = qs.filter(first_name=self.request.GET.get('first_name'))
        if self.request.GET.get('phone'):
            qs = qs.filter(phone=self.request.GET.get('phone'))
        if self.request.GET.get('moderator'):
            qs = qs.filter(distributor_user__moderator__company__iexact=self.request.GET.get('moderator'))
        return qs

    def get_context_data(self, **kwargs):
        context = super(DistributorListView, self).get_context_data(**kwargs)
        context.update({
            'r_email': self.request.GET.get('email', ''),
            'r_last_name': self.request.GET.get('last_name', ''),
            'r_first_name': self.request.GET.get('first_name', ''),
            'r_phone': self.request.GET.get('phone', ''),
            'r_moderator': self.request.GET.get('moderator', '')
        })
        return context


def distributor_add(request):
    context = {}
    user = request.user
    if request.method == "POST":
        u_form = UserAddForm(request.POST)
        d_form = DistributorAddForm(request.POST, user=user)
        if u_form.is_valid() and d_form.is_valid():
            new_user = u_form.save(commit=False)
            new_user.type = 4
            new_user.save()
            distriutor = d_form.save(commit=False)
            distriutor.user = new_user
            distriutor.save()
            return HttpResponseRedirect(reverse('distributor:update', args=(distriutor.id,)))
        else:
            context.update({
                'error': u'Проверьте правильность ввода полей'
            })
    else:
        u_form = UserAddForm()
        d_form = DistributorAddForm(user=user)
    context.update({
        'u_form': u_form,
        'd_form': d_form
    })
    return render(request, 'distributor/distributor_add.html', context)


def distributor_update(request, pk):
    context = {}
    distributor = Distributor.objects.get(pk=int(pk))
    user = distributor.user
    success_msg = u''
    error_msg = u''
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=user)
        d_form = DistributorUpdateForm(request.POST, instance=distributor)
        if u_form.is_valid() and d_form.is_valid():
            u_form.save()
            d_form.save()
            success_msg += u' Изменения успешно сохранены'
        else:
            error_msg = u'Проверьте правильность ввода полей!'
    else:
        u_form = UserUpdateForm(instance=user)
        d_form = DistributorUpdateForm(instance=distributor)

    context.update({
        'success': success_msg,
        'error': error_msg,
        'u_form': u_form,
        'd_form': d_form,
        'object': distributor
    })
    return render(request, 'distributor/distributor_update.html', context)
#
#
# def moderator_view(request, pk):
#     context = {}
#     user = User.objects.get(pk=int(pk))
#     success_msg = u''
#     error_msg = u''
#     try:
#         moderator = Moderator.objects.get(user=user)
#     except:
#         moderator = Moderator(user=user)
#         moderator.save()
#     if request.method == 'POST':
#         user_form = UserUpdateForm(request.POST, instance=user)
#         if user_form.is_valid():
#             user_form.save()
#             success_msg += u' Изменения успешно сохранены'
#         else:
#             error_msg = u'Проверьте правильность ввода полей!'
#     else:
#         user_form = UserUpdateForm(instance=user)
#     moderator_form = ModeratorForm(instance=moderator)
#     context.update({
#         'user_form': user_form,
#         'moderator_form': moderator_form,
#         'success': success_msg,
#         'error': error_msg
#     })
#     return render(request, 'moderator/moderator_update.html', context)
#
#
#
# @ajax_request
# def moderator_update(request):
#     if request.method == 'POST':
#         try:
#             moderator = Moderator.objects.get(moderator=int(request.POST.get('moderator')))
#         except:
#             return {
#                 'error': True
#             }
#         form = ModeratorForm(request.POST, instance=moderator)
#         if form.is_valid():
#             form.save()
#             return {
#                 'success': True
#             }
#         else:
#             print form
#             return {
#                 'error': True
#             }
#     return {
#         'error': True
#     }
