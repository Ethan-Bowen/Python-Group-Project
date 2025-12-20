import os
import calendar

class CalendarBackend:
    def __init__(self, year, month, filename="events.txt"):
        self.year = year
        self.month = month
        self.filename = filename
        self.events = {}
        self.load_event()

    def load_event(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as f:
                    for line in f:
                        date_str, event = line.strip().split(":", 1)
                        year, month, day = map(int, date_str.split("-"))
                        if year == self.year and month == self.month:
                            self.events.setdefault(day, []).append(event.strip())
            except Exception as e:
                print(f"Error loading events: {e}")

    def save_event(self):
        try:
            with open(self.filename, "w") as f:
                for day in sorted(self.events):
                    date_str = f"{self.year}-{self.month:02d}-{day:02d}"
                    for event in self.events[day]:
                        f.write(f"{date_str}: {event}\n")
        except Exception as e:
            print(f"Error saving events: {e}")

    def add_event(self, day: int, event: str):
        if not (1 <= day <= calendar.monthrange(self.year, self.month)[1]):
            raise ValueError("Invalid day for this month.")
        self.events.setdefault(day, []).append(event)
        self.save_event()

    def remove_event(self, day: int, event: str):
        if day in self.events and event in self.events[day]:
            self.events[day].remove(event)
            if not self.events[day]:
                del self.events[day]
            self.save_event()
        else:
            print("Event not found.")