# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.forms import formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, DetailView
from apps.administrator.decorators import administrator_required
from apps.moderator.models import Moderator
from .forms import MessageForm
from .models import Message, MessageNotify

__author__ = 'alexy'


class MessageListView(ListView):
    model = Message
    template_name = 'correspondence/message_list.html'
    paginate_by = 25

    def get_queryset(self):
        user = self.request.user
        qs = Message.objects.filter(author=user)
        return qs


# @administrator_required
# def message_add(request):
#     context = {}
#     user = request.user
#     if request.method == "POST":
#         form = MessageForm(request.POST)
#         if form.is_valid():
#             # client = form.save(commit=False)
#             # client.save()
#             # clientmanager = ClientManager(manager=client.manager, client=client)
#             # clientmanager.save()
#             # # return HttpResponseRedirect(reverse('client:update', args=(incoming.id,)))
#             # context.update({
#             #     'success': u'Клиент добавлен!'
#             # })
#         else:
#             # context.update({
#             #     'error': u'Проверьте правильность ввода полей'
#             # })
#             print 'error'
#     else:
#         form = MessageForm()
#     context.update({
#         'form': form,
#     })
#     return render(request, 'correspomdence/message_add.html', context)

class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'correspondence/message_add.html'

    def get_initial(self):
        return {
            'author': self.request.user
        }

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        if self.request.POST.getlist('sender_group[]'):
            sender_list = []
            for i in self.request.POST.getlist('sender_group[]'):
                moderator = Moderator.objects.get(pk=int(i))
                sender_list.append(MessageNotify(message=self.object, moderator=moderator))
            MessageNotify.objects.bulk_create(sender_list)
        return HttpResponseRedirect(self.get_success_url())


class MessageDetailView(DetailView):
    model = Message
    template_name = 'correspondence/message_detail.html'


class MessageNotifyListView(ListView):
    model = MessageNotify
    template_name = 'correspondence/messagenotify_list.html'
    paginate_by = 25

    def get_queryset(self):
        user = self.request.user
        qs = MessageNotify.objects.filter(moderator__user=user)
        return qs


class MessageNotifyDetailView(DetailView):
    model = MessageNotify
    template_name = 'correspondence/messagenotify_detail.html'

    def get_context_data(self, **kwargs):
        context = super(MessageNotifyDetailView, self).get_context_data()
        if self.request.user == self.object.moderator.user:
            self.object.is_view = True
            self.object.save()
        return context

