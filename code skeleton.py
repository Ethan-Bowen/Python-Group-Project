import os
import calendar
from datetime import datetime

class Shift_schedule:
    def __init__(self, accounts_file="accounts.txt"):
        self.accounts_file = accounts_file
        self.shifts = {}

    def assign_shift(self, username: str, date: str, shift: str):
        if username not in self.shifts:
            self.shifts[username] = {}
        self.shifts[username][date] = shift
        print(f"Assigned shift '{shift}' to {username} on {date}.")
        return True

    def view_shifts(self):
        for username, dates in self.shifts.items():
            print(f"Shifts for {username}:")
            for date, shift in dates.items():
                print(f"  {date}: {shift}")

class Availability:
    def __init__(self, accounts_file="accounts.txt"):
        self.accounts_file = accounts_file
        self.availability_dict = {}

    def load_accounts(self):
        accounts = {}
        try:
            with open(self.accounts_file, "r") as f:
                for line in f:
                    username, password, availability = line.strip().split(",", 2)
                    accounts[username] = {"password": password, "availability": availability}
                    self.availability_dict[username] = availability
        except FileNotFoundError:
            pass
        return accounts

    def update_availability(self, username, availability_str):
        accounts = self.load_accounts()
        if username in accounts:
            accounts[username]['availability'] = availability_str
            self.save_accounts(accounts)
            print(f"Availability for {username} updated successfully.")
            return True
        else:
            print("Username not found.")
            return False

    def save_accounts(self, accounts):
        with open(self.accounts_file, "w") as f:
            for username, info in accounts.items():
                f.write(f"{username},{info['password']},{info['availability']}\n")



    def get_availability(self):
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        shifts = ["Morning", "Afternoon", "Evening"]
        availability_dict = {}
           
        print("\nEnter your availability (Y/N) for each shift on each day:")
        for day in days:
            for shift in shifts:
                while True:
                    choice = input(f"{day} - {shift}: ").strip().lower()
                    if choice in ['y', 'n']:
                        availability_dict[f"{day}_{shift}"] = '1' if choice == 'y' else '0'
                        break
                    else:
                        print("Invalid input. Please enter 'Y' or 'N'.")
        availability_str = ''.join(availability_dict[f"{day}_{shift}"] for day in days for shift in shifts)

        return availability_str

    def display_availability(self, availability_str):
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        shifts = ["Morning", "Afternoon", "Evening"]
        print("\nYour Availability:")
        index = 0
        for day in days:
            print(f"{day}: ", end="")
            for shift in shifts:
                status = "Available" if availability_str[index] == '1' else "Not Available"
                print(f"{shift} - {status}; ", end="")
                index += 1
            print()
    
              

        


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
            
        if not (1 <= day <= calendar.monthrange(self.year, self.month)[1]):
            raise ValueError("Invalid day for this month.")
        self.events.setdefault(day, []).append(event)
        print(f"Event added on {self.year}-{self.month:02d}-{day:02d}: {event}")

    def remove_event(self, day: int, event: str): #This is the function to remove events. is_admin check does the same thing here as above
        
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
            self.admin_menu(username)

        if self.check_credentials(username, password):
            print("\n Login successful!")
            self.general_user_menu(username, password)
        else:
            print("\n Invalid username or password.")

    def create_account(self):
        username = input("Choose a username: ").strip()
        password = input("Choose a password: ").strip()
        availability = 000000000000000000000

        if not username or not password:
            print("Username and password cannot be empty.")
            return

        if self.username_exists(username):
            print("Username already exists. Please choose another.")
            return

        with open(self.accounts_file, "a") as f:
            f.write(f"{username},{password},{availability}\n")
        print("Account created successfully!")

    def check_credentials(self, username, password):
        try:
            with open(self.accounts_file, "r") as f:
                for line in f:
                    stored_user, stored_pass, stored_availability = line.strip().split(",", 2)
                    if stored_user == username and stored_pass == password:
                        return True
        except FileNotFoundError:
            pass
        return False

    def username_exists(self, username):
        try:
            with open(self.accounts_file, "r") as f:
                for line in f:
                    stored_user, stored_pass, stored_availability = line.strip().split(",", 2)
                    if stored_user == username:
                        return True
        except FileNotFoundError:
            pass
        return False
        
    def general_user_menu(self, username, password): #menu used by general users
        print("1. Open user profile")
        print("2. Open avalibility menu")
        print("3. Open shift schedule")
        print("4. Open calendar")
        choice = str(input("Input the number corresponding which window you wish to view"))
        match choice:
            case '1':
                while True:
                    print(f"Username {username}.")
                    print(f"Password {password}.")
                    sub_choice = str(input("Press 1 to exit.").strip())
                    match sub_choice:
                        case '1':
                            break
                self.general_user_menu(username, password)

            case '2':
                availability = Availability()
                while True:
                    print("1. View Availability")
                    print("2. Update Availability")
                    print("3. Back to User Menu")
                    sub_choice = str(input("Enter choice (1-3): ").strip())
                    match sub_choice:
                        case '1':
                            accounts = availability.load_accounts()
                            if username in accounts:
                                availability.display_availability(accounts[username]['availability'])
                            else:
                                print("Username not found.")
                        case '2':
                            new_availability = availability.get_availability()
                            availability.update_availability(username, new_availability)
                        case '3':
                            break
                        case _:
                            print("Bad input. Try again")
                self.general_user_menu(username, password)

            case '3':
                shift = Shift_schedule()
                while True:
                    print("1. View Shifts")
                    print("2. Back to User Menu")
                    sub_choice = str(input("Enter choice (1-2): ").strip())
                    match sub_choice:
                        case '1':
                            shift.view_shifts()
                        case '2':
                            break
                        case _:
                            print("Bad input. Try again")
                self.general_user_menu(username, password)

            case '4':
                now = datetime.now()
                cal = Calendar(now.year, now.month)
                while True:   
                    cal.display()
                    sub_choice = str(input("Press 1 to exit.").strip())
                    match sub_choice:
                        case '1':
                            break
                self.general_user_menu(username, password)
            case _:
                print("Bad input. Try again")
        return        

    def admin_menu(self, username, password): #the admin specific menu
        print("1. Open admin profile")
        print("2. Open avalibility menu")
        print("3. Open shift schedule")
        print("4. Open calendar")
        choice = str(input("Input the number corresponding which window you wish to view"))
        match choice:
            case '1':
                while True:
                    print(f"Username {username}.")
                    print(f"Password {password}.")
                    sub_choice = str(input("Press 1 to exit.").strip())
                    match sub_choice:
                        case '1':
                            break
                self.admin_menu(username, password)


            case '2':
                availability = Availability()
                while True:
                    print("1. View User Availability")

                    print("2. Back to Admin Menu")
                    sub_choice = str(input("Enter choice (1-3): ").strip())
                    match sub_choice:
                        case '1':
                            user_to_view = input("Enter username to view availability: ").strip()
                            accounts = availability.load_accounts()
                            if user_to_view in accounts:
                                availability.display_availability(accounts[user_to_view]['availability'])
                            else:
                                print("Username not found.")
                        case '2':
                            break
                        case _:
                            print("Bad input. Try again")
                self.admin_menu(username, password)

            case '3':
                shift = Shift_schedule()
                while True:
                    print("1. Assign Shift")
                    print("2. View Shifts")
                    print("3. Back to Admin Menu")
                    sub_choice = str(input("Enter choice (1-3): ").strip())
                    match sub_choice:
                        case '1':
                            username = input("Enter username to assign shift: ").strip()
                            date = input("Enter date (YYYY-MM-DD): ").strip()
                            shift_time = input("Enter shift (e.g., Morning, Evening): ").strip()
                            shift.assign_shift(username, date, shift_time)
                        case '2':
                            shift.view_shifts()
                        case '3':
                            break
                        case _:
                            print("Bad input. Try again")
                self.admin_menu(username, password)

            case '4':
                now = datetime.now()
                cal = Calendar(now.year, now.month)
                while True:
                    print("1. Add Event")
                    print("2. Remove Event")
                    print("3. Display Calendar")
                    print("4. Back")
                    cal_choice = input("Enter choice (1-4): ").strip()
                    match cal_choice:
                        case '1':
                            try:
                                day = int(input("Enter day of the month: ").strip())
                                event = input("Enter event description: ").strip()
                                cal.add_event(day, event)
                            except Exception as e:
                                print(f"Error: {e}")
                        case '2':
                            try:
                                day = int(input("Enter day of the month: ").strip())
                                event = input("Enter event description to remove: ").strip()
                                cal.remove_event(day, event)
                            except Exception as e:
                                print(f"Error: {e}")
                        case '3':
                            cal.display()
                        case '4':
                            break
                        case _:
                            print("Bad input. Try again")
                self.admin_menu(username, password)

            case _:
                print("Bad input. Try again")

        return



if __name__ == "__main__":
    Login().run()
