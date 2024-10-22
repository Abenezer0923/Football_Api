from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from allauth.account.views import SignupView
from .forms import CustomUserCreationForm, CustomAuthenticationForm

from .models import CustomUser, Item
from .forms import ItemForm
from django.shortcuts import get_object_or_404


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = CustomUser.objects.filter(email=data)
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "users/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': request.META['HTTP_HOST'],
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    send_mail(subject, email, settings.DEFAULT_FROM_EMAIL, [user.email])
                messages.success(request, 'A password reset link has been sent to your email.')
                return redirect('login')
            else:
                messages.error(request, 'No user is associated with this email address.')
    password_reset_form = PasswordResetForm()
    return render(request, 'users/password_reset.html', {'form': password_reset_form})

@login_required
def admin_create(request):
    if request.user.role != 'admin':
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('dashboard')
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item created successfully.')
            return redirect('dashboard')
    else:
        form = ItemForm()
    return render(request, 'users/admin_create.html', {'form': form})

@login_required
def coach_add_player(request):
    if request.user.role != 'coach':
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = ItemForm(request.POST)  # Adjust the form if you have a specific form for players
        if form.is_valid():
            form.save()
            messages.success(request, 'Player added successfully.')
            return redirect('dashboard')
    else:
        form = ItemForm()  # Adjust the form if you have a specific form for players
    
    return render(request, 'users/coach_add_player.html', {'form': form})


@login_required
def admin_update(request, pk):
    if request.user.role != 'admin':
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('dashboard')
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item updated successfully.')
            return redirect('dashboard')
    else:
        form = ItemForm(instance=item)
    return render(request, 'users/admin_update.html', {'form': form})

@login_required
def admin_delete(request, pk):
    if request.user.role != 'admin':
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('dashboard')
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Item deleted successfully.')
        return redirect('dashboard')
    return render(request, 'users/admin_delete.html', {'item': item})



class CustomSignupView(SignupView):
    template_name = 'users/register.html'

    def form_valid(self, form):
        # Call the parent class's form_valid method
        response = super().form_valid(form)
        messages.success(self.request, 'Registration successful. You can now log in.')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'There were errors in your form. Please correct them and try again.')
        return super().form_invalid(form)

    def get_success_url(self):
        return self.get_redirect_url() or super().get_success_url()


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')  # Assuming username is email
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {email}.")
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = CustomAuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('login')


@login_required
def dashboard(request):
    user = request.user
    role = user.role
    if role == 'admin':
        return render(request, 'users/dashboard_admin.html')
    elif role == 'coach':
        return render(request, 'users/dashboard_coach.html')
    elif role == 'agent':
        return render(request, 'users/dashboard_agent.html')
    elif role == 'player':
        return render(request, 'users/dashboard_player.html')
    else:
        messages.error(request, 'Invalid role.')
        return redirect('login')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to the login page after successful registration
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/register.html', {'form': form})


@login_required
def agent_transfer_player(request):
    if request.user.role != 'agent':
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = ItemForm(request.POST)  # Adjust this form based on your needs
        if form.is_valid():
            # Process the transfer logic here
            player_id = form.cleaned_data.get('player_id')  # Assuming the form has player_id
            new_team = form.cleaned_data.get('new_team')  # Assuming the form has new_team
            player = get_object_or_404(CustomUser, pk=player_id)
            player.current_team = new_team
            player.save()
            messages.success(request, 'Player transferred successfully.')
            return redirect('dashboard')
    else:
        form = ItemForm()  # Adjust based on your actual form

    return render(request, 'users/agent_transfer_player.html', {'form': form})

def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = CustomUser.objects.filter(email=data)
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "users/password_reset_email.txt"
                    context = {
                        "email": user.email,
                        'domain': request.META['HTTP_HOST'],  # Your domain
                        'site_name': 'Your Site',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, context)
                    send_mail(subject, email, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
                messages.success(request, 'A password reset link has been sent to your email.')
                return redirect('login')
            else:
                messages.error(request, 'No user is associated with this email address.')
    password_reset_form = PasswordResetForm()
    return render(request, 'users/password_reset.html', {'form': password_reset_form})