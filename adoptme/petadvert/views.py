from typing import Any, Dict, Optional
from django.db import models
from django.db.models.query import QuerySet
from django.shortcuts import render
from .models import PetAdvert, PetAdvertPhoto, SitterAd
from userprofile.models import SexChoices
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView, ListView
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect
from .forms import PetAdvertForm, PetAdvertPhotoForm, FilterAdForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin
from django.http import Http404
from django.core.mail import send_mail
from userprofile.views import ProfileView
from django.db.models import Q

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
        context['cities'] = PetAdvert.objects.values_list('city').filter(ad_type=PetAdvert.AdvertType.SITTER).order_by().distinct()
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


class FilterCatView(ListView):
    model = PetAdvert
    template_name = 'petadvert/filter_petad.html'
    context_object_name = 'ads'
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = FilterAdForm()
        context['form'] = form
        context[self.kwargs['type']] = True
        context['type'] = self.kwargs['type']
        context['cities'] = PetAdvert.objects.values_list('city').filter(ad_type=PetAdvert.AdvertType.PET, is_published=True, type=self.kwargs['type']).order_by().distinct()
        context['colors'] = PetAdvert.objects.values_list('color').filter(ad_type=PetAdvert.AdvertType.PET, is_published=True, type=self.kwargs['type']).order_by().distinct()
        context['breeds'] = PetAdvert.objects.values_list('breed').filter(ad_type=PetAdvert.AdvertType.PET, is_published=True, type=self.kwargs['type']).order_by().distinct()
        context['shelters'] = PetAdvert.objects.values_list('shelter').filter(ad_type=PetAdvert.AdvertType.PET, is_published=True, type=self.kwargs['type']).order_by().distinct() 

        return context

    def get_queryset(self):
        if self.kwargs['type'] not in ['CAT', 'DOG', 'HRS', 'BRD', 'EXC']:
            raise Http404
        params = self.request.GET
        gender = params.get('gender', SexChoices.MALE)
        size = params.get('size', PetAdvert.SizeChoices.MEDIUM)
        house_trained = params.get('house_trained', False)
        mina = params.get('age-min', 0)
        maxa = params.get('age-max', 60)
        ordering = params.get('ordering_type', '-time_update')
        city = params.get('city', '')
        color = params.get('color', '')
        breed =params.get('breed', '')
        house_trained = True if house_trained == 'on' else False
        shelter = params.get('shelter')

        base_q = Q(is_published=True, ad_type=PetAdvert.AdvertType.PET, type=self.kwargs['type'], gender=gender, size=size, house_trained=house_trained, age__gte=mina, age__lte=maxa, city__icontains=city, color__icontains=color, breed__icontains=breed)
        if shelter:
            return PetAdvert.objects.filter(Q(base_q, shelter__name__icontains=shelter)).order_by(ordering)
        return PetAdvert.objects.filter(base_q).order_by(ordering)
