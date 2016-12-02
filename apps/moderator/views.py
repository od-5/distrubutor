# coding=utf-8
from annoying.decorators import ajax_request
from annoying.functions import get_object_or_None
from django.conf import settings
from django.contrib.auth.decorators import login_required
from apps.administrator.decorators import administrator_required
from django.core.mail import send_mail
import datetime
from dateutil.relativedelta import relativedelta
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from django.forms.models import inlineformset_factory, modelformset_factory
from apps.packages.models import Package
from apps.robokassa.forms import RobokassaForm
from apps.robokassa.signals import result_received
from .forms import ModeratorForm, ModeratorAreaForm, ModeratorActionForm, ReviewForm
from .models import Moderator, ModeratorArea, ModeratorAction, Review, Order
from core.forms import UserAddForm, UserUpdateForm
from core.models import User

__author__ = 'alexy'


class ModeratorListView(ListView):
    queryset = User.objects.filter(type=2)
    template_name='moderator/moderator_list.html'
    paginate_by = 50

    def get_queryset(self):
        qs = User.objects.filter(type=2)
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


@administrator_required
def moderator_add(request):
    context = {}
    if request.method == "POST":
        form = UserAddForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.type = 2
            user.is_staff = True
            user.is_active = True
            user.save()
            return HttpResponseRedirect(reverse('moderator:update', args=(user.id,)))
            # return HttpResponseRedirect(reverse('moderator:list'))
        else:
            context.update({
                'error': u'Проверьте правильность ввода полей'
            })
    else:
        form = UserAddForm()
    context.update({
        'form': form,
    })
    return render(request, 'moderator/moderator_add.html', context)


@login_required()
def moderator_user_update(request, pk):
    context = {}
    moderator_user = User.objects.get(pk=int(pk))
    success_msg = u''
    error_msg = u''
    try:
        moderator = Moderator.objects.get(user=moderator_user)
    except:
        moderator = Moderator(user=moderator_user)
        moderator.deny_access = True
        moderator.save()
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=moderator_user)
        if form.is_valid():
            form.save()
            success_msg += u' Изменения успешно сохранены'
        else:
            error_msg = u'Проверьте правильность ввода полей!'
    else:
        form = UserUpdateForm(instance=moderator_user)
    context.update({
        'form': form,
        'success': success_msg,
        'error': error_msg,
        'object': moderator
    })
    return render(request, 'moderator/moderator_user_update.html', context)


@login_required()
def moderator_company_update(request, pk):
    context = {}
    user = request.user
    moderator_user = User.objects.get(pk=int(pk))
    success_msg = u''
    error_msg = u''
    try:
        moderator = Moderator.objects.get(user=moderator_user)
    except:
        moderator = Moderator(user=moderator_user)
        moderator.save()
    if request.method == 'POST':
        form = ModeratorForm(request.POST, request.FILES, instance=moderator, user=user)
        if form.is_valid():
            form.save()
            success_msg += u' Изменения успешно сохранены'
        else:
            error_msg = u'Проверьте правильность ввода полей!'
    else:
        form = ModeratorForm(instance=moderator, user=user)
    context.update({
        'form': form,
        'success': success_msg,
        'error': error_msg,
        'object': moderator
    })
    return render(request, 'moderator/moderator_update.html', context)


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
    moderatoraction_formset = inlineformset_factory(Moderator, ModeratorAction, form=ModeratorActionForm, can_delete=True, extra=1)
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
        else:
            return HttpResponseRedirect(reverse('city:list'))
    else:
        return HttpResponseRedirect(reverse('city:list'))


@login_required()
def area_update(request, pk):
    context = {}
    area = ModeratorArea.objects.get(pk=int(pk))
    if request.method == 'POST':
        form = ModeratorAreaForm(request.POST, instance=area)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('city:update', args=(area.city.id, )))
        else:
            context.update({
                'error': u'Проверьте правильность заполнения формы'
            })
    else:
        form = ModeratorAreaForm(instance=area)
    context.update({
        'form': form,
        'object': area
    })

    return render(request, 'moderator/moderatorarea_update.html', context)


@csrf_exempt
@login_required()
def review_add(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required()
def review_update(request, pk):
    context = {}
    review = get_object_or_404(Review, pk=int(pk))
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('moderator:review-list'))
        else:
            context.update({
                'error': u'Проверьте правильность ввода данных'
            })
    else:
        form = ReviewForm(instance=review)
    context.update({
        'form': form,
        'object': review
    })
    return render(request, 'moderator/review_update.html', context)


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
        context = super(ReviewListView, self).get_context_data()
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


@login_required()
def payment_list(request, pk):
    context = {}
    moderator = Moderator.objects.select_related().get(user=int(pk))
    if request.GET.get('package') and moderator.city.count():

        try:
            package = Package.objects.get(pk=int(request.GET.get('package')))
            total_sum = package.cost * moderator.city.count()
            order = Order.objects.create(moderator=moderator, cost=total_sum, package=package)
            return HttpResponseRedirect(reverse('moderator:payment-detail', args=(order.id, )))
        except:
            pass
    order_qs = moderator.order_set.all()

    if request.user.type == 2:
        context.update({
            'package_list': Package.objects.all(),
        })
    if request.user.type not in [1, 2]:
        return HttpResponseRedirect(reverse('dashboard:index'))
    context.update({
        'order_list': order_qs,
        'object': moderator
    })
    return render(request, 'moderator/payment_list.html', context)


@login_required()
def payment_detail(request, pk):
    context = {}
    order = get_object_or_None(Order, pk=int(pk))
    if not order.pay:
        form = RobokassaForm(initial={
            'OutSum': order.cost,
            'InvoiceID': order.id,
            'Description': order,
            # 'Email': order.moderator.user.email,
            # 'IncCurrLabel': '',
            # 'Culture': 'ru'
        })
        context.update({
            'form': form
        })
    context.update({
        'order': order,
        'object': order.moderator
    })
    return render(request, 'moderator/payment_detail.html', context)


def payment_received(sender, **kwargs):
    """
    Обработка сигнала result_received
    """
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
    # todo: сделать проверку - если оплата первая (количество оплат = 1), то отправлять письмо на почту.
    moderator.save()

result_received.connect(payment_received)
