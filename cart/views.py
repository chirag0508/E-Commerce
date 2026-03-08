from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from products.models import Product
from .models import CartItem


@login_required
def add_to_cart(request, slug):

    product = get_object_or_404(Product, slug=slug)

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, "Product added to cart successfully")

    return redirect("cart")


@login_required
def cart_view(request):

    items = CartItem.objects.filter(user=request.user)

    total = 0

    for item in items:
        total += item.product.price * item.quantity

    context = {
        "items": items,
        "total": total
    }

    return render(request, "cart.html", context)


@login_required
def increase_qty(request, item_id):

    item = get_object_or_404(CartItem, id=item_id, user=request.user)

    item.quantity += 1
    item.save()

    return redirect("cart")


@login_required
def decrease_qty(request, item_id):

    item = get_object_or_404(CartItem, id=item_id, user=request.user)

    if item.quantity > 1:
        item.quantity -= 1
        item.save()

    return redirect("cart")


@login_required
def remove_item(request, item_id):

    item = get_object_or_404(CartItem, id=item_id, user=request.user)

    item.delete()

    messages.success(request, "Item removed successfully")

    return redirect("cart")