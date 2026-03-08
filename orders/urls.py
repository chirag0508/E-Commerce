from django.urls import path
from . import views

urlpatterns = [

    path("checkout/", views.checkout, name="checkout"),

    path("payment/<int:order_id>/", views.payment_page, name="payment_page"),

    path("verify-payment/", views.verify_payment, name="verify_payment"),

    path("success/<int:order_id>/", views.order_success, name="order_success"),

    path("my-orders/", views.user_orders, name="user_orders"),
    path("order/<int:order_id>/", views.order_detail, name="order_detail"),
    path("invoice/<int:order_id>/", views.download_invoice, name="download_invoice"),
]