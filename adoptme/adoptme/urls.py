from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from userprofile.views import pageNotFound, serverError

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('userprofile.urls')),
    path('shelter/', include('shelter.urls')),
    path('petad/', include('petadvert.urls'))
]

handler404 = pageNotFound
handler500 = serverError

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)