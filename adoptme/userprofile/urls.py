from django.urls import path 
from .views import RegisterView, IndexView, LoginUserView, ProfileView, \
      EditProfileView, CreatePetAdView, PetAdDetailView, PetAdUpdateView, \
      PetAdDeleteView
from django.contrib.auth.views import LogoutView

app_name = "profile"
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('', IndexView.as_view(), name='home'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/<slug:profile_slug>', ProfileView.as_view(), name='profile'),
    #path('profile/<slug:profile_slug>/<', ProfileView.as_view(), name='profile'),
    path('settings', EditProfileView.as_view(), name='edit_profile'),
    path('petad/create/', CreatePetAdView.as_view(), name='create_petad'),
    path('petad/detail/<int:petad_pk>', PetAdDetailView.as_view(), name='petad_detail'),
    path('petad/edit/<int:petad_pk>', PetAdUpdateView.as_view(), name='petad_update'),
    path('petad/delete/<int:petad_pk>', PetAdDeleteView.as_view(), name='petad_delete')
]