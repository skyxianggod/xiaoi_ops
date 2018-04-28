from django.urls import path

from gzdb import views

urlpatterns = [
    path('gzdb.html', views.GzdbListAll.as_view(), name='gzdb_list'),
    path('gzdb-add-update.html', views.GzdbCreate.as_view(), name='gzdb_add'),
]

app_name = "gzdb"
