from django.urls import path
from pfdb import views

urlpatterns = [
    path('pfdb.html',views.PlatfromList.as_view(),name='pfdb_list'),
    path('pfdb-add-update.html',views.PlatfromCreat.as_view(),name='pfdb_add'),
    path('pfdb-add-update-<int:pk>.html',views.PlatfromUpdate.as_view(),name='pfdb_update'),
    path('pfdb-del.html',views.PfdbDel.as_view(),name='pfdn_del'),
    ]

app_name="pfdb"