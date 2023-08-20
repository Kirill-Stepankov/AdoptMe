from django.http import Http404
from .models import ShelterProfile

class AcceptDenyMixin:
    def get_object(self, queryset = None):
        obj =  super().get_object(queryset)
        shelterprofile = obj.shelter.shelter.filter(profile=self.request.user.profile).first()
        if not shelterprofile:
            raise Http404
        if shelterprofile.role == ShelterProfile.RoleChoices.MODERATOR:
            raise Http404
        return obj       
    
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)