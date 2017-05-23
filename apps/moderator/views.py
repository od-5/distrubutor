# coding=utf-8
import datetime
from dateutil.relativedelta import relativedelta

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.forms.models import inlineformset_factory

from lib.cbv import RedirectlessFormMixin, SendUserToFormMixin
from core.forms import UserAddForm, UserUpdateForm
from core.models import User
from apps.packages.models import Package
from apps.robokassa.forms import RobokassaForm
from apps.robokassa.signals import result_received
from apps.sale.models import CommissionOrder
from .forms import ModeratorForm, ModeratorAreaForm, ModeratorActionForm, ReviewForm
from .models import Moderator, ModeratorArea, ModeratorAction, Review, Order

__author__ = 'alexy'


class ModeratorListView(ListView):
    queryset = User.objects.filter(type=2)
    template_name = 'moderator/moderator_list.html'
    paginate_by = 50

    def get_queryset(self):
        user = self.request.user
        if user.type == 1:
            qs = User.objects.filter(type=2)
        elif user.superviser:
            qs = User.objects.select_related().filter(type=2, moderator_user__superviser=user)
        elif user.type == 6:
            qs = User.objects.select_related().filter(type=2, moderator_user__ticket_forward=True)
        else:
            qs = User.objects.none()
        if self.request.GET.get('email'):
            qs = qs.filter(email=self.request.GET.get('email'))
        if self.request.GET.get('last_name'):
            qs = qs.filter(last_name=self.request.GET.get('last_name'))
        if self.request.GET.get('first_name'):
            qs = qs.filter(first_name=self.request.GET.get('first_name'))
        if self.request.GET.get('patronymic'):
            qs = qs.filter(patronymic=self.request.GET.get('patronymic'))
        if self.request.GET.get('phone'):
            qs = qs.filter(phone=self.request.GET.get('phone'))
        return qs

    def get_context_data(self, **kwargs):
        context = super(ModeratorListView, self).get_context_data(**kwargs)
        context.update({
            'r_email': self.request.GET.get('email', ''),
            'r_last_name': self.request.GET.get('last_name', ''),
            'r_first_name': self.request.GET.get('first_name', ''),
            'r_patronymic': self.request.GET.get('patronymic', ''),
            'r_phone': self.request.GET.get('phone', '')
        })
        return context


class ModeratorCreateView(CreateView):
    form_class = UserAddForm
    template_name = 'moderator/moderator_add.html'

    def get_success_url(self):
        return reverse('moderator:update', args=(self.object.pk, ))

    def form_valid(self, form):
        form.instance.type = 2
        form.instance.is_staff = True
        form.instance.is_active = True
        form.instance.superviser = 'superviser' in self.request.POST
        return super(ModeratorCreateView, self).form_valid(form)


class ModeratorUserUpdateView(UpdateView, RedirectlessFormMixin):
    model = User
    form_class = UserUpdateForm
    template_name = 'moderator/moderator_user_update.html'

    def get_object(self):
        obj = super(ModeratorUserUpdateView, self).get_object()
        try:
            self.moderator = Moderator.objects.get(user=obj)
        except Moderator.DoesNotExist:
            self.moderator = Moderator(user=obj)
            self.moderator.deny_access = True
            self.moderator.save()
        return obj

    def form_valid(self, form):
        if self.request.POST.get('superviser'):
            form.instance.superviser = 'superviser'
        return super(ModeratorUserUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ModeratorUserUpdateView, self).get_context_data(**kwargs)
        context['object'] = self.moderator
        return context


class ModeratorDetailView(DetailView):
    model = Moderator
    template_name = 'moderator/moderator_detail.html'
    pk_url_kwarg = None
    slug_url_kwarg = 'pk'
    slug_field = 'user__id'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'comment' in request.POST:
            self.object.comment = request.POST['comment']
            self.object.save()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class ModeratorCompanyUpdateView(UpdateView, RedirectlessFormMixin, SendUserToFormMixin):
    model = Moderator
    form_class = ModeratorForm
    template_name = 'moderator/moderator_update.html'
    pk_url_kwarg = None
    slug_url_kwarg = 'pk'
    slug_field = 'user__id'

    def get_object(self):
        try:
            obj = super(ModeratorCompanyUpdateView, self).get_object()
        except Http404:
            user = User.objects.get(pk=self.kwargs['pk'])
            obj = Moderator(user=user)
            obj.save()
        return obj


