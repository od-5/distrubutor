# coding=utf-8
from PIL import Image
from django.core.urlresolvers import reverse_lazy

from django.db import models

from apps.geolocation.models import City
from apps.packages.models import Package
from core.files import upload_to
from core.models import User

__author__ = 'alexy'


class Moderator(models.Model):
    class Meta:
        verbose_name = u'Модератор'
        verbose_name_plural = u'Модераторы'
        app_label = 'moderator'

    def __unicode__(self):
        if self.company:
            city_list = ', '.join(city.name for city in self.city.all())
            return u'%s (г.%s)' % (self.company, city_list)
        else:
            return self.user.get_full_name()

    def get_city_id_list(self):
        return [i.id for i in self.city.all()]

    def has_unpaid_order(self):
        """
        Метод возвращает True, если у модератора есть неоплаченные счета.
        Если есть неоплаченные счета - новый счёт создать нельзя.
        """
        if self.order_set.filter(pay=False).count():
            return True
        else:
            return False

    def get_rating(self):
        qs = self.review_set.filter(rating__isnull=False)
        count = qs.count()
        if count > 0:
            rate = 0
            for review in qs:
                rate += review.rating
            return int(round(float(rate) / count))
        else:
            return None

    def save(self, *args, **kwargs):
        super(Moderator, self).save()
        try:
            if self.logotype:
                image = Image.open(self.logotype)
                (width, height) = image.size
                size = (200, 200)
                "Max width and height 200"
                if width > 200:
                    image.thumbnail(size, Image.ANTIALIAS)
                    image.save(self.logotype.path, "PNG")
        except:
            pass

    user = models.OneToOneField(
        to=User, limit_choices_to={'type': 2}, verbose_name=u'Модератор', related_name='moderator_user'
    )
    superviser = models.ForeignKey(
        to=User, limit_choices_to={'superviser': True}, verbose_name=u'Супервайзер', related_name='superviser_user',
        blank=True, null=True
    )

    city = models.ManyToManyField(to=City, verbose_name=u'Город', blank=True, null=True)
    company = models.CharField(verbose_name=u'Название организации', max_length=200,)
    leader = models.CharField(verbose_name=u'Руководитель', max_length=200, blank=True, null=True)
    leader_function = models.CharField(verbose_name=u'Должность руководителя', max_length=200, blank=True, null=True)
    work_basis = models.CharField(verbose_name=u'Основание для работы', max_length=200, blank=True, null=True)
    experience = models.CharField(max_length=256, verbose_name=u'Стаж работы', blank=True, null=True)
    description = models.TextField(verbose_name=u'Краткое описание', blank=True, null=True)
    contact = models.TextField(verbose_name=u'Контакты (адрес, email, skype и т.д.)', blank=True, null=True)
    phone = models.CharField(max_length=100, verbose_name=u'Телефон', blank=True, null=True)
    logotype = models.ImageField(verbose_name=u'Логотип', blank=True, null=True, upload_to=upload_to)
    experience_lang = models.CharField(max_length=256, verbose_name=u'Стаж работы', blank=True, null=True)
    description_lang = models.TextField(verbose_name=u'Краткое описание', blank=True, null=True)
    contact_lang = models.TextField(verbose_name=u'Контакты', blank=True, null=True)
    fb_link = models.URLField(verbose_name=u'Facebook', max_length=256, blank=True, null=True)
    ok_link = models.URLField(verbose_name=u'Одноклассники', max_length=256, blank=True, null=True)
    vk_link = models.URLField(verbose_name=u'ВКонтакте', max_length=256, blank=True, null=True)
    insta_link = models.URLField(verbose_name=u'Instagram', max_length=256, blank=True, null=True)
    deny_access = models.BooleanField(default=False, verbose_name=u'Доступ запрёщен')
    deny_date = models.DateField(blank=True, null=True, verbose_name=u'Дата блокировки')
    site_visible = models.BooleanField(default=False, verbose_name=u'Не отображать на сайте')
    ticket_forward = models.BooleanField(default=False, verbose_name=u'Перенаправлять заявки на рекламное агенство')
    stand_accept = models.BooleanField(default=False, verbose_name=u'Система вёрсток')
    comment = models.TextField(verbose_name=u'Комментарий', blank=True, null=True)


class ModeratorArea(models.Model):
    class Meta:
        verbose_name = u'Район'
        verbose_name_plural = u'Районы'
        app_label = 'moderator'

    def __unicode__(self):
        return self.name

    city = models.ForeignKey(to=City, verbose_name=u'Город')
    moderator = models.ForeignKey(to=Moderator, verbose_name=u'Модератор')
    name = models.CharField(max_length=100, verbose_name=u'Название')


class ModeratorActionModelManager(models.Manager):
    def get_qs(self, user):
        if user.type == 2:
            qs = ModeratorAction.objects.filter(moderator=user.moderator_user)
        elif user.type == 5:
            qs = ModeratorAction.objects.filter(moderator=user.manager_user.moderator.moderator_user)
        else:
            qs = ModeratorAction.objects.none()
        return qs


class ModeratorAction(models.Model):
    class Meta:
        verbose_name = u'Вид деятельности'
        verbose_name_plural = u'Виды деятельности'
        app_label = 'moderator'

    def __unicode__(self):
        return self.name

    objects = ModeratorActionModelManager()

    moderator = models.ForeignKey(to=Moderator, verbose_name=u'Модератор')
    name = models.CharField(verbose_name=u'Название', max_length=256)
    cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=u'Олата, руб/шт', default=0)


class Review(models.Model):
    class Meta:
        verbose_name = u'Отзыв'
        verbose_name_plural = u'Отзывы'
        app_label = 'moderator'

    def __unicode__(self):
        return u'Отзыв %s' % self.name

    RATING_CHOICES = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )

    moderator = models.ForeignKey(to=Moderator, verbose_name=u'Модератор')
    name = models.CharField(verbose_name=u'Ваше имя', max_length=100, blank=True, null=True)
    mail = models.EmailField(verbose_name=u'Ваше e-mail', max_length=100, blank=True, null=True)
    # sale = models.ForeignKey(to=Sale, verbose_name=u'Клиент')
    rating = models.PositiveSmallIntegerField(
        verbose_name=u'Оценка', choices=RATING_CHOICES, default=5, blank=True, null=True)
    text = models.TextField(verbose_name=u'Текст сообщения', blank=True, null=True)


class Order(models.Model):
    class Meta:
        verbose_name = u'Счёт'
        verbose_name_plural = u'Счета'
        app_label = 'moderator'

    moderator = models.ForeignKey(to=Moderator, verbose_name=u'Модератор', blank=True, null=True,
                                  on_delete=models.SET_NULL)
    package = models.ForeignKey(to=Package, verbose_name=u'Платёжный пакет', blank=True, null=True,
                                on_delete=models.SET_NULL)
    cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=u'Сумма оплаты', default=0)
    pay = models.BooleanField(default=False, verbose_name=u'Оплачено')
    timestamp = models.DateTimeField(verbose_name=u'Дата платежа', blank=True, null=True)
    manually = models.BooleanField(default=False, verbose_name=u'Добавлено вручную')

    def __unicode__(self):
        return u'Счёт на оплату %s' % self.id

    def get_absolute_url(self):
        return reverse_lazy('moderator:order-detail', args=(self.id, ))

    def get_update_url(self):
        return reverse_lazy('moderator:order-update', args=(self.id, ))
