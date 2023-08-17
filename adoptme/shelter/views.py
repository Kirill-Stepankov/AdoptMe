from typing import Any, Dict
from django.forms.models import BaseModelForm
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, DeleteView, DetailView
from .models import Shelter, ShelterProfile, ShelterPhoto, ShelterApply
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import Http404, HttpRequest, HttpResponse
from pytils.translit import slugify
from .forms import CreateShelterForm, ShelterPhotoForm, ShelterApplyForm
from django.views.generic.edit import FormMixin


class SheltersView(LoginRequiredMixin, ListView):
    model = ShelterProfile
    template_name = 'shelter/shelters.html'
    context_object_name = 'shelters'
    
    def get_queryset(self):
        return self.request.user.profile.profile.all()

    
class ShelterCreateView(LoginRequiredMixin, CreateView):
    model = Shelter
    form_class = CreateShelterForm
    template_name = 'shelter/shelter_create.html'

    def form_valid(self, form):
        shelter = Shelter.objects.create(slug=slugify(form.cleaned_data['name']),**form.cleaned_data)
        ShelterProfile.objects.create(shelter=shelter, profile=self.request.user.profile, role=ShelterProfile.RoleChoices.ADMIN)
        return redirect(reverse_lazy('shelter:shelters'))
    

class ShelterDeleteView(LoginRequiredMixin, DeleteView):
    model = Shelter
    pk_url_kwarg = 'shelter_pk'

    def get(self, request: HttpRequest, *args, **kwargs):
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
    
class ShelterDetailView(FormMixin, DetailView):
    model = Shelter
    template_name = "shelter/shelter_detail.html"
    slug_url_kwarg = 'shelter_slug'
    context_object_name = 'shelter'
    form_class = ShelterPhotoForm

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['photos'] = ShelterPhoto.objects.filter(shelter__slug=self.kwargs['shelter_slug']).all()
        
        print(self.get_object().shelter.filter(profile=self.request.user.profile))
        if not self.request.user.is_anonymous:
            context['is_admin'] = bool(self.get_object().shelter.filter(profile=self.request.user.profile))
        else:
            context['is_admin'] = False
        form = ShelterPhotoForm()
        context['form'] = form
        return context

    def get_success_url(self):
        return reverse_lazy('shelter:detail', kwargs={'shelter_slug': self.kwargs['shelter_slug']})
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        shelter = self.get_object()
        if not shelter.main_photo:
            shelter.main_photo = form.cleaned_data['image']
            shelter.save()
        else:
            form.save()
        return super(ShelterDetailView, self).form_valid(form)

class ShelterApplyView(LoginRequiredMixin, CreateView):
    model = ShelterApply
    slug_url_kwarg = 'shelter_slug'
    form_class = ShelterApplyForm
    template_name = 'shelter/shelter_apply.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['shelter_id'] = Shelter.objects.get(slug=self.kwargs['shelter_slug']).id
        return context

    def get_success_url(self):
        return reverse_lazy('shelter:detail', kwargs={'shelter_slug': self.kwargs['shelter_slug']})