from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from products.models import Product
from .forms import ReviewForm
from .models import Review


@login_required
def add_review(request, slug):

    product = get_object_or_404(Product, slug=slug)

    if request.method == "POST":

        form = ReviewForm(request.POST)

        if form.is_valid():

            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()

            messages.success(request, "Review added")

    return redirect("product_detail", slug=slug)