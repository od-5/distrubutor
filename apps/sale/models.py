# coding=utf-8
import datetime
from django.db import models
from apps.city.models import City
from apps.moderator.models import Moderator, ModeratorAction
from core.files import upload_to
from core.models import User
from apps.manager.models import Manager

__author__ = 'alexy'


class Sale(models.Model):
    class Meta:
        verbose_name = u'Клиент'
        verbose_name_plural = u'Клиенты'
        app_label = 'sale'

    def __unicode__(self):
        return self.legal_name

    user = models.OneToOneField(to=User, limit_choices_to={'type': 3}, verbose_name=u'Пользователь', related_name='sale_user')
    moderator = models.ForeignKey(to=Moderator, verbose_name=u'Модератор', related_name='sale_moderator')
    city = models.ForeignKey(to=City, verbose_name=u'Город', related_name='sale_city')
    manager = models.ForeignKey(to=Manager, verbose_name=u'Менеджер', blank=True, null=True, related_name='sale_manager')
    sender_email = models.EmailField(verbose_name=u'Email для получения уведомлений', blank=True, null=True, max_length=100)
    phone_sms = models.CharField(verbose_name=u'Телефон для смс уведомлений', blank=True, null=True, max_length=20)
    password = models.CharField(max_length=256, blank=True, null=True, verbose_name=u'пароль')
    legal_name = models.CharField(max_length=256, blank=True, null=True, verbose_name=u'Юридическое название')
    actual_name = models.CharField(max_length=256, blank=True, null=True, verbose_name=u'Фактичексое название')
    inn = models.CharField(max_length=50, blank=True, null=True, verbose_name=u'ИНН')
    kpp = models.CharField(max_length=50, blank=True, null=True, verbose_name=u'КПП')
    ogrn = models.CharField(max_length=50, blank=True, null=True, verbose_name=u'ОГРН')
    bank = models.CharField(max_length=50, blank=True, null=True, verbose_name=u'Банк')
    bik = models.CharField(max_length=50, blank=True, null=True, verbose_name=u'БИК')
    account = models.CharField(max_length=50, blank=True, null=True, verbose_name=u'Расчётный счёт')
    account_cor = models.CharField(max_length=50, blank=True, null=True, verbose_name=u'Кор. счёт')
    signer_post_dec = models.CharField(max_length=50, blank=True, null=True, verbose_name=u'должность подписанта')
    signer_name_dec = models.CharField(max_length=50, blank=True, null=True, verbose_name=u'имя подписанта')
    signer_doc_dec = models.CharField(max_length=50, blank=True, null=True, verbose_name=u'действует на основании')
    legal_address = models.TextField(verbose_name=u'Физический адрес', blank=True, null=True)
    leader = models.CharField(max_length=100, blank=True, null=True, verbose_name=u'Руководитель')
    leader_function = models.CharField(max_length=100, blank=True, null=True, verbose_name=u'Должность руководителя')
    work_basis = models.CharField(max_length=256, blank=True, null=True, verbose_name=u'Основание для работы')


class SaleOrder(models.Model):
    class Meta:
        verbose_name = u'Заказ'
        verbose_name_plural = u'Заказы'
        app_label = 'sale'
        ordering = ['-date_start', ]

    def __unicode__(self):
        if self.date_end:
            return u'Заказ %s - %s ' % (self.date_start, self.date_end)
        else:
            return u'Заказ  %s - <дата окончания не указана> ' % self.date_start

    def material_residue(self):
        count = self.count
        for task in self.distributortask_set.all():
            count -= task.actual_material_count()
        return count

    def current_payment(self):
        """
        Показывает текущую сумму поступлений по покупке
        """
        count = 0
        for payment in self.saleorderpayment_set.all():
            count += payment.sum
        return round(count, 2)

    def total_sum(self):
        total = ((float(self.cost)*(1+float(self.add_cost)*0.01))*(1-float(self.discount)*0.01)) * self.count
        return round(total, 2)

    sale = models.ForeignKey(to=Sale, verbose_name=u'Продажа')
    date_start = models.DateField(verbose_name=u'Дата начала')
    date_end = models.DateField(verbose_name=u'Дата окончания', blank=True, null=True)
    type = models.ForeignKey(to=ModeratorAction, verbose_name=u'Тип заказа')
    count = models.PositiveIntegerField(verbose_name=u'Количество материала, шт')
    cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=u'Стоимость за 1шт., руб')
    add_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=u'Наценка, %', default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=u'Скидка, %', default=0)
    closed = models.BooleanField(verbose_name=u'Заказ закрыт', default=False)
    has_payment = models.BooleanField(default=False, verbose_name=u'Есть поступления')
    full_payment = models.BooleanField(default=False, verbose_name=u'Оплачено')


class SaleOrderPayment(models.Model):
    class Meta:
        verbose_name = u'Поступление'
        verbose_name_plural = u'Поступления'
        app_label = 'sale'
        ordering = ['-created']

    def __unicode__(self):
        return u'Поступление на сумму %s руб. Дата: %s' % (self.sum, self.created)

    def save(self, *args, **kwargs):
        super(SaleOrderPayment, self).save()
        saleorder = self.saleorder
        saleorder.has_payment = True
        if saleorder.current_payment() >= saleorder.total_sum():
            saleorder.full_payment = True
        else:
            saleorder.full_payment = False
        saleorder.save()

    sale = models.ForeignKey(to=Sale, verbose_name=u'Клиент')
    saleorder = models.ForeignKey(to=SaleOrder, verbose_name=u'Покупка')
    sum = models.DecimalField(max_digits=11, decimal_places=2, verbose_name=u'Сумма')
    created = models.DateField(auto_now_add=True, verbose_name=u'Дата создания')


class SaleMaket(models.Model):
    class Meta:
        verbose_name = u'Макет'
        verbose_name_plural = u'Макеты'
        app_label = 'sale'
        ordering = ['-date']

    def __unicode__(self):
        return self.name

    sale = models.ForeignKey(to=Sale, verbose_name=u'Продажа')
    name = models.CharField(max_length=256, verbose_name=u'Название')
    file = models.FileField(verbose_name=u'Файл макета', upload_to=upload_to)
    date = models.DateField(verbose_name=u'Дата размещения макета')


# class Review(models.Model):
#     class Meta:
#         verbose_name = u'Отзыв'
#         verbose_name_plural = u'Отзывы'
#         app_label = 'sale'
#
#     def __unicode__(self):
#         return u'Отзыв %s' % self.name
#
#     RATING_CHOICES = (
#         (1, 1),
#         (2, 2),
#         (3, 3),
#         (4, 4),
#         (5, 5),
#     )
#
#     moderator = models.ForeignKey(to=Moderator, verbose_name=u'Модератор')
#     name = models.CharField(verbose_name=u'Ваше имя', max_length=100, blank=True, null=True)
#     mail = models.EmailField(verbose_name=u'Ваше e-mail', max_length=100, blank=True, null=True)
#     # sale = models.ForeignKey(to=Sale, verbose_name=u'Клиент')
#     rating = models.PositiveSmallIntegerField(verbose_name=u'Оценка', choices=RATING_CHOICES, default=5, blank=True, null=True)
#     text = models.TextField(verbose_name=u'Текст сообщения', blank=True, null=True)