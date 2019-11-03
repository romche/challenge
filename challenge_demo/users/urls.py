from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register, name="register_user"),
    path('token/', views.token, name="auth_token"),
    path('token/refresh/', views.refresh_token),
    path('token/revoke/', views.revoke_token),
]
