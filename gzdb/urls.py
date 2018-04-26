from django.urls import path

from gzdb import views

urlpatterns = [
    path('gzdb.html', views.GzdbListAll.as_view(), name='gzdb_list'),
]

app_name = "gzdb"
