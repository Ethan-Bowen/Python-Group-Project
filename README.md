# SDEV220-Syncster

Syncster — Shift Scheduling & Employee Management
Syncster is a lightweight Django-based scheduling system designed for small teams, public safety departments, and student projects that need a clean way to manage employees, roles, and shifts. It includes a calendar UI, profile management, and a simple workflow for shift‑change requests.

Features
- Interactive calendar with FullCalendar integration
- Employee profiles with admin‑only editing
- Shift creation via modal form
- Shift‑change request workflow (approve/decline)
- Role-based access (team lead, manager, admin)
- Dynamic profile pages (/profile/<id>/)
- JSON API endpoints for calendar events and shift creation
  
Tech Stack
- Python
- Django
- SQLite 
- FullCalendar.js
- Bootstrap 5
- css3
- JSON API endpoints
- AJAX/Fetch

Running the Project
- Set up virtual environment
- (Python -m venv env)
- (env\Scripts\activate)
- pip install -r requirements.txt
- python manage.py migrate
- python manage.py runserver


Visit the app at:
http://127.0.0.1:8000/
https://alirho.pythonanywhere.com/
