from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('csrf/', views.loginPage, name="crsf"),

    path('', views.index, name="home"),
    path('index/', views.index, name="homein"),
]