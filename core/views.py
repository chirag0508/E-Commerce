from django.shortcuts import render
from products.models import Product, Category
from django.db.models import Q


def home(request):

    products = Product.objects.all()
    categories = Category.objects.all()

    search = request.GET.get("search")
    category = request.GET.get("category")

    if search:
        products = products.filter(
            Q(name__icontains=search) |
            Q(category__name__icontains=search)
        )

    if category:
        products = products.filter(category__slug=category)

    return render(request, "home.html", {
        "products": products,
        "categories": categories
    })