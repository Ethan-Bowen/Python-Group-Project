from django.urls import path
from .views import DashboardView, ProfileView, CalendarView

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('calendar/', CalendarView.as_view(), name='calendar'),
]
