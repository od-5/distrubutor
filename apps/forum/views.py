# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView

from lib.cbv import SendUserToFormMixin
from .models import Section, Topic, Comment, Notification
from .forms import SectionAddForm, TopicAddForm, CommentAddForm, SectionUpdateForm, TopicUpdateForm, CommentUpdateForm

__author__ = 'alexy'


class SectionListView(ListView):
    model = Section
    template_name = 'forum/section_list.html'


class SectionCreateView(CreateView, SendUserToFormMixin):
    form_class = SectionAddForm
    template_name = 'forum/section_add.html'
    success_url = reverse_lazy('forum:list')


# TODO: не используется
class SectionUpdateView(UpdateView):
    model = Section
    form_class = SectionUpdateForm
    template_name = 'forum/section_update.html'
    success_url = reverse_lazy('forum:list')


class TopicListView(ListView):
    template_name = 'forum/topic_list.html'

    def get_queryset(self):
        user = self.request.user
        section = Section.objects.get(pk=self.kwargs['pk'])
        qs = section.topic_set.all()
        if user.type == 2:
            qs = qs.filter(moderator=True)
            city_list = [city.id for city in user.moderator_user.city.all()]
            qs = qs.filter(city__in=city_list) | qs.filter(all_city=True)
        elif user.type == 5:
            if user.manager_user.leader:
                qs = qs.filter(leader=True)
            else:
                qs = qs.filter(manager=True)
            city_list = [city.id for city in user.manager_user.moderator.moderator_user.city.all()]
            qs = qs.filter(city__in=city_list) | qs.filter(all_city=True)
        elif user.type == 4:
            qs = qs.filter(distributor=True)
            qs = qs.filter(city=user.adjuster.city.id) | qs.filter(all_city=True)
        return qs

    def get_context_data(self, **kwargs):
        context = super(TopicListView, self).get_context_data(**kwargs)
        context.update({
            'object': Section.objects.get(pk=self.kwargs['pk']),
        })
        return context


class TopicCreateView(CreateView, SendUserToFormMixin):
    model = Topic
    form_class = TopicAddForm
    template_name = 'forum/topic_add.html'

    def dispatch(self, request, *args, **kwargs):
        try:
            self.section = Section.objects.get(pk=request.GET.get('section'))
        except Section.DoesNotExist:
            return HttpResponseRedirect(reverse('forum:list'))
        return super(TopicCreateView, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        return {'section': self.section}

    def get_success_url(self):
        return reverse('forum:topic-list', args=(self.section.pk, ))

    def form_valid(self, form):
        result = super(TopicCreateView, self).form_valid(form)
        self.object.notification_recipients()
        return result

    def get_context_data(self, **kwargs):
        context = super(TopicCreateView, self).get_context_data(**kwargs)
        context['section'] = self.section
        return context


class TopicUpdateView(UpdateView):
    model = Topic
    form_class = TopicUpdateForm
    template_name = 'forum/topic_update.html'

    def get_success_url(self):
        return reverse('forum:topic-detail', args=(self.object.pk, ))

    def get_context_data(self, **kwargs):
        context = super(TopicUpdateView, self).get_context_data(**kwargs)
        context['section'] = self.object.section
        return context


# TODO: продумать красивое решение на CBV, переписать
@login_required
def topic_detail(request, pk):
    user = request.user
    context = {}
    topic = Topic.objects.get(pk=int(pk))
    if request.method == 'POST':
        form = CommentAddForm(request.POST, user=user, topic=topic)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('forum:topic-detail', args=(topic.id, )))
    else:
        form = CommentAddForm(user=user, topic=topic)
    notification = Notification.objects.filter(topic=topic, user=user)
    if notification:
        for notify in notification:
            notify.delete()
    context.update({
        'object': topic,
        'form': form
    })
    return render(request, 'forum/topic_detail.html', context)


class TopicNotifyListView(ListView):
    template_name = 'forum/topic_notify.html'

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)


class CommentUpdateView(UpdateView):
    model = Comment
    form_class = CommentUpdateForm
    template_name = 'forum/comment_update.html'

    def get_success_url(self):
        return reverse('forum:topic-detail', args=(self.object.topic.pk, ))


# TODO: переделать логику под CBV и переписать
@login_required
def comment_delete(request, pk):
    context = {}
    comment = Comment.objects.get(pk=int(pk))
    url = comment.topic.get_absolute_url()
    delete = request.GET.get('delete')
    if delete:
        if int(delete) == 1:
            comment.delete()
        return HttpResponseRedirect(url)
    context.update({
        'object': comment,
    })
    return render(request, 'forum/comment_delete.html', context)


# TODO: переделать логику под CBV и переписать
@login_required
def topic_delete(request, pk):
    context = {}
    topic = Topic.objects.get(pk=int(pk))
    url = topic.section.get_topic_list_url()
    delete = request.GET.get('delete')
    if delete:
        if int(delete) == 1:
            topic.delete()
        return HttpResponseRedirect(url)
    context.update({
        'object': topic,
    })
    return render(request, 'forum/topic_delete.html', context)


# TODO: переделать логику под CBV и переписать
@login_required
def topic_close(request, pk):
    user = request.user
    topic = Topic.objects.get(pk=int(pk))
    close = int(request.GET.get('close', '0'))
    if close:
        if user == topic.author or user.type == 1:
            topic.closed = True
            topic.save()
        return HttpResponseRedirect(reverse('forum:topic-detail', args=(pk,)))

    return render(request, 'forum/topic_close.html', {'object': topic})
