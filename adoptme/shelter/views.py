from typing import Any, Dict, Optional
from django import http
from django.db import models
from django.db.models import Q, Count, F, Value, SlugField
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http.response import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView, View
from .models import Shelter, ShelterProfile, ShelterPhoto, ShelterApply
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import Http404, HttpRequest, HttpResponse
from pytils.translit import slugify
from .forms import CreateShelterForm, ShelterPhotoForm, ShelterApplyForm, EditPostForm
from django.views.generic.edit import FormMixin
from petadvert.models import PetAdvert
from userprofile.models import Profile
from .utils import AcceptDenyMixin


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
        context['3pets'] = PetAdvert.objects.filter(shelter__slug=self.kwargs['shelter_slug'], is_published=True)[:3]
        context['more_than_3'] = PetAdvert.objects.filter(shelter__slug=self.kwargs['shelter_slug'], is_published=True).count()>3
        
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
        context['shelter_id'] = get_object_or_404(Shelter, slug=self.kwargs['shelter_slug']).id
        return context

    def get_success_url(self):
        return reverse_lazy('shelter:detail', kwargs={'shelter_slug': self.kwargs['shelter_slug']})
    
    def form_valid(self, form):
        if ShelterApply.objects.filter(profile=form.cleaned_data.get('profile'), shelter__slug=self.kwargs['shelter_slug']).first():
            return self.form_invalid(form)
        if form.cleaned_data.get('profile').profile.filter(shelter__slug=self.kwargs['shelter_slug']):
            return self.form_invalid(form)
        return super().form_valid(form)
    
class ShelterLeaveView(LoginRequiredMixin, DeleteView):
    model = Shelter
    pk_url_kwarg = 'shelter_pk'

    def get(self, request: HttpRequest, *args, **kwargs):
        return self.post(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs): 
        self.object = self.get_object()
        shelter = self.object
        shelterprofile = shelter.shelter.filter(profile=request.user.profile) 
        shelterprofile.delete() 
        return redirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse_lazy('shelter:shelters')
    
    def get_object(self, queryset = None):
        obj =  super().get_object(queryset)
        shelterprofile = obj.shelter.filter(profile=self.request.user.profile).first()
        if not shelterprofile:
            raise Http404
        if shelterprofile.role != ShelterProfile.RoleChoices.MODERATOR:
            raise Http404
        return obj
    
class ShelterSettingsView(LoginRequiredMixin, UpdateView):
    model = Shelter
    slug_url_kwarg = 'shelter_slug'
    template_name = 'shelter/shelter_settings.html'
    fields = [
        'email',
        'about',
        'city',
        'adress',
        'contact_ref'
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['edit_active'] = True
        return context  

    def get_success_url(self) -> str:
        return reverse_lazy('shelter:settings', kwargs={'shelter_slug': self.kwargs['shelter_slug']})
    
    def get_object(self, queryset = None) :
        obj = super().get_object(queryset)
        if not obj.shelter.filter(profile=self.request.user.profile).first():
            raise Http404
        return obj
    
class ShelterCreatePetAdView(LoginRequiredMixin, CreateView):
    model = PetAdvert
    fields = [
        'name',
        'photo',
        'color',
        'about',
        'gender',
        'type',
        'size',
        'age',
        'house_trained',
        'health',
        'breed'
    ]
    template_name = 'shelter/shelter_createad.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shelter'] = get_object_or_404(Shelter, slug=self.kwargs['shelter_slug'])
        context['create_active'] = True
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            raise Http404
        if not get_object_or_404(Shelter, slug=self.kwargs['shelter_slug']).shelter.filter(profile=self.request.user.profile).first():
            raise Http404
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse_lazy('shelter:settings', kwargs={'shelter_slug': self.kwargs['shelter_slug']})

    def form_valid(self, form):
        is_published = ShelterProfile.objects.filter(shelter=get_object_or_404(Shelter, slug=self.kwargs['shelter_slug']), role=ShelterProfile.RoleChoices.ADMIN).first().profile == self.request.user.profile
        PetAdvert.objects.create(shelter=Shelter.objects.get(slug=self.kwargs['shelter_slug']), author=self.request.user.profile, is_published=is_published, city=get_object_or_404(Shelter, slug=self.kwargs['shelter_slug']).city, **form.cleaned_data)
        return redirect(self.get_success_url())
    
