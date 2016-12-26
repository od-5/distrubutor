# coding=utf-8
from django.contrib.auth.decorators import login_required
from apps.administrator.decorators import administrator_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import UpdateView, ListView
from core.forms import UserAddForm, UserUpdateForm
from core.models import User

__author__ = 'alexy'


class AgencyListView(ListView):
    queryset = User.objects.filter(type=6)
    template_name = 'agency/agency_list.html'
    paginate_by = 50


@administrator_required
def agency_add(request):
    context = {}
    if request.method == "POST":
        form = UserAddForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.type = 6
            user.is_staff = True
            user.is_active = True
            if request.POST.get('leader'):
                user.agency_leader = True
            user.save()
            return HttpResponseRedirect(reverse('agency:update', args=(user.id,)))
        else:
            context.update({
                'error': u'Проверьте правильность ввода полей'
            })
    else:
        form = UserAddForm()
    context.update({
        'form': form,
    })
    return render(request, 'agency/agency_add.html', context)


@administrator_required
def agency_update(request, pk):
    context = {}
    user = User.objects.get(pk=int(pk))
    success_msg = u''
    error_msg = u''
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            instance = form.save(commit=False)
            if request.POST.get('leader'):
                instance.agency_leader = True
            instance.save()
            success_msg += u' Изменения успешно сохранены'
        else:
            error_msg = u'Проверьте правильность ввода полей!'
    else:
        form = UserUpdateForm(instance=user)
    context.update({
        'success': success_msg,
        'error': error_msg,
        'form': form,
        'object': user
    })
    return render(request, 'agency/agency_update.html', context)
