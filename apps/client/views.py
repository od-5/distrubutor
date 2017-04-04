# coding=utf-8
import datetime

from django.db.models import F, Q
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.views.generic import ListView, CreateView, UpdateView
from django.utils import timezone

from lib.cbv import RedirectlessFormMixin, SendUserToFormMixin, PassGetArgsToCtxMixin
from core.models import User
from apps.geolocation.models import City
from apps.manager.models import Manager
from .models import Client, Task, ClientContact, ClientManager
from .forms import ClientAddForm, ClientUpdateForm, TaskForm, ClientContactForm, ClientImportForm

__author__ = 'alexy'


# TODO: придумать как структурировать и улучшить
class ClientListView(ListView, PassGetArgsToCtxMixin):
    model = Client
    template_name = 'client/client_list.html'
    paginate_by = 25
    passed_get_args = (
        'name',
        'phone',
        'contact',
        'manager',
        'city',
        'client_name',
    )

    def get_queryset(self):
        user = self.request.user
        qs = self.model.objects.get_qs(user).select_related('moderator', 'manager', 'city')
        if qs:
            name = self.request.GET.get('name')
            phone = self.request.GET.get('phone')
            contact = self.request.GET.get('contact')
            manager = self.request.GET.get('manager')
            city = self.request.GET.get('city')

            if city and int(city) != 0:
                qs = qs.filter(city=int(city))
            if manager and int(manager) != 0:
                qs = qs.filter(manager=int(manager))
            if name:
                qs = qs.filter(name__icontains=name)
            if phone or contact:
                c_qs = ClientContact.objects.filter(client__in=list(qs.values_list('id', flat=True)))
                if phone:
                    c_qs = c_qs.filter(phone__icontains=phone)
                if contact:
                    c_qs = c_qs.filter(name__icontains=contact)
                qs = qs.filter(id__in=list(c_qs.values_list('id', flat=True)))

        return qs

    def get_context_data(self, **kwargs):
        context = super(ClientListView, self).get_context_data(**kwargs)

        user = self.request.user
        queryset = self.object_list
        manager_client_count = queryset.count()
        search_client_name = self.request.GET.get('client_name')
        if search_client_name:
            if self.request.user.type == User.UserType.manager:
                qs = Client.objects.filter(moderator=user.manager_user.moderator.moderator_user)
            else:
                qs = queryset
            search_client_qs = qs.filter(name__icontains=search_client_name)
            context.update({
                'search_client_list': search_client_qs,
            })

        manager_task_count = 0
        for client in queryset:
            manager_task_count += client.task_set.count()

        context.update({
            'manager_client_count': manager_client_count,
            'manager_task_count': manager_task_count
        })
        if user.type == User.UserType.administrator:
            manager_qs = Manager.objects.filter(user__is_active=True)
            city_qs = City.objects.all()
        elif user.type == User.UserType.moderator:
            manager_qs = Manager.objects.filter(moderator=user, user__is_active=True)
            city_qs = user.moderator_user.city.all()
        elif user.type == User.UserType.manager:
            context.update({
                'current_manager': user.manager_user
            })
            if user.manager_user.leader:
                city_qs = user.manager_user.moderator.moderator_user.city.all()
            else:
                city_qs = None
            manager_qs = Manager.objects.filter(
                moderator=user.manager_user.moderator.moderator_user, user__is_active=True)
        else:
            manager_qs = None
            city_qs = None
        import_form = ClientImportForm()
        context.update({
            'import_form': import_form,
            'manager_list': manager_qs,
            'city_list': city_qs
        })
        return context


class ClientCreateView(CreateView, SendUserToFormMixin, RedirectlessFormMixin):
    form_class = ClientAddForm
    template_name = 'client/client_add.html'

    def form_valid(self, form):
        result = super(ClientCreateView, self).form_valid(form)
        clientmanager = ClientManager(manager=self.object.manager, client=self.object)
        clientmanager.save()
        return result


class ClientUpdateView(UpdateView, SendUserToFormMixin, RedirectlessFormMixin):
    model = Client
    form_class = ClientUpdateForm
    template_name = 'client/client_update.html'

    def form_valid(self, form):
        result = super(ClientUpdateView, self).form_valid(form)
        if 'manager' in form.changed_data:
            self.object.type = Client.ClientType.reported_client
            self.object.save()
            clientmanager = ClientManager(manager=self.object.manager, client=self.object)
            clientmanager.save()
        return result


class ClientManagerHistory(ListView):
    template_name = 'client/clientmanager_history.html'

    def get_queryset(self):
        self.client = get_object_or_404(Client, pk=self.kwargs['pk'])
        return self.client.clientmanager_set.all()

    def get_context_data(self, **kwargs):
        context = super(ClientManagerHistory, self).get_context_data(**kwargs)
        context['object'] = self.client
        return context


