from django.urls import path, include
from agence import views

urlpatterns = [
    path('', views.receptionner, name='agence_index'),
    path('receptionner/', views.receptionner, name='receptionner'),
    path('receptionner/<str:username>/', views.receptionner, name='receptionner_trouveur'),
    path('valider_reception/', views.valider_reception, name="valider_reception"),
    path('valider_reception/<int:id>/', views.valider_reception, name="valider_reception_object"),
    path('restituer/', views.restituer, name="restituer"),
    path('deliver_object/', views.deliverObject, name="deliver"),
]