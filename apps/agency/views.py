# coding=utf-8
from django.core.urlresolvers import reverse
from django.views.generic import CreateView, UpdateView, ListView

from core.forms import UserAddForm, UserUpdateForm
from core.models import User
from lib.cbv import RedirectlessFormMixin

__author__ = 'alexy'


class AgencyListView(ListView):
    queryset = User.objects.filter(type=6)
    template_name = 'agency/agency_list.html'
    paginate_by = 50


class AgencyCreateView(CreateView):
    form_class = UserAddForm
    template_name = 'agency/agency_add.html'

    def get_success_url(self):
        return reverse('agency:update', args=(self.object.pk,))

    def form_valid(self, form):
        form.instance.type = 6
        form.instance.is_staff = True
        form.instance.is_active = True
        if 'leader' in self.request.POST:
            form.instance.agency_leader = True
        return super(AgencyCreateView, self).form_valid(form)


class AgencyUpdateView(UpdateView, RedirectlessFormMixin):
    model = User
    form_class = UserUpdateForm
    template_name = 'agency/agency_update.html'

    def form_valid(self, form):
        if 'leader' in self.request.POST:
            form.instance.agency_leader = True
        return super(AgencyUpdateView, self).form_valid(form)
