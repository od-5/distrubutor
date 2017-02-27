# coding=utf-8
from django.test import TestCase
from core.models import User


class LoginWithUserTestCase(TestCase):
    user_type = 1
    user_email = 'test_user@user.us'
    user_password = '123456'

    def setUp(self):
        self.user = User.objects.create_user(self.user_email, self.user_password, type=self.user_type)
        self.client.login(username=self.user_email, password=self.user_password)
