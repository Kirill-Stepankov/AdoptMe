from django.urls import path
from .views import SheltersView, ShelterCreateView, ShelterDeleteView, ShelterDetailView # maybe ListView

app_name = 'shelter'
urlpatterns = [
    path('shelters/', SheltersView.as_view(), name='shelters'),
    path('create/', ShelterCreateView.as_view(), name='create'),
    path('delete/<int:shelter_pk>/', ShelterDeleteView.as_view(), name='delete'),
    path('<slug:shelter_slug>/', ShelterDetailView.as_view(), name='detail'),
]