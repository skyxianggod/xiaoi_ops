from django.urls import path

from base_info import views

urlpatterns = [
    path('person.html', views.PersonList.as_view(), name='person_list'),
    path('person-add-update.html', views.PersonAdd.as_view(), name='person_add'),
    path('person-del.html', views.PersonDel.as_view(), name='person_del'),
    path('person-add-update-<pk>.html', views.PersonUpdate.as_view(), name='person_update'),
    path('person-ztree.html', views.PersonZtree, name='person_ztree'),
    path('department.html', views.PartList.as_view(), name='part_list'),
    path('department-add-update.html', views.PartAdd.as_view(), name='part_add'),
    path('department-del.html', views.PartDel.as_view(), name='part_del'),
    path('department-add-update-<pk>.html', views.PartUpdate.as_view(), name='part_update'),

    path('shop.html', views.ShopList.as_view(), name='shop_list'),
    path('shop-add-update.html', views.ShopAdd.as_view(), name='shop_add'),
    path('shop-del.html', views.ShopDel.as_view(), name='shop_del'),
    path('shop-add-update-<pk>.html', views.ShopUpdate.as_view(), name='shop_update'),

    path('platform.html', views.PlatformList.as_view(), name='platform_list'),
    path('platform-add-update.html', views.PlatformAdd.as_view(), name='platform_add'),
    path('platformsize-add-update.html', views.Platform_sizeAdd.as_view(), name='platformsize_add'),
    # path('platformasstes-add-update.html', views.Platform_assetsAdd.as_view(), name='platformasstes_add'),
    # path('platform-del.html', views.PlatformDel.as_view(), name='platform_del'),
    # path('platform-add-update-<pk>.html', views.PlatformUpdate.as_view(), name='platform_update'),

]
app_name = 'base_info'
