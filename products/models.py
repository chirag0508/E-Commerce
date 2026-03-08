from django.db import models
from django.db.models import Avg


class Category(models.Model):

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    price = models.DecimalField(max_digits=10, decimal_places=2)

    # FIXED IMAGE FIELD
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    available = models.BooleanField(default=True)

    # STOCK
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    # Average Rating
    def average_rating(self):
        avg = self.reviews.aggregate(Avg("rating"))["rating__avg"]
        return round(avg, 1) if avg else 0

    # Total Reviews
    def total_reviews(self):
        return self.reviews.count()