#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.urls import path
from tb_log import views

app_name = 'tb_log'

urlpatterns = [
    path('tb_log-<kw>-<pk>-<user>.html', views.logcreate, name='tb_log_create'),
    path('tb_log.html', views.LogView.as_view(), name='tb_log_list'),
    # path('assets-add-update.html', views.AssetsAdd.as_view(), name='assets_add'),
    # path('assets-detail-<pk>.html', views.AssetsDetail.as_view(), name='assets_detail'),
    # path('assets-add-update-g-<pk>.html', views.AssetsUpdate.as_view(), name='assets_update_g'),
    # path('assets-add-update-o-<pk>.html', views.AssetsUpdate.as_view(), name='assets_update_o'),
    # path('assets-add-update-i-<pk>.html', views.AssetsUpdatein.as_view(), name='assets_update_i'),
    # path('getdata.html', views.getdata, name='getdate'),
]