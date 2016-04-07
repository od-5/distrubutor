# coding=utf-8
import os
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

__author__ = 'alexy'


class DashboardView(TemplateView):

    def get_template_names(self):
        user = self.request.user
        folder = 'dashboard'
        template = 'dashboard.html'
        if user.type == 1:
            template = 'dash_admin.html'
        return os.path.join(folder, template)
