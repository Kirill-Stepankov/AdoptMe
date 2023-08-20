from django.urls import path
from .views import SheltersView, ShelterCreateView, ShelterDeleteView, \
    ShelterDetailView, ShelterApplyView, ShelterLeaveView, ShelterSettingsView, \
          ShelterCreatePetAdView, ShelterModsView, ShelterDeleteModView, ShelterApplicationsView, \
          AcceptApplyView, DenyApplyView, ShelterPostsAppliesView, AcceptPostView, DenyPostView

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
    path('settings/<slug:shelter_slug>/mods', ShelterModsView.as_view(), name='mods'),
    path('delete/<int:shelter_pk>/<int:mod_pk>', ShelterDeleteModView.as_view(), name='delete_mod'),
    path('settings/<slug:shelter_slug>/applications', ShelterApplicationsView.as_view(), name='appls_mods'),
    path('settings/accept/<int:apply_pk>', AcceptApplyView.as_view(), name='accept_apply'),
    path('settings/deny/<int:apply_pk>', DenyApplyView.as_view(), name='deny_apply'),
    path('settings/<slug:shelter_slug>/posts-applies', ShelterPostsAppliesView.as_view(), name='appls_posts'),
    path('settings/accept-ad/<int:petad_pk>', AcceptPostView.as_view(), name='accept_post'),
    path('settings/deny-ad/<int:petad_pk>', DenyPostView.as_view(), name='deny_post'),
]