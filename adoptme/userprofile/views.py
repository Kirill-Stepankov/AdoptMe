from typing import Any, Dict, Optional
from django.db import models
from django.forms.models import BaseModelForm
from django.shortcuts import render, redirect
from django.views.generic import CreateView, View, DetailView, UpdateView, DeleteView
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RegisterForm, LoginForm, ProfileUpdateForm
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import UserPassesTestMixin
from .models import Profile
from .utils import unauthenticated_user
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpRequest, HttpResponse
from django.db.models import Q
from petadvert.models import PetAdvert


@method_decorator(unauthenticated_user, name='dispatch')
class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "userprofile/register.html"

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('profile:home')

@method_decorator(unauthenticated_user, name='dispatch')
class LoginUserView(LoginView):
    form_class = LoginForm
    template_name = 'userprofile/login.html'
    next_page = reverse_lazy('profile:home')

class IndexView(View):
    def get(self, request):
        return render(request, 'userprofile/index.html', context={'title': 'home'})
    
class ProfileView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'userprofile/userprofile.html'
    context_object_name = 'userprofile'
    slug_url_kwarg = 'profile_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['petads'] = PetAdvert.objects.filter(owner=kwargs['object']).order_by(self.request.GET.get('ordering_type') or 'name')
        print(self.request)
        return context

    # def test_func(self):
    #     return self.request.user.username == Profile.objects.get(slug=self.request.GET.get('profile_slug'))

class EditProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    context_object_name = 'userprofile'
    form_class = ProfileUpdateForm
    slug_url_kwarg = 'profile_slug'
    template_name = "userprofile/edit_profile.html"

    def get_object(self, queryset=None):
        return self.request.user.profile
    

    
    


    

