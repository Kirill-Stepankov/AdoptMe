from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, DeleteView, DetailView
from .models import Shelter, ShelterProfile
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import Http404, HttpRequest
from pytils.translit import slugify

class SheltersView(LoginRequiredMixin, ListView):
    model = ShelterProfile
    template_name = 'shelter/shelters.html'
    context_object_name = 'shelters'
    
    def get_queryset(self):
        return self.request.user.profile.profile.all()

    
class ShelterCreateView(LoginRequiredMixin, CreateView):
    model = Shelter
    template_name = 'shelter/shelter_create.html'
    fields = [
        'name',
        'main_photo',
        'email',
        'about',
    ]

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
    
class ShelterDetailView(DetailView):
    model = Shelter
    template_name = "shelter/shelter_detail.html"
    slug_url_kwarg = 'shelter_slug'
    context_object_name = 'shelter'
