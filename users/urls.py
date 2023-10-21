from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.user_register, name='user_register'),
    path('login/', views.user_login, name='user_login'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('logout/', views.logout, name='logout_request'),
]
