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
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from asgiref.sync import sync_to_async
from django.db.models import Q, Count
from functools import reduce
from operator import and_


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_create.html'
    success_url = reverse_lazy('products:product_list')

    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super().form_valid(form)


@method_decorator(cache_page(60 * 15), name='dispatch')
class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        cache_key = f'product_list_{self.request.GET.urlencode()}'
        cached_queryset = cache.get(cache_key)
        if cached_queryset:
            return cached_queryset

        filters = Q()
        category = self.request.GET.get('category')
        rating = self.request.GET.get('rating')
        price_min = self.request.GET.get('price_min')
        price_max = self.request.GET.get('price_max')
        sort = self.request.GET.get('sort', '-created_at')

        if category:
            filters &= Q(category__name=category)
        if rating:
            filters &= Q(ratings__gte=float(rating))
        if price_min:
            filters &= Q(price__gte=float(price_min))
        if price_max:
            filters &= Q(price__lte=float(price_max))

        queryset = Product.objects.filter(filters).order_by(sort)
        cache.set(cache_key, queryset, 60 * 15)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'categories': Category.objects.annotate(product_count=Count('product')),
            'price_ranges': [
                {'min': 0, 'max': 50},
                {'min': 50, 'max': 100},
                {'min': 100, 'max': 500},
                {'min': 500, 'max': None}
            ],
            'sort_options': [
                {'value': '-created_at', 'label': 'Newest'},
                {'value': 'price', 'label': 'Price Low to High'},
                {'value': '-price', 'label': 'Price High to Low'},
                {'value': '-ratings', 'label': 'Highest Rated'}
            ]
        })
        return context


@method_decorator(cache_page(60 * 15), name='dispatch')
class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

    def get_object(self, queryset=None):
        pk = self.kwargs.get(self.pk_url_kwarg)
        cache_key = f'product_detail_{pk}'
        cached_product = cache.get(cache_key)
        
        if cached_product:
            return cached_product

        product = get_object_or_404(Product, pk=pk)
        cache.set(cache_key, product, 60 * 15)
        return product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context['reviews'] = product.review_set.all().select_related('reviewer').order_by('-created_at')
        return context


class ProductSearchView(ListView):
    model = Product
    template_name = 'products/product_search.html'
    context_object_name = 'results'

    def get_queryset(self):
        query = self.request.GET.get('q')
        cache_key = f'search_{query}'
        cached_results = cache.get(cache_key)
        if cached_results:
            return cached_results

        filters = []
        if query:
            # Search in product name, description, and category name
            filters.append(
                Q(name__icontains=query) | 
                Q(description__icontains=query) |
                Q(category__name__icontains=query)
            )

        category = self.request.GET.get('category')
        if category:
            filters.append(Q(category__name=category))

        price_min = self.request.GET.get('price_min')
        if price_min:
            filters.append(Q(price__gte=float(price_min)))

        price_max = self.request.GET.get('price_max')
        if price_max:
            filters.append(Q(price__lte=float(price_max)))

        rating = self.request.GET.get('rating')
        if rating:
            filters.append(Q(ratings__gte=float(rating)))

        queryset = Product.objects.all()
        if filters:
            queryset = queryset.filter(reduce(and_, filters))

        sort = self.request.GET.get('sort', '-created_at')
        queryset = queryset.order_by(sort)

        cache.set(cache_key, queryset, 60 * 5)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'query': self.request.GET.get('q', ''),
            'categories': Category.objects.annotate(product_count=Count('product')),
            'price_ranges': [
                {'min': 0, 'max': 50},
                {'min': 50, 'max': 100},
                {'min': 100, 'max': 500},
                {'min': 500, 'max': None}
            ],
            'sort_options': [
                {'value': '-created_at', 'label': 'Newest'},
                {'value': 'price', 'label': 'Price Low to High'},
                {'value': '-price', 'label': 'Price High to Low'},
                {'value': '-ratings', 'label': 'Highest Rated'}
            ]
        })
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
