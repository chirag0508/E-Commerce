from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings

import razorpay
from django.http import HttpResponse
from reportlab.pdfgen import canvas

from cart.models import CartItem
from .models import Order, OrderItem


@login_required
def checkout(request):

    cart_items = CartItem.objects.filter(user=request.user)

    total = 0
    for item in cart_items:
        total += item.product.price * item.quantity

    if request.method == "POST":

        full_name = request.POST.get("name")
        address = request.POST.get("address")
        city = request.POST.get("city")
        pincode = request.POST.get("pincode")

        order = Order.objects.create(
            user=request.user,
            full_name=full_name,
            address=address,
            city=city,
            pincode=pincode,
            total=total
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        cart_items.delete()

        messages.success(request, "Order created. Please complete payment.")

        return redirect("payment_page", order_id=order.id)

    return render(request, "checkout.html", {
        "cart_items": cart_items,
        "total": total
    })


# Razorpay Payment Page
@login_required
def payment_page(request, order_id):

    order = get_object_or_404(Order, id=order_id, user=request.user)

    # Prevent paying again
    if order.paid:
        messages.info(request, "This order is already paid.")
        return redirect("user_orders")

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


# Payment Verification
@login_required
def verify_payment(request):

    if request.method == "POST":

        order_id = request.POST.get("order_id")

        order = get_object_or_404(Order, id=order_id, user=request.user)

        order.paid = True
        order.save()

        messages.success(request, "Payment successful!")

        return redirect("order_success", order_id=order.id)

    return redirect("home")


# Order Success Page
@login_required
def order_success(request, order_id):

    order = get_object_or_404(Order, id=order_id, user=request.user)

    return render(request, "orders/order_success.html", {
        "order": order
    })


# My Orders Page
@login_required
def user_orders(request):

    orders = Order.objects.filter(user=request.user).order_by("-created_at")

    return render(request, "orders/orders.html", {
        "orders": orders
    })


# Order Detail Page
@login_required
def order_detail(request, order_id):

    order = get_object_or_404(Order, id=order_id, user=request.user)

    items = order.items.all()

    return render(request, "orders/order_detail.html", {
        "order": order,
        "items": items
    })


# Download Invoice
@login_required
def download_invoice(request, order_id):

    order = get_object_or_404(Order, id=order_id, user=request.user)
    items = order.items.all()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{order.id}.pdf"'

    p = canvas.Canvas(response)

    y = 800

    p.drawString(100, y, f"Invoice - Order #{order.id}")
    y -= 40

    p.drawString(100, y, f"Customer: {order.user.username}")
    y -= 30

    p.drawString(100, y, f"Total: ₹{order.total}")
    y -= 50

    p.drawString(100, y, "Products:")
    y -= 30

    for item in items:
        line = f"{item.product.name} - {item.quantity} x ₹{item.price}"
        p.drawString(100, y, line)
        y -= 25

    p.showPage()
    p.save()

    return response