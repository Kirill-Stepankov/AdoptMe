from django.shortcuts import render
from .models import PetAdvert, PetAdvertPhoto
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect
from .forms import PetAdvertForm, PetAdvertPhotoForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin
from django.http import Http404



class CreatePetAdView(LoginRequiredMixin, CreateView):
    model = PetAdvert
    form_class = PetAdvertForm
    template_name = "petadvert/create_pet_ad.html"

    def form_valid(self, form):
        PetAdvert.objects.create(owner=self.request.user.profile, **form.cleaned_data)
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

    def get_success_url(self):
        return reverse_lazy('petad:petad_detail', kwargs={'petad_pk': self.kwargs['petad_pk']})
    
    def post(self, request, *args, **kwargs):
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
    template_name = 'petadvert/petad_edit.html'

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
