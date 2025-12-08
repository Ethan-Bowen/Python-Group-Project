import calendar
from datetime import datetime
import os

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
            """if not is_admin():
                raise PermissionError("You do not have permission to add events.")"""
            if not (1 <= day <= calendar.monthrange(self.year, self.month)[1]):
                raise ValueError("Invalid day for this month.")
            self.events.setdefault(day, []).append(event)
            print(f"Event added on {self.year}-{self.month:02d}-{day:02d}: {event}")

    def remove_event(self, day: int, event: str): #This is the function to remove events. is_admin check does the same thing here as above
        """if not is_admin():
            raise PermissionError("You do not have permission to remove events.")"""
        if day in self.events and event in self.events[day]:
            self.events[day].remove(event)
            if not self.events[day]:
                del self.events[day]
            print(f"Event removed from {self.year}-{self.month:02d}-{day:02d}: {event}")
        else:
            print("Event not found.")





class Login:
    def __init__(self, accounts_file="accounts.txt"):
        self.accounts_file = accounts_file
        self.admin_username = "admin"
        self.admin_password = "admin123"
        if not os.path.exists(self.accounts_file):
            with open(self.accounts_file, "w") as f:
                pass

    def run(self):
        while True:
            print("\n=== Welcome to the Login System ===")
            print("1. Login")
            print("2. Create New Account")
            print("3. Exit")
            choice = input("Enter choice (1-3): ").strip()

            if choice == "1":
                self.login()
            elif choice == "2":
                self.create_account()
            elif choice == "3":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

    def login(self):
        username = input("Enter username: ").strip()
        password = input("Enter password: ").strip()

        if username == self.admin_username and password == self.admin_password:
            print("\n Admin login successful!")
            self.admin_menu()
            return

        if self.check_credentials(username, password):
            print("\n Login successful!")
            self.general_user_menu(username)
        else:
            print("\n Invalid username or password.")

    def create_account(self):
        username = input("Choose a username: ").strip()
        password = input("Choose a password: ").strip()

        if not username or not password:
            print("Username and password cannot be empty.")
            return

        if self.username_exists(username):
            print("Username already exists. Please choose another.")
            return

        with open(self.accounts_file, "a") as f:
            f.write(f"{username},{password}\n")
        print("Account created successfully!")

    def check_credentials(self, username, password):
        try:
            with open(self.accounts_file, "r") as f:
                for line in f:
                    stored_user, stored_pass = line.strip().split(",", 1)
                    if stored_user == username and stored_pass == password:
                        return True
        except FileNotFoundError:
            pass
        return False

    def username_exists(self, username):
        try:
            with open(self.accounts_file, "r") as f:
                for line in f:
                    stored_user, _ = line.strip().split(",", 1)
                    if stored_user == username:
                        return True
        except FileNotFoundError:
            pass
        return False
        
    def general_user_menu(self, username): #menu used by general users
        print("User login succesful")
        print("1. Open user profile")
        print("2. Open avalibility menu")
        print("3. Open shift schedule")
        print("4. Open calendar")
        choice = str(input("Input the number corresponding which window you wish to view"))
        match choice:
            #case '1':
                #load_profile()
            #case '2':
                #open_avaliability_menu()
            #case '3':
                #open_shift_schedule()
            case '4':
                now = datetime.now()
                cal = Calendar(now.year, now.month)
                cal.display()
            case _:
                print("Bad input. Try again")
        return        

    def admin_menu(self, username): #the admin specific menu
        print("Admin login succesful")
        print("1. Open admin profile")
        print("2. Open avalibility menu")
        print("3. Open shift schedule")
        print("4. Open calendar")
        choice = str(input("Input the number corresponding which window you wish to view"))
        match choice:
            #case '1':
                #load_admin_profile()
            #case '2':
                #open_avaliability_menu()
            #case '3':
                #shift_schedule()
            case '4':
                now = datetime.now()
                cal = Calendar(now.year, now.month)
                cal.display()
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
