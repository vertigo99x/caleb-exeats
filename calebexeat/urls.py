from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include, re_path

from .router import router
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

vue_views_regex = r'\/|\b'.join([

    # List all your react routes here
    'users',
    'history',
    'events',
    'profile',
]) + r'\/'


urlpatterns = [
    path("admin/", admin.site.urls),
    
    path('api/v1/', include('djoser.urls')),
    path('api/v1/', include('djoser.urls.authtoken')), 
    path('api/v1/',include('api.urls')),
    path('api/v1/',include(router.urls)),
    path("", TemplateView.as_view(template_name="index.html")),
    re_path(vue_views_regex, TemplateView.as_view(template_name="index.html")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
