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
            sale = user.sale_user
            task_qs = sale.distributortask_set.select_related().all()
            order_qs = sale.saleorder_set.all()
            point_qs = GPSPoint.objects.filter(task__sale=sale)
            # ловим значения из формы поиска
            r_task = self.request.GET.get('task') or None
            r_date_start = self.request.GET.get('date_start') or None
            r_date_end = self.request.GET.get('date_end') or None
            r_order = self.request.GET.get('order') or None
            show_table = self.request.GET.get('show_table') or None
            if r_task and r_task != '0':
                point_qs = point_qs.filter(task=int(r_task))
                context.update({
                    'r_task': int(r_task)
                })
            if r_order and r_order != '0':
                point_qs = point_qs.filter(task__order=int(r_order))
                context.update({
                    'r_order': int(r_order)
                })
            if r_date_start:
                point_qs = point_qs.filter(timestamp__gte=datetime.datetime.strptime(r_date_start, '%d.%m.%Y'))
                context.update({
                    'r_date_start': r_date_start
                })
            if r_date_end:
                point_qs = point_qs.filter(timestamp__lte=datetime.datetime.strptime(r_date_end, '%d.%m.%Y'))
                context.update({
                    'r_date_end': r_date_end
                })
            if show_table:
                if int(show_table) == 0:
                    show_table = None
                else:
                    show_table = True
            else:
                show_table = True
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
                'show_table': show_table,
                'order_list': order_qs,
                # 'current_task': task,
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

