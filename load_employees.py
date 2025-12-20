from django.contrib.auth.models import User
from core.models import Employee, Role
import random
import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "syncster.settings")
django.setup()

def run():
    first_names = [
        "John", "Alice", "Brian", "Carla", "David", "Emily", "Frank", "Grace",
        "Henry", "Isabella", "Jack", "Kara", "Liam", "Mia", "Noah", "Olivia",
        "Paul", "Quinn", "Ryan", "Sophia", "Tyler", "Uma", "Victor", "Wendy",
        "Xavier", "Yara", "Zane", "Hannah", "Ethan", "Natalie", "Owen", "Chloe",
        "Lucas", "Ava", "Mason", "Ella", "Logan", "Harper", "Elijah", "Abigail",
        "James", "Charlotte", "Benjamin", "Amelia", "Jacob", "Evelyn", "Michael", "Aria"
    ]

    last_names = [
        "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
        "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
        "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin"
    ]

    roles = list(Role.objects.all())
    count = 0

    for i in range(50):
        first = random.choice(first_names)
        last = random.choice(last_names)
        username = f"{first.lower()}{last.lower()}{random.randint(10,99)}"

        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "first_name": first,
                "last_name": last,
                "email": f"{username}@example.com"
            }
        )

        if created:
            user.set_password("password123")
            user.save()

        Employee.objects.get_or_create(
            user=user,
            defaults={"role": "user"}
        )

        count += 1

    print(f"Added {count} example employees.")


run()