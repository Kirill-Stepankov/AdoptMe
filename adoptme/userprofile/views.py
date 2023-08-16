from typing import Any, Dict, Optional
from django.db import models
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.shortcuts import render, redirect
from django.views.generic import CreateView, View, DetailView, UpdateView, DeleteView, ListView
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
    
class ProfileView(LoginRequiredMixin, ListView):
    model = PetAdvert
    template_name = 'userprofile/userprofile.html'
    paginate_by = 3
    context_object_name = 'petads'
    slug_url_kwarg = 'profile_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['userprofile'] = Profile.objects.get(slug=self.kwargs['profile_slug'])
        return context

    def get_queryset(self):
        if not self.request.GET.get('ad_type') or self.request.GET.get('ad_type') == 'All':
            return PetAdvert.objects.filter(owner__slug=self.kwargs['profile_slug']).order_by(self.request.GET.get('ordering_type') or '-time_update')
        return PetAdvert.objects.filter(owner__slug=self.kwargs['profile_slug'], ad_type=self.request.GET.get('ad_type')).order_by(self.request.GET.get('ordering_type') or '-time_update')            

    
class EditProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    context_object_name = 'userprofile'
    form_class = ProfileUpdateForm
    template_name = "userprofile/edit_profile.html"

    def get_object(self, queryset=None):
        return self.request.user.profile
    

    
    


    

