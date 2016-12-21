# coding=utf-8
import os, socket
from .base import BASE_DIR

YANDEX_MAPS_API_KEY = 'AO7kF1UBAAAA-akFCwIAR7_VYsSjwJ9g-dDEVHElLxuBQi8AAAAAAAAAAAAQMK4N7NYtvg4ALgMZ8-GRO_cQqQ=='
SMS_RU_API_KEY = 'D075A0B5-6EA1-CC9B-DB3F-8DBC636BFDEA'

# DATABASES = {
#     'default': {
#          'ENGINE': 'django.db.backends.mysql',
#          'NAME': 'enjoyafrru_distr',
#          'USER': 'enjoyafrru_distr',
#          'PASSWORD': 'alena2010',
#          'HOST': 'localhost',
#          'PORT': '',
#     }
# }


TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)


TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, '../templates'),
)

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, '../../static')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, '../static'),
)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, '../../media')

CKEDITOR_JQUERY_URL = '//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js'
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_CONFIGS = {
    'default': {
        'width': '100%',
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['FontSize', 'TextColor'],
            ['Bold', 'Italic', 'Underline'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['Link', 'Unlink', 'Image'],
            ['RemoveFormat', 'Source']
        ]
    },
}

POINT_PHOTO_THUMB_SIZE = [300, 300]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, '../../debug.log'),
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
