# coding=utf-8
import datetime
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Stand, StandItem
from .forms import StandForm

__author__ = 'alexy'


class StandCreateView(CreateView):
    """
    Создание новой вёрстки
    """
    models = Stand
    form_class = StandForm
    template_name = 'stand/stand_add.html'

    def get_form_kwargs(self):
        kwargs = super(StandCreateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        self.object = form.save()
        today = datetime.date.today()
        # создание вёрстки по умолчанию.
        # todo: подумать над более элегантным способом
        StandItem.objects.bulk_create([
            StandItem(created=today, stand=self.object, side='front', position='top',
                      width=120, height=150, top=0, left=160),
            StandItem(created=today, stand=self.object, side='front', position='top',
                      width=120, height=150, top=0, left=280),
            StandItem(created=today, stand=self.object, side='front', position='bottom',
                      width=200, height=120, top=0, left=0),
            StandItem(created=today, stand=self.object, side='front', position='bottom',
                      width=200, height=120, top=0, left=200),
            StandItem(created=today, stand=self.object, side='front', position='bottom',
                      width=200, height=120, top=120, left=0),
            StandItem(created=today, stand=self.object, side='front', position='bottom',
                      width=200, height=120, top=120, left=200),
            StandItem(created=today, stand=self.object, side='front', position='bottom',
                      width=200, height=120, top=240, left=0),
            StandItem(created=today, stand=self.object, side='front', position='bottom',
                      width=200, height=120, top=240, left=200),
            StandItem(created=today, stand=self.object, side='front', position='bottom',
                      width=200, height=120, top=360, left=0),
            StandItem(created=today, stand=self.object, side='front', position='bottom',
                      width=200, height=120, top=360, left=200),
            StandItem(created=today, stand=self.object, side='back', position='top',
                      width=120, height=150, top=0, left=160),
            StandItem(created=today, stand=self.object, side='back', position='top',
                      width=120, height=150, top=0, left=280),
            StandItem(created=today, stand=self.object, side='back', position='bottom',
                      width=200, height=120, top=0, left=0),
            StandItem(created=today, stand=self.object, side='back', position='bottom',
                      width=200, height=120, top=0, left=200),
            StandItem(created=today, stand=self.object, side='back', position='bottom',
                      width=200, height=120, top=120, left=0),
            StandItem(created=today, stand=self.object, side='back', position='bottom',
                      width=200, height=120, top=120, left=200),
            StandItem(created=today, stand=self.object, side='back', position='bottom',
                      width=200, height=120, top=240, left=0),
            StandItem(created=today, stand=self.object, side='back', position='bottom',
                      width=200, height=120, top=240, left=200),
            StandItem(created=today, stand=self.object, side='back', position='bottom',
                      width=200, height=120, top=360, left=0),
            StandItem(created=today, stand=self.object, side='back', position='bottom',
                      width=200, height=120, top=360, left=200)

        ])
        return HttpResponseRedirect(self.object.get_absolute_url())


class StandUpdateView(UpdateView):
    model = Stand
    template_name = 'stand/stand_form.html'
    form_class = StandForm

    def get_form_kwargs(self):
        kwargs = super(StandUpdateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(StandUpdateView, self).get_context_data(**kwargs)
        front_top = self.object.standitem_set.filter(side='front', position='top')
        front_bottom = self.object.standitem_set.filter(side='front', position='bottom')
        back_top = self.object.standitem_set.filter(side='back', position='top')
        back_bottom = self.object.standitem_set.filter(side='back', position='bottom')
        context.update({
            'front_top': front_top,
            'front_bottom': front_bottom,
            'back_top': back_top,
            'back_bottom': back_bottom
        })
        return context


class StandListView(ListView):
    """
    Список рекламных вёрсток
    """
    model = Stand
    paginate_by = 25
    template_name = 'stand/stand_list.html'

    def get_queryset(self):
        user = self.request.user
        if user.type == 1:
            qs = Stand.objects.all()
        elif user.type == 2:
            if user.superviser:
                qs = Stand.objects.filter(Q(moderator__superviser=user) | Q(moderator=user.moderator_user))
            else:
                qs = Stand.objects.filter(moderator=user.moderator_user)
        elif user.type == 5:
            qs = Stand.objects.filter(moderator=user.manager_user.moderator.moderator_user)
        else:
            qs = None
        if self.request.GET.get('name'):
            qs = qs.filter(name__icontains=self.request.GET.get('name'))
        if self.request.GET.get('date_start'):
            qs = qs.filter(date_start__gte=datetime.datetime.strptime(self.request.GET.get('date_start'), '%d.%m.%Y'))
        if self.request.GET.get('date_end'):
            qs = qs.filter(date_end__lte=datetime.datetime.strptime(self.request.GET.get('date_end'), '%d.%m.%Y'))
        return qs

    def get_context_data(self, **kwargs):
        context = super(StandListView, self).get_context_data(**kwargs)
        if self.request.GET.get('date_start'):
            context.update({
                'r_date_start': self.request.GET.get('date_start')
            })
        if self.request.GET.get('date_end'):
            context.update({
                'r_date_end': self.request.GET.get('date_end')
            })
        return context
