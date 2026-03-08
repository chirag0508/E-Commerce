from django.shortcuts import render,get_object_or_404
from .models import Product,Category
from reviews.models import Review


def product_list(request):

    category_slug = request.GET.get("category")
    search = request.GET.get("search")

    products = Product.objects.filter(available=True)

    if category_slug:
        products = products.filter(category__slug=category_slug)

    if search:
        products = products.filter(name__icontains=search)

    categories = Category.objects.all()

    context = {

        "products":products,
        "categories":categories

    }

    return render(request,"home.html",context)


def product_detail(request, slug):

    product = Product.objects.get(slug=slug)
    products = Product.objects.filter(available=True, stock__gt=0)

    reviews = Review.objects.filter(product=product).order_by("-created_at")

    context = {

        "product": product,
        "reviews": reviews

    }

    return render(request, "product_detail.html", context)