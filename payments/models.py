from django.db import models
from django.conf import settings
from orders.models import Order


class Payment(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    razorpay_order_id = models.CharField(max_length=200)

    razorpay_payment_id = models.CharField(max_length=200)

    razorpay_signature = models.CharField(max_length=200)

    amount = models.DecimalField(max_digits=10, decimal_places=2)

    paid = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.id} - {self.user.username}"