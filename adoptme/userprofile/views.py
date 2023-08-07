from django.shortcuts import render, redirect
from django.views.generic import CreateView, View
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RegisterForm, LoginForm
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator


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
