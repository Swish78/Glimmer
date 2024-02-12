from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import BlogForm
from .models import Blog, BlogReview
from .forms import BlogReviewForm


class BlogListView(ListView):
    model = Blog
    template_name = 'blogs/blog_list.html'
    context_object_name = 'blogs'


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blogs/blog_detail.html'
    context_object_name = 'blog'


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    form_class = BlogForm
    template_name = 'blogs/blog_form.html'
    success_url = reverse_lazy('blogs:blog_list')  # Adjust the URL for your blog list

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    form_class = BlogForm
    template_name = 'blogs/blog_form.html'
    success_url = reverse_lazy('blogs:blog_list')  # Adjust the URL for your blog list

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = Blog
    template_name = 'blogs/blog_confirm_delete.html'
    success_url = reverse_lazy('blogs:blog_list')  # Adjust the URL for your blog list

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class BlogReviewCreateView(LoginRequiredMixin, CreateView):
    model = BlogReview
    form_class = BlogReviewForm
    template_name = 'blogs/blog_review_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.blog = Blog.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blogs:blog_detail', kwargs={'pk': self.kwargs['pk']})


class BlogReviewUpdateView(LoginRequiredMixin, UpdateView):
    model = BlogReview
    form_class = BlogReviewForm
    template_name = 'blogs/blog_review_form.html'

    def get_success_url(self):
        return reverse_lazy('blogs:blog_detail', kwargs={'pk': self.kwargs['blog_pk']})


class BlogReviewDeleteView(LoginRequiredMixin, DeleteView):
    model = BlogReview
    template_name = 'blogs/blog_review_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('blogs:blog_detail', kwargs={'pk': self.kwargs['blog_pk']})
