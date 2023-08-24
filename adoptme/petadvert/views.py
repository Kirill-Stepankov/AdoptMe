from typing import Any, Dict, Optional
from django.db import models
from django.db.models.query import QuerySet
from django.shortcuts import render
from .models import PetAdvert, PetAdvertPhoto, SitterAd
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView, ListView
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect
from .forms import PetAdvertForm, PetAdvertPhotoForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin
from django.http import Http404
from django.core.mail import send_mail
from userprofile.views import ProfileView

class CreatePetAdView(LoginRequiredMixin, CreateView):
    model = PetAdvert
    form_class = PetAdvertForm
    template_name = "petadvert/create_pet_ad.html"

    def form_valid(self, form):
        PetAdvert.objects.create(ad_type=PetAdvert.AdvertType.PET, owner=self.request.user.profile, **form.cleaned_data)
        return redirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse_lazy('profile:profile', kwargs={'profile_slug': self.request.user.profile.slug})
    
class CreateSitterAdView(LoginRequiredMixin, CreateView):
    model = PetAdvert
    template_name = 'petadvert/create_sitterad.html'
    fields = [
        'content',
        'salary',
        'city',
        'experience'
    ]

    def form_valid(self, form):
        PetAdvert.objects.create(ad_type=PetAdvert.AdvertType.SITTER, owner=self.request.user.profile, name=form.cleaned_data['city'], **form.cleaned_data)
        return redirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse_lazy('profile:profile', kwargs={'profile_slug': self.request.user.profile.slug})
    
class PetAdDetailView(FormMixin, DetailView):
    model = PetAdvert
    pk_url_kwarg = 'petad_pk'
    template_name = 'petadvert/petad_detail.html'
    context_object_name = 'petad'
    form_class = PetAdvertPhotoForm

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['photos'] = PetAdvertPhoto.objects.filter(pet_advert__pk=self.kwargs['petad_pk']).all()
        form = PetAdvertPhotoForm()
        context['form'] = form
        return context
    
    def get_object(self, queryset=None):
        ad = super().get_object(queryset)
        if ad.ad_type == PetAdvert.AdvertType.SITTER or not ad.is_published:
            raise Http404
        return super().get_object(queryset)

    def get_success_url(self):
        return reverse_lazy('petad:petad_detail', kwargs={'petad_pk': self.kwargs['petad_pk']})
    
    def post(self, request, *args, **kwargs):
        if self.request.POST.get('ad_id'):
            return ProfileView.post(self, request, *args, **kwargs)
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return super(PetAdDetailView, self).form_valid(form)

class PetAdUpdateView(LoginRequiredMixin, UpdateView):  
    model = PetAdvert
    pk_url_kwarg = 'petad_pk'
    context_object_name = 'petad'
    form_class = PetAdvertForm
    template_name = 'petadvert/create_pet_ad.html'

    def get_object(self, queryset = None):
        obj =  super().get_object(queryset)
        if obj.owner != self.request.user.profile:
            raise Http404
        return obj
    
    def get_success_url(self):
        return reverse_lazy('profile:profile', kwargs={'profile_slug': self.request.user.profile.slug})
    

class SitterAdUpdateView(LoginRequiredMixin, UpdateView):
    model = PetAdvert
    pk_url_kwarg = 'sitterad_pk'
    context_object_name = 'sitterad'
    template_name = 'petadvert/create_sitterad.html'
    fields = [
        'content',
        'city',
        'salary',
        'experience'
    ]

    def get_object(self, queryset = None):
        obj =  super().get_object(queryset)
        if obj.owner != self.request.user.profile:
            raise Http404
        return obj
    
    def get_success_url(self):
        return reverse_lazy('profile:profile', kwargs={'profile_slug': self.request.user.profile.slug})

class PetAdDeleteView(LoginRequiredMixin, DeleteView):
    model = PetAdvert
    pk_url_kwarg = 'petad_pk'

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs): 
        self.object = self.get_object() 
        self.object.delete() 
        return redirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse_lazy('profile:profile', kwargs={'profile_slug': self.request.user.profile.slug})
    
    def get_object(self, queryset = None):
        obj =  super().get_object(queryset)
        if obj.owner != self.request.user.profile:
            raise Http404
        return obj

class FilterSitterView(ListView):
    model = PetAdvert
    template_name = 'petadvert/filter_sitter.html'
    context_object_name = 'ads'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        params = self.request.GET
        minp = params.get('min-price', 2500)
        maxp = params.get('max-price', 7500)
        city = params.get('city', '')
        mine = params.get('exp-min', 2)
        maxe = params.get('exp-max', 6)
        ordering = params.get('ordering_type', '-time_update')

        return PetAdvert.objects.filter(is_published=True, ad_type=PetAdvert.AdvertType.SITTER, city__icontains=city, experience__gte=mine, experience__lte=maxe, salary__gte=minp, salary__lte=maxp).order_by(ordering)


class FilterPetAdView(ListView):
    model = PetAdvert
    template_name = 'petadvert/filter_pet.html'
    context_object_name = 'ads'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['form']

    def get_queryset(self):
        return super().get_queryset() 
