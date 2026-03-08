import razorpay
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from orders.models import Order
from products.models import Product


def payment_page(request, order_id):

    order = get_object_or_404(Order, id=order_id)

    if order.paid:
        return redirect("my_orders")

    client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )

    amount = int(order.total * 100)

    payment = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": 1
    })

    context = {
        "order": order,
        "payment": payment,
        "amount": amount,
        "razorpay_key": settings.RAZORPAY_KEY_ID
    }

    return render(request, "payments/payment_page.html", context)


def verify_payment(request):

    if request.method == "POST":

        order_id = request.POST.get("order_id")
        razorpay_payment_id = request.POST.get("razorpay_payment_id")

        order = Order.objects.get(id=order_id)

        # mark order as paid
        order.paid = True
        order.save()

        # ⭐ Reduce stock after payment
        items = order.items.all()

        for item in items:
            product = item.product
            product.stock -= item.quantity
            product.save()

        return redirect("order_success", order_id=order.id)

    return redirect("home")