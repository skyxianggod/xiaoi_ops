from django.urls import path

from work_order import views

urlpatterns = [
    path('order.html', views.OrderList.as_view(), name='order_list'),
    path('order-add-update.html', views.GzdbCreate.as_view(), name='gzdb_add'),
]

app_name = "gzdb"