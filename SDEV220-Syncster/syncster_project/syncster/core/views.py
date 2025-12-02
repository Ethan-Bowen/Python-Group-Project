from django.views.generic import TemplateView

class DashboardView(TemplateView):
    template_name = "core/dashboard.html"

class ProfileView(TemplateView):
    template_name = "core/profile.html"

class CalendarView(TemplateView):
    template_name = "core/calendar.html"
