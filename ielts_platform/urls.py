"""
URL configuration for ielts_platform project - Django MVT
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Redirect root to auth page
    path('', RedirectView.as_view(url='/auth/', permanent=False)),
    
    # MVT URLs
    path('', include('organizations.urls_mvt')),
    path('', include('exams.urls_mvt')),
    path('results/', include('results.urls_mvt')),
    path('students/', include('students.urls')),
    path('support/', include('support.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
