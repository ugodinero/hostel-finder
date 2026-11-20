from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from hostels.views import landing

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing, name='landing'),
    path('hostels/', include('hostels.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