class ShelterModsView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = 'shelter/shelter_mods.html'
    context_object_name = 'mods'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shelter'] = get_object_or_404(Shelter, slug=self.kwargs['shelter_slug'])
        context['mods_active'] = True
        return context
    
    def get_queryset(self):
        ordering = self.request.GET.get('ordering_type')
        if get_object_or_404(Shelter, slug=self.kwargs['shelter_slug']).shelter.filter(role=ShelterProfile.RoleChoices.ADMIN).first().profile != self.request.user.profile:
            raise Http404
        query = self.request.GET.get("q")
        queryset = Profile.objects.annotate(num_posts=Count('author', filter=Q(Q(author__shelter=get_object_or_404(Shelter, slug=self.kwargs['shelter_slug'])) & Q(author__is_published=True)))).order_by(ordering or 'user__username')
        if query:
            queryset = queryset.annotate(shelter=Value(self.kwargs['shelter_slug'], output_field=SlugField())).filter(profile__shelter__slug=F('shelter')).filter(Q(slug__icontains=query))
        else:
            queryset = queryset.annotate(shelter=Value(self.kwargs['shelter_slug'], output_field=SlugField())).filter(profile__shelter__slug=F('shelter'))

        return queryset

    
class ShelterDeleteModView(LoginRequiredMixin, DeleteView):
    model = Shelter
    pk_url_kwarg = 'shelter_pk'

    def get(self, request: HttpRequest, *args, **kwargs):
        return self.post(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs): 
        self.object = self.get_object()
        shelter = self.object
        shelterprofile = shelter.shelter.filter(profile=get_object_or_404(Profile, pk=self.kwargs['mod_pk'])) 
        shelterprofile.delete() 
        return redirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse_lazy('shelter:mods', kwargs={'shelter_slug': self.object.slug})
    
    def get_object(self, queryset = None):
        obj =  super().get_object(queryset)
        shelterprofile = obj.shelter.filter(profile=self.request.user.profile).first()
        if not shelterprofile:
            raise Http404
        if shelterprofile.role == ShelterProfile.RoleChoices.MODERATOR:
            raise Http404
        if shelterprofile.profile == get_object_or_404(Profile, pk=self.kwargs['mod_pk']):
            raise Http404
        return obj
    
class ShelterApplicationsView(LoginRequiredMixin, ListView):
    model = ShelterApply
    template_name = 'shelter/shelter_applies.html'
    context_object_name = 'applies'
    paginate_by = 5

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context['membership_active'] = True
        context['shelter'] = get_object_or_404(Shelter, slug=self.kwargs['shelter_slug'])
        return context
    
    def get_queryset(self):
        query = self.request.GET.get("q")
        ordering = self.request.GET.get("ordering_type")
        if query:
            return ShelterApply.objects.filter(shelter=get_object_or_404(Shelter, slug=self.kwargs['shelter_slug']), profile__slug__icontains=query).order_by(ordering or 'profile__slug')
        return ShelterApply.objects.filter(shelter=get_object_or_404(Shelter, slug=self.kwargs['shelter_slug'])).order_by(ordering or 'profile__slug')
    
class AcceptApplyView(LoginRequiredMixin, AcceptDenyMixin, DeleteView):
    model = ShelterApply
    pk_url_kwarg = 'apply_pk'
 
    def post(self, request, *args, **kwargs): 
        self.object = self.get_object()
        ShelterProfile.objects.create(shelter=self.object.shelter, profile=self.object.profile, role=ShelterProfile.RoleChoices.MODERATOR)
        self.object.delete() 
        return redirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse_lazy('shelter:appls_mods', kwargs={'shelter_slug': self.object.shelter.slug})
    
class DenyApplyView(LoginRequiredMixin, AcceptDenyMixin, DeleteView):
    model = ShelterApply
    pk_url_kwarg = 'apply_pk'
    
    def post(self, request, *args, **kwargs): 
        self.object = self.get_object()
        self.object.delete() 
        return redirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse_lazy('shelter:appls_mods', kwargs={'shelter_slug': self.object.shelter.slug})

class ShelterPostsAppliesView(LoginRequiredMixin, ListView):
    model = PetAdvert
    template_name = 'shelter/shelter_post_applies.html'
    paginate_by = 1
    context_object_name = 'applies'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shelter'] = get_object_or_404(Shelter, slug=self.kwargs['shelter_slug'])
        context['confirmation_active'] = True
        return context
    
    def get_queryset(self):
        if get_object_or_404(Shelter, slug=self.kwargs['shelter_slug']).shelter.filter(role=ShelterProfile.RoleChoices.ADMIN).first().profile != self.request.user.profile:
            raise Http404
        query = self.request.GET.get("q")
        ordering = self.request.GET.get('ordering_type')
        if query:
            return PetAdvert.objects.filter(shelter=get_object_or_404(Shelter, slug=self.kwargs['shelter_slug']), is_published=False, author__slug__icontains=query).order_by(ordering or 'author__slug')           
        return PetAdvert.objects.filter(shelter=get_object_or_404(Shelter, slug=self.kwargs['shelter_slug']), is_published=False).order_by(ordering or 'author__slug')

