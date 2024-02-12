from django.contrib import admin

from products.models import Category, Product, Review


# Register your models here.
@admin.register(Category)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass