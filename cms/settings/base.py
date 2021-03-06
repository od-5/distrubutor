# coding=utf-8
import socket
from django.utils.translation import ugettext_lazy as _

__author__ = 'alexy'

import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = 'u@5!he@8y6ynbta9c9(l=%b1qzb(c=*9*v)jf+1lkn%_by!jk*'

DEBUG = True

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['*']

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

ADMINS = (('Alexey', 'od-5@yandex.ru'),)

ROOT_URLCONF = 'cms.urls'

WSGI_APPLICATION = 'cms.wsgi.application'

AUTH_USER_MODEL = 'core.User'
LOGIN_URL = '/login/'

LANGUAGE_CODE = 'ru-ru'
LANGUAGES = (
    ('ru', u'Россия'),
    ('uk', u'Украина'),
    ('kk', u'Казахстан'),
)
LOCALE_PATHS = (
    os.path.join(BASE_DIR, '../locale'),
)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True
