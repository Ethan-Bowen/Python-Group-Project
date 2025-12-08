import calendar
from datetime import datetime

def is_admin(): #will check if the user ID is the admin ID (I believe we should hardcode this)
    return False

class Shift_schedule: #contains all the info on the shift schedule
    def empty(self):
        return



class User_profile: #contains the info for a user, including their name, ID, position, etc.
    def empty(self):
        return



class Calendar: #contains the info for the calendar
    def __init__(self, year: int, month: int):
        if not (1 <= month <= 12):
            raise ValueError("Month must be between 1 and 12.")
        self.year = year
        self.month = month
        self.events = {}

    def display(self): #This is the display for the calendar
        cal = calendar.TextCalendar(calendar.SUNDAY)
        month_str = cal.formatmonth(self.year, self.month)
        print(month_str)

        if self.events:
            print("Events:")
            for day in sorted(self.events):
                date_str = f"{self.year}-{self.month:02d}-{day:02d}"
                print(f" {date_str}: {', '.join(self.events[day])}")
        else:
            print("No events scheduled.")

        def add_event(self, day: int, event: str): #This is the function to add events. If admin returns false, then an error is thrown
            if not is_admin():
                raise PermissionError("You do not have permission to add events.")
            if not (1 <= day <= calendar.monthrange(self.year, self.month)[1]):
                raise ValueError("Invalid day for this month.")
            self.events.setdefault(day, []).append(event)
            print(f"Event added on {self.year}-{self.month:02d}-{day:02d}: {event}")

    def remove_event(self, day: int, event: str): #This is the function to remove events. is_admin check does the same thing here as above
        if not is_admin():
            raise PermissionError("You do not have permission to remove events.")
        if day in self.events and event in self.events[day]:
            self.events[day].remove(event)
            if not self.events[day]:
                del self.events[day]
            print(f"Event removed from {self.year}-{self.month:02d}-{day:02d}: {event}")
        else:
            print("Event not found.")
    return


def load_info(): #loads the info from the data files into the program
    return


def export_info(): #exports all of the data into the data files
    return




def login(): #will compare the input info to the possible logins in the database
             #if login is successful, the user's profile will be put into a variable, and passed along as needed
    return


def create_profile(): #creates a profile and adds it to the memory
    return


def general_user_menu(): #menu used by general users
    print("User login succesful")
    print("1. Open user profile")
    print("2. Open avalibility menu")
    print("3. Open shift schedule")
    print("4. Open calendar")
    choice = str(input("Input the number corresponding which window you wish to view"))
    match choice:
        case '1':
            load_profile()
        case '2':
            open_avaliability_menu()
        case '3':
            open_shift_schedule()
        case '4':
            open_calendar()
        case _:
            print("Bad input. Try again")
    return


def load_profile(): #the user's profile info is printed here
    return


def open_avaliability_menu(): #the avaliability menu for the user is printed here, and the user is given the choice to edit it
    return

def edit_avalability(): #the availability can be changed here
    return

def open_shift_schedule(): #the shift schedule is printed here
    return


def admin_menu(): #the admin specific menu
    print("Admin login succesful")
    print("1. Open admin profile")
    print("2. Open avalibility menu")
    print("3. Open shift schedule")
    print("4. Open calendar")
    choice = str(input("Input the number corresponding which window you wish to view"))
    match choice:
        case '1':
            load_admin_profile()
        case '2':
            admin_open_avaliability_menu()
        case '3':
            admin_open_shift_schedule()
        case '4':
            admin_open_calendar()
        case _:
            print("Bad input. Try again")

    return


def load_admin_profile(): #prints the profile used by the admin
    return


def admin_open_avaliability_menu(): #prints the avaliability of all users
    return


def admin_open_shift_schedule(): #prints the schedule of all users and allows for editing of the schedule
    display_shift_schedule()
    edit_display_schedule()
    return


def display_shift_schedule(): #code for displaying the schedule
    return



def main(): #main code block
    load_info()

    has_profile = input("Enter 1 if you already have a profile, or any other character otherwise")
    if str(has_profile) != '1':
        return

    login()

    done = False
    while not done:
        if is_admin():
            admin_menu()
        else:
            general_user_menu()
