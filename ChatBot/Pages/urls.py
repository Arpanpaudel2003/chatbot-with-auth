from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('',views.login, name='login'),
    path('register/', views.register, name = 'register'),
    path('logout', views.logout, name = 'logout')
]