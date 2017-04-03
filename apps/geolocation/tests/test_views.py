# coding=utf-8
from django.core.urlresolvers import reverse

from core.tests.base import LoginWithUserTestCase
from .fixtures import CityFactory, RegionFactory, CountryFactory


class CityTestCase(LoginWithUserTestCase):
    def test_list_smoke(self):
        response = self.client.get(reverse('city:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('geolocation/city_list.html')

    def test_create_smoke(self):
        response = self.client.get(reverse('city:add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('geolocation/city_add.html')

    def test_update_smoke(self):
        city = CityFactory()
        response = self.client.get(reverse('city:update', args=(city.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('geolocation/city_update.html')


class RegionTestCase(LoginWithUserTestCase):
    def test_list_smoke(self):
        response = self.client.get(reverse('region:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('geolocation/region_list.html')

    def test_create_smoke(self):
        response = self.client.get(reverse('region:add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('geolocation/region_add.html')

    def test_update_smoke(self):
        region = RegionFactory()
        response = self.client.get(reverse('region:update', args=(region.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('geolocation/region_update.html')


class CountryTestCase(LoginWithUserTestCase):
    def test_list_smoke(self):
        response = self.client.get(reverse('country:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('geolocation/country_list.html')

    def test_create_smoke(self):
        response = self.client.get(reverse('country:add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('geolocation/country_add.html')

    def test_update_smoke(self):
        country = CountryFactory()
        response = self.client.get(reverse('country:update', args=(country.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('geolocation/country_update.html')
