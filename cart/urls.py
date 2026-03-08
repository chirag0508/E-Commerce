from django.urls import path
from .views import (
    add_to_cart,
    cart_view,
    increase_qty,
    decrease_qty,
    remove_item
)

urlpatterns = [

    path("", cart_view, name="cart"),

    path("add/<slug:slug>/", add_to_cart, name="add_to_cart"),

    path("inc/<int:item_id>/", increase_qty, name="increase_qty"),

    path("dec/<int:item_id>/", decrease_qty, name="decrease_qty"),

    path("remove/<int:item_id>/", remove_item, name="remove_item"),

]