from django.urls import path
from app import views

urlpatterns = [
    path('', views.login, name="login"),
    path('login/', views.login, name="login"),
    path('home/', views.home, name="home"),
    
    
]