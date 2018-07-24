from django.urls import path

from work_order import views

urlpatterns = [
    path('order.html', views.OrderList.as_view(), name='order_list'),
    path('order-add.html', views.OrderCreate.as_view(), name='order_add'),
    path('order-update-<pk>.html', views.OrderUpdate.as_view(), name='order_updata'),
]

app_name = "order"