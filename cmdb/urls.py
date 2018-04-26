from django.urls import path

from cmdb import views

urlpatterns = [
    path('cmdb.html',views.CmdbListAll.as_view(),name='cmdb_list'),
    path('cmdb-del.html',views.CmdbDel.as_view(),name='cmdb_del'),
    path('cmdb-add-update.html',views.CmdbAdd.as_view(),name='cmdb_add'),
    path('cmdb-add-update-<int:pk>.html',views.CmdbUpdate.as_view(),name='cmdb_update'),
    path('cmdb-detail-<int:pk>.html',views.CmdbDetail.as_view(),name='cmdb_detail'),
    path('cmdb-export.html',views.CmdbExport.as_view(),name='cmdb_export'),
    path('cmdb-import.html',views.CmdbImport,name='cmdb_import'),
    path('cmdb-ztree.html', views.CmdbZtree, name='cmdb_ztree'),
    ]

app_name="cmdb"