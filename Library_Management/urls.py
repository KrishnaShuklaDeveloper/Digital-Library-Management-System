"""
URL configuration for Library_Management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from library import views
from django.urls import path, include

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('user-login/', views.user_login, name='user_login'),
    path('admin/', admin.site.urls),
    path('custom-admin/', include('admin_panel.urls')),
    path('users/', include('users.urls')),
    path('library/', include('library.urls')),
]

from django.conf import settings
from django.conf.urls.static import static

# Existing urlpatterns...
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




