from django.urls import path
from . import views
from .views import agent_transfer_player, register, coach_add_player
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('password-reset/', views.password_reset_request, name='password_reset'),
    path('dashboard/', views.dashboard, name='dashboard'),
    # Add CRUD URLs as needed

    path('admin/create/', views.admin_create, name='admin_create'),
    path('admin/update/<int:pk>/', views.admin_update, name='admin_update'),
    path('admin/delete/<int:pk>/', views.admin_delete, name='admin_delete'),
    path('coach/add-player/', coach_add_player, name='coach_add_player'),
    path('agent/transfer-player/', agent_transfer_player, name='agent_transfer_player'), 
    path('password_reset/', views.password_reset_request, name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
]

