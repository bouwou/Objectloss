from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [

    path('', views.index, name="trouveur_index"),
    path('signaler_objet/', views.signaler, name="signaler_objet"),
    path('signaler_objet/<int:id>/', views.signaler, name="signaler_objet_update"),
    path('mes_objets/', views.objets, name="mes_objets"),
    path('solde/', views.solde, name="solde"),
    path('objet_delete/<int:id>/', views.objet_delete, name="objet_delete"),
]