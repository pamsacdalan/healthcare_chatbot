from xml.etree.ElementInclude import include
from django.urls import path
from app import views

urlpatterns = [
    # path('', views.login, name="login"),
    path('', views.user_login, name='login'),
    # path('login/', views.login, name="login"),
    path('home/', views.home, name="home"),

    # user login/logout
    # path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),

    
]