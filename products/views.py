from django.views.generic import CreateView, ListView, DetailView
from .models import Product, Category, Review
from .forms import ProductForm, ReviewForm, ReviewUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect
from django.urls import reverse


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_create.html'
    success_url = reverse_lazy('products:product_list')

    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super().form_valid(form)


class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        category_name = self.request.GET.get('category')
        rating = self.request.GET.get('rating')

        queryset = Product.objects.all()

        if category_name:
            category = Category.objects.get(name=category_name)
            queryset = queryset.filter(category=category)

        if rating:
            queryset = queryset.filter(ratings__gte=float(rating))

        queryset = queryset.order_by('-created_at')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'


class ProductSearchView(ListView):
    model = Product
    template_name = 'products/product_search.html'
    context_object_name = 'results'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Product.objects.filter(name__icontains=query)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_update.html'

    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('products:product_detail', kwargs={'pk': self.object.pk})


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'products/product_delete.html'
    success_url = reverse_lazy('products:product_list')


@login_required
@require_POST
def add_review(request, pk):
    product = get_object_or_404(Product, pk=pk)
    rating = request.POST.get('rating')
    comment = request.POST.get('comment')

    if not rating or not comment:
        messages.error(request, 'Both rating and comment are required.')
        return HttpResponseRedirect(reverse('products:product_detail', args=[pk]))

    Review.objects.create(product=product, reviewer=request.user, rating=rating, comment=comment)
    messages.success(request, 'Review added successfully.')
    return HttpResponseRedirect(reverse('products:product_detail', args=[pk]))


@login_required
def update_review(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk, reviewer=request.user)

    if request.method == 'POST':
        form = ReviewUpdateForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Review updated successfully.')
            return redirect('products:product_detail', pk=review.product.pk)
    else:
        form = ReviewUpdateForm(instance=review)

    return render(request, 'products/update_review.html', {'form': form, 'review': review})


@login_required
def delete_review(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk, reviewer=request.user)
    review.delete()
    messages.success(request, 'Review deleted successfully.')
    return HttpResponseRedirect(reverse('products:product_detail', args=[review.product.pk]))
