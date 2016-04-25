# coding=utf-8
import os
import datetime
from django.forms import HiddenInput
from django.utils.timezone import utc
from django.views.generic import TemplateView
from apps.distributor.models import GPSPoint, DistributorTask
from apps.moderator.forms import ReviewForm

__author__ = 'alexy'


class DashboardView(TemplateView):

    def get_template_names(self):
        user = self.request.user
        folder = 'dashboard'
        template = 'dashboard.html'
        if user.type == 1:
            template = 'dash_admin.html'
        elif user.type == 2:
            template = 'dash_moderator.html'
        elif user.type == 3:
            template = 'dash_sale.html'
        elif user.type == 5:
            if user.manager_user.leader:
                template = 'dash_moderator.html'
            else:
                template = 'dash_manager.html'
        return os.path.join(folder, template)

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data()
        user = self.request.user
        if user.type == 3:
            task_qs = DistributorTask.objects.filter(sale=user.sale_user)
            if self.request.GET.get('task'):
                task = DistributorTask.objects.get(pk=int(self.request.GET.get('task')))
            else:
                task = task_qs.first()
            point_qs = task.gpspoint_set.all()
            form = ReviewForm(
                initial={
                    'moderator': user.sale_user.moderator,
                    'name': user.get_full_name(),
                    'mail': user.email
                }
            )
            form.fields['name'].widget = HiddenInput()
            form.fields['mail'].widget = HiddenInput()
            context.update({
                'current_task': task,
                'task_list': task_qs,
                'point_list': point_qs,
                'form': form
            })
        if user.type == 5:
            if not user.manager_user.leader:
                today = datetime.datetime.utcnow().replace(tzinfo=utc).date()
                actual_task_count = user.manager_user.task_set.filter(date=today).count()
                context.update({
                    'actual_task_count': actual_task_count
                })
        return context

