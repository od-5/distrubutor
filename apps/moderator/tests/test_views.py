# coding=utf-8
from django.core.urlresolvers import reverse

from core.tests.base import LoginWithUserTestCase
from apps.sale.tests.fixtures import CommissionOrderFactory
from .fixtures import ModeratorFactory, ReviewFactory, ModeratorAreaFactory, OrderFactory


class ModeratorTestCase(LoginWithUserTestCase):
    def test_list_smoke(self):
        response = self.client.get(reverse('moderator:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'moderator/moderator_list.html')

    def test_create_smoke(self):
        response = self.client.get(reverse('moderator:add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'moderator/moderator_add.html')

    def test_user_update_smoke(self):
        moderator = ModeratorFactory()
        response = self.client.get(reverse('moderator:update', args=(moderator.user.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'moderator/moderator_user_update.html')

    def test_company_update_smoke(self):
        moderator = ModeratorFactory()
        response = self.client.get(reverse('moderator:company', args=(moderator.user.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'moderator/moderator_update.html')

    def test_action_update_smoke(self):
        moderator = ModeratorFactory()
        response = self.client.get(reverse('moderator:action', args=(moderator.user.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'moderator/moderator_action_update.html')

    def test_detail_smoke(self):
        moderator = ModeratorFactory()
        response = self.client.get(reverse('moderator:detail', args=(moderator.user.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'moderator/moderator_detail.html')


class ReviewTestCase(LoginWithUserTestCase):
    def test_list_smoke(self):
        moderator = ModeratorFactory()
        response = self.client.get(reverse('moderator:review-list'), {'moderator': moderator.pk})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'moderator/review_list.html')

    def test_create_smoke(self):
        response = self.client.get(reverse('moderator:review-add'))
        self.assertEqual(response.status_code, 200)

    def test_update_smoke(self):
        review = ReviewFactory()
        response = self.client.get(reverse('moderator:review-update', args=(review.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'moderator/review_update.html')


class ModeratorAreaTestCase(LoginWithUserTestCase):
    def test_create_smoke(self):
        response = self.client.get(reverse('moderator:area-add'))
        self.assertRedirects(response, reverse('city:list'))

    def test_update_smoke(self):
        moderator_area = ModeratorAreaFactory()
        response = self.client.get(reverse('moderator:area-update', args=(moderator_area.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'moderator/moderatorarea_update.html')


class PaymentTestCase(LoginWithUserTestCase):
    def test_list_smoke(self):
        moderator = ModeratorFactory()
        response = self.client.get(reverse('moderator:payment-list', args=(moderator.user.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'moderator/payment_list.html')

    def test_detail_smoke(self):
        order = OrderFactory()
        response = self.client.get(reverse('moderator:payment-detail', args=(order.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'moderator/payment_detail.html')


class CommissionTestCase(LoginWithUserTestCase):
    def test_list_smoke(self):
        moderator = ModeratorFactory()
        response = self.client.get(reverse('moderator:commission-list', args=(moderator.user.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'moderator/commission_list.html')

    def test_detail_smoke(self):
        commission_order = CommissionOrderFactory()
        response = self.client.get(reverse('moderator:commission-detail', args=(commission_order.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'moderator/commission_detail.html')


class OrderTestCase(LoginWithUserTestCase):
    def test_list_smoke(self):
        response = self.client.get(reverse('moderator:order-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'moderator/order_list.html')

    def test_detail_smoke(self):
        order = OrderFactory()
        response = self.client.get(reverse('moderator:order-detail', args=(order.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'moderator/order_detail.html')
