"""
URLs principales du projet HôtelLuxe
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/dashboard/', permanent=False), name='home'),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('rooms/', include('rooms.urls', namespace='rooms')),
    path('reservations/', include('reservations.urls', namespace='reservations')),
    path('clients/', include('clients.urls', namespace='clients')),
    path('dashboard/', include('dashboard.urls', namespace='dashboard')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
