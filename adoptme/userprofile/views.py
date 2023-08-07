from typing import Optional
from django.shortcuts import render, redirect
from django.views.generic import CreateView, View, DetailView
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RegisterForm, LoginForm
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import UserPassesTestMixin
from .models import Profile


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "userprofile/register.html"

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('profile:home')

class LoginUserView(LoginView):
    form_class = LoginForm
    template_name = 'userprofile/login.html'
    next_page = reverse_lazy('profile:home')

class IndexView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'userprofile/index.html', context={'title': 'home'})
    
class ProfileView(DetailView):
    model = Profile
    template_name = 'userprofile/userprofile.html'
    context_object_name = 'userprofile'
    slug_url_kwarg = 'profile_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        return context

    # def test_func(self):
    #     return self.request.user.username == Profile.objects.get(slug=self.request.GET.get('profile_slug'))


    

