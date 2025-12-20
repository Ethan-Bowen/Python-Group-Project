from django.urls import path
from .views import EmployeeProfileView
from django.contrib.auth import views as auth_views
from .views import (
    DashboardView,
    ProfileView,
    CalendarView,
    approve_request,
    decline_request,
    shift_events,
    create_shift,  
)

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('calendar/', CalendarView.as_view(), name='calendar'),
    path("employee/<int:user_id>/", EmployeeProfileView.as_view(), name="profile"),

    # API endpoints
    path("api/shifts/", shift_events, name="shift_events"),
    path("api/create-shift/", create_shift, name="create_shift"),  

    # Request management
    path('requests/<int:request_id>/approve/', approve_request, name='approve_request'),
    path('requests/<int:request_id>/decline/', decline_request, name='decline_request'),

    # Auth
    path("logout/", auth_views.LogoutView.as_view(template_name="core/logout.html"), name="logout"),
]
