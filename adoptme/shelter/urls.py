from django.urls import path
from .views import SheltersView, ShelterCreateView, ShelterDeleteView, \
    ShelterDetailView, ShelterApplyView, ShelterLeaveView, ShelterSettingsView, \
          ShelterCreatePetAdView, ShelterMods, ShelterDeleteModView

app_name = 'shelter'
urlpatterns = [
    path('shelters/', SheltersView.as_view(), name='shelters'),
    path('create/', ShelterCreateView.as_view(), name='create'),
    path('delete/<int:shelter_pk>/', ShelterDeleteView.as_view(), name='delete'),
    path('<slug:shelter_slug>/', ShelterDetailView.as_view(), name='detail'),
    path('apply/<slug:shelter_slug>', ShelterApplyView.as_view(), name='apply'),
    path('leave/<int:shelter_pk>', ShelterLeaveView.as_view(), name='leave'),
    path('settings/<slug:shelter_slug>/', ShelterSettingsView.as_view(), name='settings'),
    path('settings/<slug:shelter_slug>/create', ShelterCreatePetAdView.as_view(), name='create_petad'),
    path('settings/<slug:shelter_slug>/mods', ShelterMods.as_view(), name='mods'),
    path('delete/<int:shelter_pk>/<int:mod_pk>', ShelterDeleteModView.as_view(), name='delete_mod')

]