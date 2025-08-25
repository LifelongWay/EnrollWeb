from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('user/auth/login/', views.login_view, name = "login"),
    path('user/auth/register/', views.register, name = 'register'),
    path('user/auth/logout/', views.logout_view, name = 'logout'),
    path('users/panel/<str:role>/', views.roles_view, name = 'panel'),
    path('users/add/<str:role>/', views.account_add_view, name = 'add'),
    path('user/profile/<int:user_id>/', views.profile_view, name = 'profile'),
    path('user/profile/edit/<int:user_id>/', views.profile_edit_view, name = 'profile-edit'),
]
