# coding=utf-8
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import debug_toolbar


urlpatterns = patterns(
    '',
    # url(r'^api_v1/', include('api.urls', namespace='api')),
    # url(r'^sign/', include('apps.sign.urls', namespace='sign'),),
    url(r'^dashboard/', include('apps.dashboard.urls', namespace='dashboard'),),
    url(r'^administrator/', include('apps.administrator.urls', namespace='administrator'),),
    url(r'^moderator/', include('apps.moderator.urls', namespace='moderator'),),
    url(r'^city/', include('apps.city.urls', namespace='city'),),
    url(r'^sale/', include('apps.sale.urls', namespace='sale'),),
    # url(r'^adjuster/', include('apps.adjuster.urls', namespace='adjuster'),),
    # url(r'^task/', include('apps.adjustertask.urls', namespace='adjustertask'),),
    # url(r'^surface/', include('apps.surface.urls', namespace='surface'),),
    # url(r'^ticket/', include('apps.ticket.urls', namespace='ticket'),),
    # url(r'^journal/', include('apps.journal.urls', namespace='journal'),),
    url(r'^manager/', include('apps.manager.urls', namespace='manager'),),
    # url(r'^incoming/', include('apps.incoming.urls', namespace='incoming'),),
    url(r'', include('core.urls')),
    url(r'', include('landing.urls', namespace='landing')),

    url(r'^ckeditor/', include('ckeditor.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += patterns(
        '',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
