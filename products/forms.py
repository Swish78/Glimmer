from django import forms
from .models import Product, Review


class ProductForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter product name'
        }),
        help_text='Enter a descriptive name for your product'
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Enter product description'
        }),
        help_text='Provide detailed information about your product'
    )
    price = forms.DecimalField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter price',
            'min': '0',
            'step': '0.01'
        }),
        help_text='Enter the price in dollars'
    )
    category = forms.ModelChoiceField(
        queryset=None,
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text='Select the most appropriate category'
    )
    image1 = forms.ImageField(
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'
        }),
        help_text='Upload the main product image'
    )
    image2 = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'
        }),
        help_text='Upload an additional product image (optional)'
    )
    image3 = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'
        }),
        help_text='Upload an additional product image (optional)'
    )

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'image1', 'image2', 'image3']

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        from .models import Category
        self.fields['category'].queryset = Category.objects.all()
        self.fields['category'].empty_label = "Select Category"

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise forms.ValidationError('Price must be greater than zero')
        return price


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