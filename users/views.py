from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView
from .forms import CustomUserCreationForm, CustomUserUpdateForm
from products.models import Product
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import CustomUser
from django.views import View


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_products'] = Product.objects.order_by('-created_at')[:5]
        return context


# class RegisterView(FormView):
#     template_name = 'users/register.html'
#     form_class = CustomUserCreationForm
#     success_url = '/home/'  # Adjust the URL for your home page
#
#     def form_valid(self, form):
#         user = form.save()
#         login(self.request, user)
#         return super().form_valid(form)


class RegisterView(View):
    template_name = 'users/register.html'

    def get(self, request, *args, **kwargs):
        form = CustomUserCreationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Redirect to your home page
        return render(request, self.template_name, {'form': form})

# class LoginView(FormView):
#     template_name = 'users/login.html'
#     form_class = AuthenticationForm
#     success_url = ''  # Adjust the URL for your home page
#
#     def form_valid(self, form):
#         user = form.get_user()
#         login(self.request, user)
#         return super().form_valid(form)


class LoginView(View):
    template_name = 'users/login.html'

    def get(self, request, *args, **kwargs):
        form = AuthenticationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirect to your home page
        return render(request, self.template_name, {'form': form})

# class LogoutView(TemplateView):
#     template_name = 'users/logout.html'  # Create a simple template for logout if needed
#
#     def get(self, request, *args, **kwargs):
#         logout(request)
#         return redirect('home/')  # Adjust the URL for your home page


class LogoutView(View):
    template_name = 'users/logout.html'  # Create a simple template for logout if needed

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('home')  # Adjust the URL for your home page

# def user_logout(request):
#     logout(request)
#     return redirect('home')


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserUpdateForm
    template_name = 'users/user_profile_update.html'
    success_url = reverse_lazy('home')  # Redirect to your home page

    def get_object(self, queryset=None):
        return self.request.user  # Get the current user for updating


class ProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = CustomUser
    template_name = 'users/user_profile_delete.html'
    success_url = reverse_lazy('home')  # Redirect to your home page

    def get_object(self, queryset=None):
        return self.request.user  # Get the current user for deletion


class UserProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'users/user_profile.html'  # Create this template


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserUpdateForm
    template_name = 'users/user_profile_update.html'  # Create this template
    success_url = reverse_lazy('users:user_profile')  # Redirect to the user profile view

    def get_object(self, queryset=None):
        return self.request.user  # Get the current user for updating


class UserProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = CustomUser
    template_name = 'users/user_profile_delete.html'  # Create this template
    success_url = reverse_lazy('home')  # Redirect to your home page

    def get_object(self, queryset=None):
        return self.request.user  # Get the current user for deletion

