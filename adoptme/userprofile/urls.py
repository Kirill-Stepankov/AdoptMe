from django.urls import path 
from .views import RegisterView, IndexView, LoginUserView, ProfileView, EditProfileView, \
    pageNotFound, serverError
from django.contrib.auth.views import LogoutView
from django.views.decorators.cache import cache_page

app_name = "profile"
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('', IndexView.as_view(), name='home'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/<slug:profile_slug>', ProfileView.as_view(), name='profile'),
    path('settings', EditProfileView.as_view(), name='edit_profile'),
]