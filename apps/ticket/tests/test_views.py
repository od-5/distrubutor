# coding=utf-8
from django.core.urlresolvers import reverse

from core.tests.base import LoginWithUserTestCase
from .fixtures import TicketFactory, PreSaleFactory


class TicketTestCase(LoginWithUserTestCase):
    def test_list_smoke(self):
        response = self.client.get(reverse('ticket:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ticket/ticket_list.html')

    def test_agencylist_smoke(self):
        response = self.client.get(reverse('ticket:agency'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ticket/ticketagency_list.html')

    def test_salelist_smoke(self):
        response = self.client.get(reverse('ticket:sale'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ticket/ticketagency_list.html')

    def test_add_smoke(self):
        response = self.client.get(reverse('ticket:add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ticket/ticket_add.html')

    def test_detail_smoke(self):
        ticket = TicketFactory()
        response = self.client.get(reverse('ticket:detail', args=(ticket.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ticket/ticket_detail.html')


class PreSaleTestCase(LoginWithUserTestCase):
    def test_list_smoke(self):
        response = self.client.get(reverse('ticket:presale-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ticket/presale_list.html')

    def test_create_smoke(self):
        ticket = TicketFactory()
        response = self.client.get(reverse('ticket:presale-add', args=(ticket.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ticket/presale_form.html')

    def test_update_smoke(self):
        presale = PreSaleFactory()
        response = self.client.get(reverse('ticket:presale-update', args=(presale.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ticket/presale_form.html')

    def test_detail_smoke(self):
        presale = PreSaleFactory()
        response = self.client.get(reverse('ticket:presale-detail', args=(presale.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ticket/presale_detail.html')
