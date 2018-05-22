"""xiaoi_ops URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

from index.views import login_view,index

urlpatterns = [
    path('admin/', admin.site.urls,name='admin'),
    path('',index),
    path('index.html',index,name='index'),
    path('login.html',login_view),
    path('cmdb/', include('cmdb.urls', namespace="cmdb", ), ),
    path('pfdb/',include('pfdb.urls',namespace="pfdb")),
    path('gzdb/', include('gzdb.urls', namespace="gzdb")),
    path('base_info/', include('base_info.urls', namespace="base_info")),
    path('asstes/',include('assets.urls',namespace="asssts")),
    path('tb_log/',include('tb_log.urls',namespace="tb_log")),
]
