from django.urls import path, include
from . import views

urlpatterns = [
    path('login/', views.login),
    path('register/', views.register),
    path('index/', views.index),
    path('signaler/', views.signaler),
    path('objets/', views.objets),
]