# TODO: формсет в качестве формы
@login_required()
def moderator_action_update(request, pk):
    context = {}
    moderator_user = User.objects.get(pk=int(pk))
    success_msg = u''
    error_msg = u''
    try:
        moderator = Moderator.objects.get(user=moderator_user)
    except:
        moderator = Moderator(user=moderator_user)
        moderator.save()
    if moderator.moderatoraction_set.count() > 0:
        extra_count = 0
    else:
        extra_count = 1
    moderatoraction_formset = inlineformset_factory(
        Moderator, ModeratorAction, form=ModeratorActionForm,
        can_delete=True, extra=extra_count)
    if request.method == 'POST':
        formset = moderatoraction_formset(request.POST, instance=moderator)
        if formset.is_valid():
            formset.save()
            success_msg += u' Изменения успешно сохранены'
            formset = moderatoraction_formset(instance=moderator)
        else:
            error_msg = u'Проверьте правильность ввода полей!'
    else:
        formset = moderatoraction_formset(instance=moderator)
    context.update({
        'formset': formset,
        'success': success_msg,
        'error': error_msg,
        'object': moderator
    })
    return render(request, 'moderator/moderator_action_update.html', context)


@login_required()
def area_add(request):
    if request.method == 'POST':
        form = ModeratorAreaForm(request.POST)
        if form.is_valid():
            area = form.save()
            return HttpResponseRedirect(reverse('city:update', args=(area.city.id, )))

    return HttpResponseRedirect(reverse('city:list'))


class AreaUpdateView(UpdateView):
    model = ModeratorArea
    form_class = ModeratorAreaForm
    template_name = 'moderator/moderatorarea_update.html'

    def get_success_url(self):
        return reverse('city:update', args=(self.object.city.id, ))


