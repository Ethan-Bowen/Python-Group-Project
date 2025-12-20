from django.db import models
from django.contrib.auth.models import User

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(
        max_length=20,
        choices=[
            ("user", "User"),
            ("team_lead", "Team Lead"),
            ("manager", "Manager"),
            ("admin", "Admin"),
        ],
        default="user"
    )

    def __str__(self):
        return f"{self.user.username} ({self.role})"

class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Shift(models.Model):
    employee = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_shifts"
    )

    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    role_needed = models.ForeignKey(
    Role,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name="shifts"
)

    # add color coding 
    color = models.CharField(max_length=20, default="#4e73df")

    # add special instructions
    notes = models.TextField(blank=True)

    def __str__(self):
        emp = self.employee.username if self.employee else "Unassigned"
        return f"{self.date} {self.start_time}-{self.end_time} ({self.role_needed}) — {emp}"

    @property
    def start_datetime(self):
        """Combine date + start_time for FullCalendar."""
        from datetime import datetime
        return datetime.combine(self.date, self.start_time)

    @property
    def end_datetime(self):
        """Combine date + end_time for FullCalendar."""
        from datetime import datetime
        return datetime.combine(self.date, self.end_time)


class Availability(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.employee.user.username} available {self.date} {self.start_time}-{self.end_time}"


class ShiftChangeRequest(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
    reason = models.TextField()
    status = models.CharField(
        max_length=10,
        choices=[("pending", "Pending"), ("approved", "Approved"), ("declined", "Declined")],
        default="pending"
    )
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_by = models.ForeignKey(
        Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name="reviewed_requests"
    )

    def __str__(self):
        return f"{self.employee.user.username} request for {self.shift} ({self.status})"