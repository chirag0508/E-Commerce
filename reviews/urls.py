from django.urls import path
from .views import add_review

urlpatterns = [

    path("add/<slug:slug>/", add_review, name="add_review"),

]