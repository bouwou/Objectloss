from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('register_trouveur/', views.registerTrouveur, name="register_trouveur"),
    path('register_agence/', views.registerAgence, name="register_agence"),
    path('login/', views.loginPage, name="login"),

    path('', views.index, name="home"),
    path('index/', views.index, name="homein"),
    path('getobjets/', views.getobjets, name="getobjets"),
    path('getobjet/', views.getobjet, name="getobjet"),
    path('getobjet/<int:id>/', views.getobjet, name="getobjet_charger"),
]