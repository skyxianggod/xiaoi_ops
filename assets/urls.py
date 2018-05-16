#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.urls import path
from assets import views

app_name = 'assets'

urlpatterns = [
    path('assets.html', views.AssetsList.as_view(), name='assets_list'),
    path('assets-add-update.html', views.AssetsAdd.as_view(), name='assets_add'),
    path('assets-add-update-g-<pk>.html', views.AssetsUpdate.as_view(), name='assets_update'),
    path('getdata.html', views.getdata, name='getdate'),
]