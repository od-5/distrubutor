# coding=utf-8
from django.test import TestCase
from core.models import User


class LoginWithAdminTestCase(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user('admin@admin.ad', '123456')
        self.client.login(username='admin@admin.ad', password='123456')
