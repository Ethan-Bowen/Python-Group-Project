import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "syncster.settings")
django.setup()

from django.contrib.auth.models import User
from core.models import Employee

def run():
    superusers = User.objects.filter(is_superuser=True).values_list("id", flat=True)
    employees = Employee.objects.exclude(user_id__in=superusers)
    print("Found", employees.count(), "employees to delete")

    for emp in employees:
        try:
            emp.user.delete()
        except Exception as e:
            print("Error deleting user:", e)

        try:
            emp.delete()
        except Exception as e:
            print("Error deleting employee:", e)

    print("Finished deleting non-admin users.")

run()