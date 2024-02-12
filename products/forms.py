from django import forms
from .models import Product, Review


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'image1', 'image2', 'image3']

        widgets = {
            'description': forms.Textarea(attrs={'cols': 80, 'rows':3})
        }

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['category'].empty_label = "Select Category"


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']

        widgets = {
            'description': forms.Textarea(attrs={'cols': 80, 'rows': 1})
        }


class ReviewUpdateForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']