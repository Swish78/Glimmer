from django.db import models
from django.conf import settings


class Blog(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    excerpt = models.TextField(max_length=500, blank=True, help_text='A short summary of the blog post')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cover_photo = models.ImageField(default='default.jpg', upload_to='static/blogs_covers/', blank=True)
    is_featured = models.BooleanField(default=False, help_text='Featured posts will be displayed on the home page')
    category = models.CharField(max_length=50, blank=True, help_text='Blog category (e.g., Fashion, Sustainability)')

    def __str__(self):
        return self.title


class BlogReview(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    comment = models.TextField()

    def __str__(self):
        return f'Review by {self.reviewer} on {self.blog}'
