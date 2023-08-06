from django.urls import path 
from .views import RegisterView, IndexView, LoginUserView
from django.contrib.auth.views import LogoutView

app_name = "profile"
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('home/', IndexView.as_view(), name='home'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout')
]