from django.urls import path

from items.views import CreateDetailView, CreateOrderView, buy_order

urlpatterns = [
    path("order/create/", CreateOrderView.as_view(), name="order-create"),
    path("order/detail/<int:pk>", CreateDetailView.as_view(), name="order-detail"),
    path("order/buy/<int:pk>", buy_order, name="order-buy"),
]
