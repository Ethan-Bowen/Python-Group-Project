from django.contrib import admin
from django.urls import path, include
from core import views

from django.contrib.auth import views as auth_views

from core.views import DashboardView, ProfileView, CalendarView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', DashboardView.as_view(), name='dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('calendar/', CalendarView.as_view(), name='calendar'),
    path('api/create-shift/', views.create_shift, name='create_shift'),
    path('api/shift_events/', views.shift_events, name='shift_events'),
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='core/password_reset.html'),name='password_reset'),
    path('', include('core.urls')),
    
]
