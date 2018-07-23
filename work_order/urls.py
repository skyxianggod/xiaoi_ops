from django.urls import path

from work_order import views

urlpatterns = [
    path('order.html', views.OrderList.as_view(), name='order_list'),
    path('order-add-update.html', views.OrderCreate.as_view(), name='order_add'),
]

app_name = "order"