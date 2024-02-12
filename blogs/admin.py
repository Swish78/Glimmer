from django.contrib import admin

from blogs.models import Blog, BlogReview


# Register your models here.
@admin.register(Blog)
class BlogReviewAdmin(admin.ModelAdmin):
    pass


@admin.register(BlogReview)
class BlogReviewAdmin(admin.ModelAdmin):
    pass