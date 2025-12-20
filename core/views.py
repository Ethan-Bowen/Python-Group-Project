from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import json

from .models import ShiftChangeRequest, Shift, Role, Employee
from .calendar_backend import CalendarBackend

# Approve / Decline Requests

@login_required
def approve_request(request, request_id):
    req = get_object_or_404(ShiftChangeRequest, id=request_id)
    if request.user.employee.role in ["team_lead", "manager", "admin"]:
        req.status = "approved"
        req.reviewed_by = request.user.employee
        req.save()
    return redirect("core/requests_list")


@login_required
def decline_request(request, request_id):
    req = get_object_or_404(ShiftChangeRequest, id=request_id)
    if request.user.employee.role in ["team_lead", "manager", "admin"]:
        req.status = "declined"
        req.reviewed_by = request.user.employee
        req.save()
    return redirect("core/requests_list")


# Basic Views

class DashboardView(TemplateView):
    template_name = "core/dashboard.html"


class ProfileView(TemplateView):
    template_name = "core/profile.html"


class CalendarView(TemplateView):
    template_name = "core/calendar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["roles"] = Role.objects.all()
        context["employees"] = Employee.objects.select_related("user").all()
        return context



# Employee Profile (click from calendar)

class EmployeeProfileView(TemplateView):
    template_name = "core/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs["user_id"]
        context["employee"] = Employee.objects.select_related("user").get(user__id=user_id)
        return context



# Calendar Events JSON
@csrf_exempt
def shift_events(request):
    shifts = Shift.objects.all()
    events = []

    for shift in shifts:
        try:
            # Safe employee lookup
            if shift.employee and hasattr(shift.employee, "username"):
                employee_name = shift.employee.get_full_name() or shift.employee.username
                employee_id = shift.employee.id
            elif shift.employee and hasattr(shift.employee, "user"):
                employee_name = shift.employee.user.get_full_name() or shift.employee.user.username
                employee_id = shift.employee.user.id
            else:
                employee_name = "Unassigned"
                employee_id = None

            events.append({
                "id": shift.id,
                "title": employee_name,
                "start": f"{shift.date}T{shift.start_time}",
                "end": f"{shift.date}T{shift.end_time}",
                "url": f"/employee/{employee_id}/" if employee_id else None,
            })

        except Exception as e:
            print("Error building event:", e)

    return JsonResponse(events, safe=False)



# Create Shift (modal save)

@csrf_exempt
def create_shift(request):
    if request.method == "POST":
        data = json.loads(request.body)

        role = Role.objects.get(id=data["role"])

        # If no employee is assigned, user will be None
        user = None
        if data.get("employee"):
            user = User.objects.get(id=data["employee"])

        shift = Shift.objects.create(
            date=data["date"],
            start_time=data["start_time"],
            end_time=data["end_time"],
            role_needed=role,
            employee=user
        )

        return JsonResponse({"status": "ok", "id": shift.id})