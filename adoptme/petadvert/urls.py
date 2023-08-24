from django.urls import path 
from .views import CreatePetAdView, PetAdDetailView, PetAdUpdateView, PetAdDeleteView, \
    CreateSitterAdView, SitterAdUpdateView, FilterSitterView, FilterCatView

app_name = "petad"
urlpatterns = [
    path('create/', CreatePetAdView.as_view(), name='create_petad'),
    path('detail/<int:petad_pk>', PetAdDetailView.as_view(), name='petad_detail'),
    path('edit/<int:petad_pk>', PetAdUpdateView.as_view(), name='petad_update'),
    path('delete/<int:petad_pk>', PetAdDeleteView.as_view(), name='petad_delete'),
    path('create/sitterad', CreateSitterAdView.as_view(), name='create_sitterad'),
    path('edit/sitterad/<int:sitterad_pk>', SitterAdUpdateView.as_view(), name='sitterad_update'),
    path('filter/sitter/', FilterSitterView.as_view(), name='filter_sitter'),
    path('filter/pet/<str:type>', FilterCatView.as_view(), name='filter_petad'),
]