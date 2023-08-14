from typing import Any
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, View, CreateView, DeleteView, DetailView
from .models import Shelter, ShelterProfile
from django.urls import reverse_lazy
from django.http import Http404, HttpRequest
from pytils.translit import slugify

class SheltersView(ListView):
    model = ShelterProfile
    template_name = 'shelter/shelters.html'
    context_object_name = 'shelters'
    
    def get_queryset(self):
        return self.request.user.profile.profile.all()
    
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['petads'] = PetAdvert.objects.filter(owner=kwargs['object']).order_by(self.request.GET.get('ordering_type') or 'name')
    #     print(self.request)
    #     return context
    # наверное в View нет этого метода, используй ListView
    
class ShelterCreateView(CreateView):
    model = Shelter
    template_name = 'shelter/shelter_create.html'
    fields = [
        'name',
        'main_photo',
        'email',
        'about'
    ]

    def form_valid(self, form):
        shelter = Shelter.objects.create(slug=slugify(form.cleaned_data['name']),**form.cleaned_data)
        ShelterProfile.objects.create(shelter=shelter, profile=self.request.user.profile, role=ShelterProfile.RoleChoices.ADMIN)
        return redirect(reverse_lazy('shelter:shelters'))
    

class ShelterDeleteView(DeleteView):
    model = Shelter
    pk_url_kwarg = 'shelter_pk'

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any):
        return self.post(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs): 
        self.object = self.get_object() 
        self.object.delete() 
        return redirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse_lazy('shelter:shelters')
    
    def get_object(self, queryset = None):
        obj =  super().get_object(queryset)
        if obj.shelter.filter(role=ShelterProfile.RoleChoices.ADMIN).first().profile != self.request.user.profile:
            raise Http404
        return obj
    
class ShelterDetailView(DetailView):
    model = Shelter
    template_name = "shelter/shelter_detail.html"
    slug_url_kwarg = 'shelter_slug'
    context_object_name = 'shelter'
