# coding=utf-8
from annoying.functions import get_object_or_None
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView
from apps.administrator.decorators import administrator_required
from .models import Section, Topic, Comment, Notification
from .forms import SectionAddForm, TopicAddForm, CommentAddForm, SectionUpdateForm, TopicUpdateForm, CommentUpdateForm
from core.models import User

__author__ = 'alexy'


class SectionListView(ListView):
    model = Section
    template_name = 'forum/section_list.html'


@administrator_required
def section_add(request):
    user = request.user
    if request.method == 'POST':
        form = SectionAddForm(request.POST, user=user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('forum:list'))
    else:
        form = SectionAddForm(user=user)
    context = {
        'form': form
    }
    return render(request, 'forum/section_add.html', context)


@administrator_required
def section_update(request, pk):
    section = Section.objects.get(pk=int(pk))
    if request.method == 'POST':
        form = SectionUpdateForm(request.POST, instance=section)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('forum:list'))
    else:
        form = SectionUpdateForm(instance=section)
    context = {
        'form': form
    }
    return render(request, 'forum/section_update.html', context)


@login_required
def topic_list(request, pk):
    user = request.user
    context = {}
    section = Section.objects.get(pk=int(pk))
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
    context.update({
        'object': section,
        'object_list': qs
    })
    return render(request, 'forum/topic_list.html', context)


@login_required
def topic_add(request):
    user = request.user
    try:
        section = Section.objects.get(pk=int(request.GET.get('section')))
    except:
        return HttpResponseRedirect(reverse('forum:list'))
    if request.method == 'POST':
        form = TopicAddForm(request.POST, user=user)
        if form.is_valid():
            topic = form.save()
            topic.notification_recipients()
            return HttpResponseRedirect(reverse('forum:topic-list', args=(section.id, )))
    else:
        form = TopicAddForm(user=user, initial={'section': section})
    context = {
        'form': form,
        'section': section
    }
    return render(request, 'forum/topic_add.html', context)


@login_required
def topic_update(request, pk):
    topic = Topic.objects.get(pk=int(pk))
    if request.method == 'POST':
        form = TopicUpdateForm(request.POST, instance=topic)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('forum:topic-detail', args=(topic.id, )))
    else:
        form = TopicUpdateForm(instance=topic)
    context = {
        'form': form,
        'object': topic,
        'section': topic.section
    }
    return render(request, 'forum/topic_update.html', context)


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


@login_required
def topic_notify(request):
    user = request.user
    qs = Notification.objects.filter(user=user)
    context = {
        'object_list': qs
    }
    return render(request, 'forum/topic_notify.html', context)


@login_required
def comment_update(request, pk):
    context = {}
    comment = Comment.objects.get(pk=int(pk))
    topic = comment.topic
    if request.method == 'POST':
        form = CommentUpdateForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('forum:topic-detail', args=(topic.id, )))
    else:
        form = CommentUpdateForm(instance=comment)
    context.update({
        'object': comment,
        'form': form
    })
    return render(request, 'forum/comment_update.html', context)


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