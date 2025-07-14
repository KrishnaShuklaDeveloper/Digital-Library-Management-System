from django.urls import path
from . import views
from .views import admin_logout

urlpatterns = [
    path('', views.admin_login, name='admin_login'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('logout/', admin_logout, name='admin_logout'),
]
