from django.urls import path
from .views import payment_page,verify_payment

urlpatterns = [
    path("pay/<int:order_id>/", payment_page, name="payment_page"),
    path("verify/", verify_payment, name="verify_payment"),
]