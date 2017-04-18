# coding=utf-8
from django.core.urlresolvers import reverse

from core.tests.base import LoginWithUserTestCase
from .fixtures import SaleFactory, SaleMaketFactory, SaleOrderFactory, QuestionaryFactory


class SaleTestCase(LoginWithUserTestCase):
    def test_list_smoke(self):
        response = self.client.get(reverse('sale:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sale/sale_list.html')

    def test_create_smoke(self):
        response = self.client.get(reverse('sale:add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sale/sale_add.html')

    def test_update_smoke(self):
        sale = SaleFactory()
        response = self.client.get(reverse('sale:update', args=(sale.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sale/sale_update.html')


class SaleMaketTestCase(LoginWithUserTestCase):
    def test_view_smoke(self):
        sale = SaleFactory()
        response = self.client.get(reverse('sale:maket', args=(sale.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sale/sale_maket.html')

    def test_update_smoke(self):
        sale_maket = SaleMaketFactory()
        response = self.client.get(reverse('sale:maket-update', args=(sale_maket.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sale/sale_maket_update.html')


class SaleOrderTestCase(LoginWithUserTestCase):
    def test_view_smoke(self):
        sale = SaleFactory()
        response = self.client.get(reverse('sale:order', args=(sale.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sale/sale_order.html')

    def test_update_smoke(self):
        sale_order = SaleOrderFactory()
        response = self.client.get(reverse('sale:order-update', args=(sale_order.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sale/sale_order_update.html')

    def test_journal_smoke(self):
        response = self.client.get(reverse('sale:journal'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sale/journal_list.html')


class SaleQuestionaryTestCase(LoginWithUserTestCase):
    def test_view_smoke(self):
        sale = SaleFactory()
        response = self.client.get(reverse('sale:questionary', args=(sale.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sale/sale_questionary.html')

    def test_update_smoke(self):
        sale_questionary = QuestionaryFactory()
        response = self.client.get(reverse('sale:questionary-update', args=(sale_questionary.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sale/sale_questionary_update.html')


class SaleOrderPaymentTestCase(LoginWithUserTestCase):
    def test_list_smoke(self):
        sale = SaleFactory()
        response = self.client.get(reverse('sale:payment-list', args=(sale.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sale/saleorderpayment_list.html')


class CommissionOrderTestCase(LoginWithUserTestCase):
    def test_list_smoke(self):
        response = self.client.get(reverse('sale:commissionorder-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sale/commissionorder_list.html')
