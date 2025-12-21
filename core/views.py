from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import json

from .models import ShiftChangeRequest, Shift, Role, Employee
from .calendar_backend import CalendarBackend
from .models import Shift, Employee, Role
from core.models import Shift



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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["employees"] = Employee.objects.all()
        context["roles"] = Role.objects.all()
        context["shifts"] = Shift.objects.all()
        return context


class ProfileView(TemplateView):
    template_name = "core/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        employee = getattr(user, "employee", None)
        context['employee'] = employee
        context['user_obj'] = user
        return context


class CalendarView(TemplateView):
    template_name = "core/calendar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["roles"] = Role.objects.all()
        context["employees"] = Employee.objects.select_related("user").all()
        return context



# Employee Profile from calendar

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
                "url": f"/profile/{employee_id}/" if employee_id else None,
            })

        except Exception as e:
            print("Error building event:", e)
            
    print("SHIFTS:", list(Shift.objects.values()))
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
       
@login_required
def edit_profile(request, user_id):
    if not request.user.is_superuser and request.user.employee.role != "admin":
        return redirect("profile_detail", user_id=user_id)

    user = get_object_or_404(User, id=user_id)
    employee = user.employee

    if request.method == "POST":
        user.email = request.POST.get("email")
        employee.phone_number = request.POST.get("phone_number")
        employee.emergency_contact_name = request.POST.get("emergency_contact_name")
        employee.emergency_contact_phone = request.POST.get("emergency_contact_phone")
        employee.address = request.POST.get("address")
        employee.job_title = request.POST.get("job_title")
        employee.notes = request.POST.get("notes")

        user.save()
        employee.save()

        return redirect("profile_detail", user_id=user_id)

    return render(request, "core/edit_profile.html", {
        "user_obj": user,
        "employee": employee
    })

        
def schedule_status(request):
    today = timezone.now().date()
    week_end = today + timedelta(days=7)

    # Days with no shifts
    days = [today + timedelta(days=i) for i in range(7)]
    unscheduled_days = [
        day for day in days
        if not Shift.objects.filter(date=day).exists()
    ]

    # Roles with no assigned employee
    unassigned_roles = Role.objects.filter(employee__isnull=True)

    # Employees with no shifts this week
    employees_without_shifts = [
        e for e in Employee.objects.all()
        if not Shift.objects.filter(employee=e, start_time__date__range=[today, week_end]).exists()
    ]

    return render(request, "schedule_status.html", {
        "unscheduled_days": unscheduled_days,
        "unassigned_roles": unassigned_roles,
        "employees_without_shifts": employees_without_shifts,
    })
    
@login_required
def profile_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    employee = getattr(user, "employee", None)

    return render(request, "core/profile.html", {
        "user_obj": user,
        "employee": employee
    })


        
