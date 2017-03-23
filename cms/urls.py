# coding=utf-8
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

import debug_toolbar

urlpatterns = patterns(
    '',
    url(r'^api_v1/', include('api.urls', namespace='api')),
    url(r'^api_promo/', include('api_promo.urls', namespace='api_promo')),
    url(r'^dashboard/', include('apps.dashboard.urls', namespace='dashboard'),),
    url(r'^administrator/', include('apps.administrator.urls', namespace='administrator'),),
    url(r'^agency/', include('apps.agency.urls', namespace='agency'),),
    url(r'^moderator/', include('apps.moderator.urls', namespace='moderator'),),
    url(r'', include('apps.geolocation.urls'),),
    url(r'^forum/', include('apps.forum.urls', namespace='forum'),),
    url(r'^package/', include('apps.packages.urls', namespace='package'),),
    url(r'^sale/', include('apps.sale.urls', namespace='sale'),),
    url(r'^distributor/', include('apps.distributor.urls', namespace='distributor'),),
    url(r'^ticket/', include('apps.ticket.urls', namespace='ticket'),),
    url(r'^manager/', include('apps.manager.urls', namespace='manager'),),
    url(r'^client/', include('apps.client.urls', namespace='client'),),
    url(r'^payment/', include('apps.robokassa.urls', namespace='payment'),),
    url(r'^correspondence/', include('apps.correspondence.urls', namespace='correspondence'),),
    url(r'^calculator/', include('apps.calculator.urls', namespace='calculator'),),
    url(r'^stand/', include('apps.stand.urls', namespace='stand'),),
    # url(r'^hanger/', include('apps.hanger_mailer.urls', namespace='hanger_mailer'),),
    url(r'', include('core.urls')),

    (r'^i18n/', include('django.conf.urls.i18n')),

    url(r'^ckeditor/', include('ckeditor.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'', include('landing.urls', namespace='landing'))
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += patterns(
        '',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
