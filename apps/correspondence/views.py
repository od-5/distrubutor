# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView, DetailView

from apps.moderator.models import Moderator
from .forms import MessageForm, UserMessageAnswerForm
from .models import Message, UserMessage

__author__ = 'alexy'


class MessageListView(ListView):
    model = Message
    template_name = 'correspondence/message_list.html'
    paginate_by = 25

    def get_queryset(self):
        user = self.request.user
        if user.type == 1:
            qs = Message.objects.filter(author__type=1)
        elif user.type == 6:
            qs = Message.objects.filter(author__type=6)
        else:
            qs = Message.objects.none()
        return qs


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
                sender_list.append(UserMessage(message=self.object, recipient=moderator.user))
            UserMessage.objects.bulk_create(sender_list)
        return HttpResponseRedirect(self.get_success_url())


class MessageDetailView(DetailView):
    model = Message
    template_name = 'correspondence/message_detail.html'


class UserMessageListView(ListView):
    model = UserMessage
    template_name = 'correspondence/usermessage_list.html'
    paginate_by = 25

    def get_queryset(self):
        user = self.request.user
        if user.type == 2:
            qs = UserMessage.objects.filter(recipient=user)
        elif user.type == 1 or user.type == 6:
            qs = UserMessage.objects.select_related().filter(usermessageanswer__recipient=user)
        else:
            qs = UserMessage.objects.none()
        return qs


class UserMessageDetailView(DetailView):
    model = UserMessage
    template_name = 'correspondence/usermessage_detail.html'

    def get_context_data(self, **kwargs):
        context = super(UserMessageDetailView, self).get_context_data()
        form = UserMessageAnswerForm()
        form.fields['usermessage'].initial = self.object
        form.fields['author'].initial = self.request.user
        if self.request.user == self.object.recipient:
            self.object.is_view = True
            self.object.save()
            form.fields['recipient'].initial = self.object.message.author
        else:
            form.fields['recipient'].initial = self.request.user
        self.object.usermessageanswer_set.filter(recipient=self.request.user, is_view=False).update(is_view=True)
        context.update({
            'form': form
        })
        return context


@login_required
def usermessage_answer_add(request):
    form = UserMessageAnswerForm(request.POST)
    if form.is_valid():
        instance = form.save()
        return HttpResponseRedirect(reverse('correspondence:usermessage-detail', args=(instance.usermessage.pk, )))
    else:
        return HttpResponseRedirect(reverse('correspondence:usermessage-list'))
