from django.urls import path
from .views import DashboardView, ProfileView, CalendarView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('calendar/', CalendarView.as_view(), name='calendar'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
]
