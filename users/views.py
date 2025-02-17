from django.contrib.auth import login, logout
from django.contrib import messages
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


from blogs.models import Blog

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get latest products
        context['latest_products'] = Product.objects.order_by('-created_at')[:6]
        # Get featured blog posts
        context['featured_blog_posts'] = Blog.objects.filter(is_featured=True).order_by('-created_at')[:3]
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


from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import EmailVerificationToken

class RegisterView(View):
    template_name = 'users/register.html'

    def get(self, request, *args, **kwargs):
        form = CustomUserCreationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            
            if settings.REQUIRE_EMAIL_VERIFICATION:
                user.is_active = False
                user.save()

                # Create verification token
                token = EmailVerificationToken.objects.create(user=user)

                # Send verification email
                verification_url = f"{settings.SITE_URL}/users/verify-email/{token.token}/"
                context = {
                    'user': user,
                    'verification_url': verification_url,
                }
                html_message = render_to_string('users/email/verification_email.html', context)
                plain_message = strip_tags(html_message)

                try:
                    from sendgrid import SendGridAPIClient
                    from sendgrid.helpers.mail import Mail

                    message = Mail(
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        to_emails=user.email,
                        subject='Verify your email address',
                        html_content=html_message
                    )

                    sg = SendGridAPIClient(settings.EMAIL_HOST_PASSWORD)
                    response = sg.send(message)
                    return render(request, 'users/registration_success.html')
                except Exception as e:
                    # For development, print the error and continue
                    print(f'Email sending failed: {e}')
                    messages.error(request, 'Failed to send verification email. Please try again.')
                    user.delete()  # Delete the user if email sending fails
                    return render(request, self.template_name, {'form': form})
            else:
                # Skip email verification
                user.is_active = True
                user.email_verified = True
                user.save()
                login(request, user)
                messages.success(request, 'Registration successful! Welcome to Glimmer!')
                return redirect('home')
        return render(request, self.template_name, {'form': form})

class EmailVerificationView(View):
    def get(self, request, token):
        try:
            verification_token = EmailVerificationToken.objects.get(token=token)
            if verification_token.is_valid():
                user = verification_token.user
                user.is_active = True
                user.email_verified = True
                user.save()
                verification_token.delete()
                login(request, user)
                return render(request, 'users/email_verification_success.html')
            else:
                return render(request, 'users/email_verification_expired.html')
        except EmailVerificationToken.DoesNotExist:
            return render(request, 'users/email_verification_invalid.html')

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

