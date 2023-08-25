from typing import Any, Dict, Optional
from django.db import models
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.shortcuts import render, redirect, get_object_or_404
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
from django.views.generic.edit import FormMixin
from django.core.mail import send_mail
from django.conf import settings


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
        context ={}
        context['3pets'] = PetAdvert.objects.filter(is_published=True, ad_type=PetAdvert.AdvertType.PET)[:3]
        context['more_than_3'] = PetAdvert.objects.filter(is_published=True).count()>3
        return render(request, 'userprofile/index.html', context=context)
    
class ProfileView(ListView):
    model = PetAdvert
    template_name = 'userprofile/userprofile.html'
    paginate_by = 3
    context_object_name = 'petads'
    slug_url_kwarg = 'profile_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['userprofile'] = get_object_or_404(Profile, slug=self.kwargs['profile_slug'])
        return context

    def get_queryset(self):
        if not self.request.GET.get('ad_type') or self.request.GET.get('ad_type') == 'All':
            return PetAdvert.objects.filter(owner__slug=self.kwargs['profile_slug']).order_by(self.request.GET.get('ordering_type') or '-time_update')
        return PetAdvert.objects.filter(owner__slug=self.kwargs['profile_slug'], ad_type=self.request.GET.get('ad_type')).order_by(self.request.GET.get('ordering_type') or '-time_update')


    # очень кринж
    def post(self, request, *args, **kwargs):
        ad = get_object_or_404(PetAdvert, pk=self.request.POST['ad_id'])
        if ad.ad_type == ad.AdvertType.PET:
            detail_link = 'http://localhost:8000'+reverse_lazy('petad:petad_detail', kwargs={'petad_pk': self.request.POST['ad_id']})+'\n'
        else:
            detail_link = 'http://localhost:8000'+reverse_lazy('profile:profile', kwargs={'profile_slug': ad.owner.slug})+'\n'
        owner = ad.owner.user.email if not ad.shelter else ad.shelter.email
        send_mail(
            ad,
            'From: '+self.request.POST['reciever']+'\n'+detail_link+self.request.POST['content'],
            settings.EMAIL_HOST_USER,
            [owner]
        )

        if ad.ad_type == ad.AdvertType.PET:
            return redirect(reverse_lazy('petad:petad_detail', kwargs={'petad_pk': self.request.POST['ad_id']}))
        get_params = ''
        for k in self.request.GET:
            get_params += str(k)+'='+str(self.request.GET[k])+'&'
        if get_params:
            return redirect(str(reverse_lazy('profile:profile', kwargs={'profile_slug': self.kwargs['profile_slug']}))+'?'+get_params[:-1])
        return redirect(reverse_lazy('profile:profile', kwargs={'profile_slug': self.kwargs['profile_slug']}))

class EditProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    context_object_name = 'userprofile'
    form_class = ProfileUpdateForm
    template_name = "userprofile/edit_profile.html"

    def get_object(self, queryset=None):
        return self.request.user.profile
    
def pageNotFound(request, exception):
    return render(request, 'userprofile/error.html', context={'status': 404})

def serverError(request):
    return render(request, 'userprofile/error.html', context={'status': 500})


    

