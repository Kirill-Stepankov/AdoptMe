from django.urls import path 
from .views import CreatePetAdView, PetAdDetailView, PetAdUpdateView, PetAdDeleteView

app_name = "petad"
urlpatterns = [
    path('create/', CreatePetAdView.as_view(), name='create_petad'),
    path('detail/<int:petad_pk>', PetAdDetailView.as_view(), name='petad_detail'),
    path('edit/<int:petad_pk>', PetAdUpdateView.as_view(), name='petad_update'),
    path('delete/<int:petad_pk>', PetAdDeleteView.as_view(), name='petad_delete'),
]