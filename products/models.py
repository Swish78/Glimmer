from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image1 = models.ImageField(upload_to='product_images/')
    image2 = models.ImageField(upload_to='product_images/', blank=True, null=True)
    image3 = models.ImageField(upload_to='product_images/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return f'{self.name}'

    @property
    def ratings(self):
        reviews = self.review_set.all()
        if reviews:
            total_rating = sum([review.rating for review in reviews])
            return round(total_rating / len(reviews), 1)
        return 0.0

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('products:product_detail', kwargs={'pk': self.pk})


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Review by {self.reviewer} on {self.product}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Clear the product's cache when a review is added/updated
        from django.core.cache import cache
        cache.delete(f'product_detail_{self.product.pk}')