class AcceptPostView(LoginRequiredMixin, AcceptDenyMixin, UpdateView):
    model = PetAdvert
    pk_url_kwarg = 'petad_pk'

    def post(self, request, *args, **kwargs): 
        self.object = self.get_object()
        PetAdvert.objects.filter(pk=self.object.id).update(is_published=True) 
        return redirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse_lazy('shelter:appls_posts', kwargs={'shelter_slug': self.object.shelter.slug})
    
class DenyPostView(LoginRequiredMixin, AcceptDenyMixin, DeleteView):
    model = PetAdvert
    pk_url_kwarg = 'petad_pk'

    def post(self, request, *args, **kwargs): 
        self.object = self.get_object()
        self.object.delete()
        return redirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse_lazy('shelter:appls_posts', kwargs={'shelter_slug': self.object.shelter.slug})

class ShelterPostsView(LoginRequiredMixin, ListView):
    model = PetAdvert
    template_name = 'shelter/shelter_posts.html'
    paginate_by = 5
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shelter'] = get_object_or_404(Shelter, slug=self.kwargs['shelter_slug'])
        context['pets_active'] = True
        return context
    
    def get_queryset(self):
        shelter = get_object_or_404(Shelter, slug=self.kwargs['shelter_slug'])
        shelterprofile = shelter.shelter.filter(profile=self.request.user.profile).first()
        if not shelterprofile:
            raise Http404
        
        query = self.request.GET.get("q")
        ordering = self.request.GET.get('ordering_type')
        if query:
            return PetAdvert.objects.filter(shelter=get_object_or_404(Shelter, slug=self.kwargs['shelter_slug']), is_published=True, name__icontains=query).order_by(ordering or '-time_create')            
        return PetAdvert.objects.filter(shelter=get_object_or_404(Shelter, slug=self.kwargs['shelter_slug']), is_published=True).order_by(ordering or '-time_create') 

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
        return reverse_lazy('shelter:pets', kwargs={'shelter_slug': self.object.shelter.slug})
    
    def get_object(self, queryset = None):
        obj =  super().get_object(queryset)
        if not obj.shelter:
            raise Http404        
        shelterprofile = obj.shelter.shelter.filter(profile=self.request.user.profile).first()
        if not shelterprofile:
            raise Http404
        if shelterprofile.role == ShelterProfile.RoleChoices.MODERATOR:
            raise Http404
        return obj
    
class ShetlerEditPostView(LoginRequiredMixin, UpdateView):
    model = PetAdvert
    context_object_name = 'ad'
    template_name = 'shelter/edit_ad.html'
    pk_url_kwarg = 'petad_pk'
    form_class = EditPostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shelter'] = get_object_or_404(Shelter, pk=self.kwargs['shelter_pk'])
        context['pets_active'] = True
        return context
    
    def get_object(self, queryset=None):
        obj =  super().get_object(queryset)
        if not obj.shelter:
            raise Http404
        if obj.shelter != get_object_or_404(Shelter, pk=self.kwargs['shelter_pk']):
            raise Http404
        if not get_object_or_404(Shelter, pk=self.kwargs['shelter_pk']).shelter.filter(profile=self.request.user.profile).first():
            raise Http404
        return obj
    
    def get_success_url(self) -> str:
        return reverse_lazy('shelter:pets', kwargs={'shelter_slug': get_object_or_404(Shelter, pk=self.kwargs['shelter_pk']).slug })

class SheltersListView(ListView):
    model = Shelter
    context_object_name = 'shelters'
    template_name = 'shelter/shelter_list.html'
    paginate_by = 8

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context['cities'] = Shelter.objects.values_list('city').order_by().distinct()
        return context
    
    def get_queryset(self):
        params = self.request.GET
        city = params.get('city', '')
        minp = params.get('exp-min', 0)
        maxp = params.get('exp-max', 3000)
        ordering = params.get('ordering_type', '-name')

        return Shelter.objects.annotate(num_ads=Count('shelter')).filter(city__icontains=city, num_ads__gte=minp, num_ads__lte=maxp).order_by(ordering)
    