class ClientContactListView(ListView):
    template_name = 'client/clientcontact_list.html'

    def get_queryset(self):
        self.client = get_object_or_404(Client, pk=self.kwargs['pk'])
        return self.client.clientcontact_set.all()

    def get_context_data(self, **kwargs):
        context = super(ClientContactListView, self).get_context_data(**kwargs)
        context['object'] = self.client
        return context


class ClientContactCreateView(CreateView):
    form_class = ClientContactForm
    template_name = 'client/clientcontact_add.html'

    def get_initial(self):
        self.client = get_object_or_404(Client, pk=self.kwargs['pk'])
        return {'client': self.client}

    def get_success_url(self):
        return reverse('client:contact-list', args=(self.client.pk,))

    def get_context_data(self, **kwargs):
        context = super(ClientContactCreateView, self).get_context_data(**kwargs)
        context['object'] = self.client
        return context


class ClientContactUpdateView(UpdateView):
    model = ClientContact
    form_class = ClientContactForm
    template_name = 'client/clientcontact_update.html'

    def get_success_url(self):
        return reverse('client:contact-list', args=(self.object.client.pk,))

    def get_context_data(self, **kwargs):
        context = super(ClientContactUpdateView, self).get_context_data(**kwargs)
        context['object'] = self.object.client
        return context


# TODO: придумать как структурировать и улучшить
class ClientTaskListView(ListView):
    model = Task
    template_name = 'client/task_list.html'
    paginate_by = 25

    def get_queryset(self):
        user = self.request.user
        qs = self.model.objects.get_qs(user)
        if qs:
            r_name = self.request.GET.get('name')
            r_date_s = self.request.GET.get('date_s')
            r_date_e = self.request.GET.get('date_e')
            r_all = self.request.GET.get('all')
            r_type = self.request.GET.get('type')
            r_status = self.request.GET.get('status')
            r_manager = self.request.GET.get('manager')

            if r_all and int(r_all) == 1:
                self.request.session['show_all_task'] = True
            elif r_all and int(r_all) == 0:
                self.request.session['show_all_task'] = False
            try:
                show_all = self.request.session['show_all_task']
            except KeyError:
                show_all = False
            if r_manager and int(r_manager) != 0:
                qs = qs.filter(manager=int(r_manager))
            if not r_name and not r_date_s and not r_date_e and not show_all:
                qs = qs.filter(date=timezone.localtime(timezone.now()))
            else:
                if r_name:
                    qs = qs.filter(client__name__icontains=r_name)
                if r_date_s:
                    qs = qs.filter(date__gte=datetime.strptime(r_date_s, '%d.%m.%Y'))
                if r_date_e:
                    qs = qs.filter(date__lte=datetime.strptime(r_date_e, '%d.%m.%Y'))
            if r_type:
                qs = qs.filter(type=int(r_type))
            if r_status:
                qs = qs.filter(status=int(r_status))

        return qs

    def get_context_data(self, **kwargs):
        context = super(ClientTaskListView, self).get_context_data(**kwargs)

        if self.request.GET.get('error') and int(self.request.GET.get('error')) == 1:
            context.update({
                'error': True
            })

        user = self.request.user
        manager_qs = None
        if user.type == User.UserType.administrator:
            manager_qs = Manager.objects.all()
        elif user.type == User.UserType.moderator:
            manager_qs = Manager.objects.filter(moderator=user)
        elif user.type == User.UserType.manager:
            if user.manager_user.leader:
                manager_qs = Manager.objects.filter(moderator=user.manager_user.moderator.moderator_user)

        context.update({
            'manager_list': manager_qs
        })
        r_name = self.request.GET.get('name')
        r_date_s = self.request.GET.get('date_s')
        r_date_e = self.request.GET.get('date_e')
        r_type = self.request.GET.get('type')
        r_status = self.request.GET.get('status')
        r_manager = self.request.GET.get('manager')
        show_all = self.request.session.get('show_all_task')

        if r_manager and int(r_manager) != 0:
            context.update({
                'r_manager': int(r_manager)
            })
        if r_type:
            context.update({
                'r_type': int(r_type)
            })
        if r_status:
            context.update({
                'r_status': int(r_status)
            })
        if r_name:
            context.update({
                'r_name': r_name
            })
        if r_date_s:
            context.update({
                'r_date_s': r_date_s
            })
        if r_date_e:
            context.update({
                'r_date_e': r_date_e
            })
        if show_all:
            context.update({
                'show_all': True
            })

        return context


class ClientTaskCreateView(CreateView, SendUserToFormMixin):
    form_class = TaskForm
    template_name = 'client/task_add.html'

    def get_success_url(self):
        return reverse('client:task-update', args=(self.object.pk,))


class ClientTaskUpdateView(UpdateView, SendUserToFormMixin, RedirectlessFormMixin):
    model = Task
    form_class = TaskForm
    template_name = 'client/task_update.html'
