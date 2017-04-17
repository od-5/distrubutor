from django.core.urlresolvers import reverse

from core.tests.base import LoginWithUserTestCase


class CalculatorTestCase(LoginWithUserTestCase):
    def test_index_smoke(self):
        response = self.client.get(reverse('calculator:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'calculator/calculator.html')
