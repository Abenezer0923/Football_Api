# Football Management API

This is a Django API built with the Django Rest Framework, designed for managing users in a football management system. It supports various user roles and allows for user authentication through traditional sign-up, social sign-up, and login methods.

## Features

- **User Roles**: Custom roles for users including Admin, Coach, Agent, and Football Player.
- **Authentication**: Supports traditional sign-up and social sign-up using Google and Facebook.
- **Login**: Users can log in using traditional methods or social logins.
- **Password Reset**: Users can reset their passwords easily through email.

## Installation

### Prerequisites

- Python 3.6 or higher
- Django 3.x
- Django Rest Framework
- Django Allauth for social authentication
- Sqlite (or any other database of your choice)

### Steps to Set Up

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/yourusername/football-management-api.git
    cd football-management-api
    ```

2. **Create a Virtual Environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set Up the Database:**
    Update your database settings in `settings.py`, then run:
    ```bash
    python manage.py migrate
    ```

5. **Create a Superuser:**
    ```bash
    python manage.py createsuperuser
    ```

6. **Run the Server:**
    ```bash
    python manage.py runserver
    ```

## Usage

Access the API documentation at `/api/docs/` (if you have included a documentation tool). Use Postman or any API client to test endpoints for user registration, login, and password reset.

## Video Demo

Check out this short video to see the API in action:

[Download Video Demo](/home/abeni/Desktop/django_role_based_app/users/templates/demo.webm)

> **Note**: To view the video, make sure to play it using a compatible video player.

## Routes

The following routes are available in the application:

```python
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('password-reset/', views.password_reset_request, name='password_reset'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin/create/', views.admin_create, name='admin_create'),
    path('admin/update/<int:pk>/', views.admin_update, name='admin_update'),
    path('admin/delete/<int:pk>/', views.admin_delete, name='admin_delete'),
    path('coach/add-player/', views.coach_add_player, name='coach_add_player'),
    path('agent/transfer-player/', views.agent_transfer_player, name='agent_transfer_player'), 
    path('password_reset/', views.password_reset_request, name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
]
