from django import forms
from .models import Blog
from .models import BlogReview


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content', 'cover_photo']  # Add other fields as needed

    # def __init__(self, *args, **kwargs):
    #     super(BlogForm, self).__init__(*args, **kwargs)
    #     # Customize form widgets or add additional customization as needed


class BlogReviewForm(forms.ModelForm):
    class Meta:
        model = BlogReview
        fields = ['comment', 'rating']  # Add other fields as needed
