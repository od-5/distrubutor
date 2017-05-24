# coding=utf-8
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, FormView, View
from django.views.generic.detail import SingleObjectMixin

from lib.cbv import RedirectlessFormMixin
from core.models import User
from .models import Section, Topic, Comment, Notification
from .forms import SectionForm, TopicForm, CommentForm

__author__ = 'alexy'


class SectionListView(ListView):
    model = Section
    template_name = 'forum/section_list.html'


class SectionCreateView(CreateView):
    form_class = SectionForm
    template_name = 'forum/section_add.html'
    success_url = reverse_lazy('forum:list')

    def get_initial(self):
        initial = super(SectionCreateView, self).get_initial()
        initial['author'] = self.request.user
        return initial


# TODO: URL не используется
class SectionUpdateView(UpdateView):
    model = Section
    form_class = SectionForm
    template_name = 'forum/section_update.html'
    success_url = reverse_lazy('forum:list')


class TopicListView(ListView):
    template_name = 'forum/topic_list.html'

    def get_queryset(self):
        user = self.request.user
        section = Section.objects.get(pk=self.kwargs['pk'])
        qs = section.topic_set.all()
        if user.type == User.UserType.moderator:
            qs = qs.filter(moderator=True)
            city_list = [city.id for city in user.moderator_user.city.all()]
            qs = qs.filter(city__in=city_list) | qs.filter(all_city=True)
        elif user.type == User.UserType.manager:
            if user.manager_user.leader:
                qs = qs.filter(leader=True)
            else:
                qs = qs.filter(manager=True)
            city_list = [city.id for city in user.manager_user.moderator.moderator_user.city.all()]
            qs = qs.filter(city__in=city_list) | qs.filter(all_city=True)
        elif user.type == User.UserType.distributor:
            qs = qs.filter(distributor=True)
            qs = qs.filter(city=user.adjuster.city.id) | qs.filter(all_city=True)
        return qs

    def get_context_data(self, **kwargs):
        context = super(TopicListView, self).get_context_data(**kwargs)
        context.update({
            'object': Section.objects.get(pk=self.kwargs['pk']),
        })
        return context


class TopicCreateView(CreateView):
    model = Topic
    form_class = TopicForm
    template_name = 'forum/topic_add.html'

    def dispatch(self, request, *args, **kwargs):
        try:
            self.section = Section.objects.get(pk=request.GET.get('section'))
        except Section.DoesNotExist:
            return HttpResponseRedirect(reverse('forum:list'))
        return super(TopicCreateView, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super(TopicCreateView, self).get_initial()
        initial.update({
            'section': self.section,
            'author': self.request.user
        })
        return initial

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
    form_class = TopicForm
    template_name = 'forum/topic_update.html'

    def get_success_url(self):
        return reverse('forum:topic-detail', args=(self.object.pk, ))

    def get_context_data(self, **kwargs):
        context = super(TopicUpdateView, self).get_context_data(**kwargs)
        context['section'] = self.object.section
        return context


class TopicDisplayView(DetailView):
    model = Topic
    template_name = 'forum/topic_detail.html'

    def get_context_data(self, **kwargs):
        context = super(TopicDisplayView, self).get_context_data(**kwargs)
        context['form'] = CommentForm(initial={'topic': self.object, 'author': self.request.user})
        return context


class TopicCommentCreateView(SingleObjectMixin, FormView, RedirectlessFormMixin):
    template_name = 'forum/topic_detail.html'
    form_class = CommentForm
    model = Topic

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(TopicCommentCreateView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        return super(TopicCommentCreateView, self).form_valid(form)


class TopicDetailView(View):

    def get(self, request, *args, **kwargs):
        view = TopicDisplayView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = TopicCommentCreateView.as_view()
        return view(request, *args, **kwargs)


class TopicNotifyListView(ListView):
    template_name = 'forum/topic_notify.html'

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)


class CommentUpdateView(UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'forum/comment_update.html'

    def get_success_url(self):
        return reverse('forum:topic-detail', args=(self.object.topic.pk, ))


class CommentDeleteView(DeleteView):
    model = Comment
    template_name = 'forum/comment_delete.html'

    def get_success_url(self):
        return self.object.topic.get_absolute_url()


class TopicDeleteView(DeleteView):
    model = Topic
    template_name = 'forum/topic_delete.html'

    def get_success_url(self):
        return self.object.section.get_topic_list_url()


class TopicCloseView(DetailView):
    model = Topic
    template_name = 'forum/topic_close.html'

    def get_success_url(self):
        return reverse('forum:topic-detail', args=(self.object.pk,))

    def close(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()

        if self.request.user == self.object.author or self.request.user.type == User.UserType.administrator:
            self.object.closed = True
            self.object.save()

        return HttpResponseRedirect(success_url)

    def post(self, request, *args, **kwargs):
        return self.close(request, *args, **kwargs)
