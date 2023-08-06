from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib.auth import login, logout
from .forms import RegisterForm

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "userprofile/register.html"

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