@csrf_exempt
@login_required()
def review_add(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


class ReviewUpdateView(UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'moderator/review_update.html'
    success_url = reverse_lazy('moderator:review-list')


class ReviewListView(ListView):
    model = Review
    template_name = 'moderator/review_list.html'
    paginate_by = 25

    def get_queryset(self):
        user = self.request.user
        if user.type == 1:
            qs = Review.objects.all()
            if self.request.GET.get('moderator') and self.request.GET.get('moderator') != '0':
                qs = qs.filter(moderator=int(self.request.GET.get('moderator')))
        elif user.type == 2:
            qs = Review.objects.filter(moderator=user.moderator_user)
        elif user.type == 5:
            qs = Review.objects.filter(moderator=user.manager_user.moderator.moderator_user)
        else:
            raise Http404
        return qs

    def get_context_data(self, **kwargs):
        context = super(ReviewListView, self).get_context_data(**kwargs)
        if self.request.user.type == 1:
            moderator_qs = Moderator.objects.all()
            context.update({
                'moderator_list': moderator_qs
            })
            if self.request.GET.get('moderator'):
                context.update({
                    'r_moderator': int(self.request.GET.get('moderator'))
                })
        return context


class PaymentListView(ListView):
    template_name = 'moderator/payment_list.html'
    context_object_name = 'order_list'

    def get(self, request, *args, **kwargs):
        if request.user.type not in [1, 2]:
            return HttpResponseRedirect(reverse('dashboard:index'))

        self.moderator = Moderator.objects.select_related().get(user=int(kwargs['pk']))
        if request.GET.get('package') and self.moderator.city.count():
            try:
                package = Package.objects.get(pk=int(request.GET.get('package')))
                total_sum = package.cost * self.moderator.city.count()
                order = Order.objects.create(moderator=self.moderator, cost=total_sum, package=package)
                return HttpResponseRedirect(reverse('moderator:payment-detail', args=(order.id, )))
            except Package.DoesNotExist:
                pass

        return super(PaymentListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        return self.moderator.order_set.all()

    def get_context_data(self, **kwargs):
        context = super(PaymentListView, self).get_context_data(**kwargs)
        if self.request.user.type == 2:
            context['package_list'] = Package.objects.all()
        context['object'] = self.moderator
        return context


# TODO: переписать использование имен в контексте шаблона
class PaymentDetailView(DetailView):
    model = Order
    context_object_name = 'order'
    template_name = 'moderator/payment_detail.html'

    def get_context_data(self, **kwargs):
        context = super(PaymentDetailView, self).get_context_data(**kwargs)
        if not self.object.pay:
            form = RobokassaForm(initial={
                'OutSum': self.object.cost,
                'InvoiceID': self.object.id,
                'Description': self.object,
                '_commission': 2,
                # 'Email': order.moderator.user.email,
                # 'IncCurrLabel': '',
                # 'Culture': 'ru'
            })
            context['form'] = form
        context['object'] = self.object.moderator

        return context


class CommissionListView(ListView):
    template_name = 'moderator/commission_list.html'
    context_object_name = 'order_list'

    def get_queryset(self):
        self.moderator = Moderator.objects.get(user=self.kwargs['pk'])
        return CommissionOrder.objects.filter(moderator=self.moderator)

    def get_context_data(self, **kwargs):
        context = super(CommissionListView, self).get_context_data(**kwargs)
        context['object'] = self.moderator
        return context


# TODO: переписать использование имен в контексте шаблона
class CommissionDetailView(DetailView):
    model = CommissionOrder
    context_object_name = 'order'
    template_name = 'moderator/commission_detail.html'

    def get_context_data(self, **kwargs):
        context = super(CommissionDetailView, self).get_context_data(**kwargs)
        if not self.object.pay:
            form = RobokassaForm(initial={
                'OutSum': self.object.cost,
                'InvoiceID': self.object.id,
                'Description': self.object,
                '_commission': 1,
                # 'Email': order.moderator.user.email,
                # 'IncCurrLabel': '',
                # 'Culture': 'ru'
            })
            context['form'] = form
        context['object'] = self.object.moderator

        return context


def payment_received(sender, **kwargs):
    """
    Обработка сигнала result_received
    """
    commission = kwargs['extra']['_commission']
    if int(commission) == 1:

        order = CommissionOrder.objects.get(id=kwargs['InvId'])
        order.pay = True
        order.save()
    else:
        order = Order.objects.get(id=kwargs['InvId'])
        order.pay = True
        order.save()
        moderator = order.moderator
        moderator.deny_access = False
        today = datetime.date.today()
        if moderator.deny_date:
            if moderator.deny_date < today:
                moderator.deny_date = today + relativedelta(months=order.package.month)
            else:
                moderator.deny_date = moderator.deny_date + relativedelta(months=order.package.month)
        else:
            moderator.deny_date = today + relativedelta(months=order.package.month)
        if moderator.order_set.count() == 1:
            # todo: нужно сделать другой способ отправки, что то навроде постановки писем в очередь и
            # их последующая отправка. django-mailer и django-mailer-2 не подходят, так как не умеют отправлять
            # свёрстанные письма. Думаем над альтернативой.
            email = moderator.user.email
            # msg_plain = render_to_string('email.txt', {'name': name})
            msg_html = render_to_string('moderator/mail.html')
            second_msg_html = render_to_string('moderator/second_mail.html')
            try:
                send_mail(
                    u'Пошаговая инструкция reklamadoma.com',
                    msg_html,
                    settings.DEFAULT_FROM_EMAIL,
                    [email, ],
                    html_message=msg_html,
                )
            except:
                pass
            try:
                send_mail(
                    u'Видеоинструкции по работе в программе Контроль распространения и расклейки',
                    msg_html,
                    settings.DEFAULT_FROM_EMAIL,
                    [email, ],
                    html_message=second_msg_html,
                )
            except:
                pass
        moderator.save()


class OrderListView(ListView):
    model = Order
    template_name = 'moderator/order_list.html'
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super(OrderListView, self).get_context_data()
        pay_qs = self.object_list.filter(pay=True)
        context.update({
            'total_sum': pay_qs.aggregate(Sum('cost'))['cost__sum']
        })
        return context


class OrderDetailView(DetailView):
    model = Order
    template_name = 'moderator/order_detail.html'


result_received.connect(payment_received)
