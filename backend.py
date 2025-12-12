import os
import calendar
from datetime import datetime

class Shift_schedule: #contains the info for the shift schedule
    def __init__(self, accounts_file="accounts.txt"):
        self.accounts_file = accounts_file
        self.shifts = {}

    def assign_shift(self, username: str, date: str, shift: str): #assigns a shift to a user on a specific date
        if username not in self.shifts: #if the user does not have any shifts assigned yet
            self.shifts[username] = {}
        self.shifts[username][date] = shift #assign the shift to the user on the specified date
        print(f"Assigned shift '{shift}' to {username} on {date}.")
        return True

    def view_shifts(self): #views the shifts assigned to users
        for username, dates in self.shifts.items(): #iterate through the users and their assigned shifts
            print(f"Shifts for {username}:")
            for date, shift in dates.items(): #iterate through the dates and shifts for the user
                print(f"  {date}: {shift}")

class Availability:
    def __init__(self, accounts_file="accounts.txt"):
        self.accounts_file = accounts_file
        self.availability_dict = {}

    def load_accounts(self): #loads the accounts from a text file
        accounts = {}
        try:
            with open(self.accounts_file, "r") as f: #opens the accounts file
                for line in f:
                    username, password, availability = line.strip().split(",", 2) #splits the line into username, password, and availability
                    accounts[username] = {"password": password, "availability": availability} #stores the account info in a dictionary
                    self.availability_dict[username] = availability
        except FileNotFoundError:
            pass
        return accounts

    def update_availability(self, username, availability_str): #updates the availability for a specific user
        accounts = self.load_accounts() #loads the accounts
        if username in accounts: #checks if the username exists
            accounts[username]['availability'] = availability_str #updates the availability
            self.save_accounts(accounts) #saves the updated accounts
            print(f"Availability for {username} updated successfully.")
            return True
        else:
            print("Username not found.")
            return False

    def save_accounts(self, accounts): #saves the accounts to a text file
        with open(self.accounts_file, "w") as f: #opens the accounts file for writing
            for username, info in accounts.items(): #iterates through the accounts
                f.write(f"{username},{info['password']},{info['availability']}\n") #writes the account info to the file



    def get_availability(self): #gets the availability from user input
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        shifts = ["Morning", "Afternoon", "Evening"]
        availability_dict = {}
           
        print("\nEnter your availability (Y/N) for each shift on each day:")
        for day in days: #iterates through the days of the week
            for shift in shifts: #iterates through the shifts
                while True:
                    choice = input(f"{day} - {shift}: ").strip().lower() #gets user input for availability
                    if choice in ['y', 'n']: #validates the input
                        availability_dict[f"{day}_{shift}"] = '1' if choice == 'y' else '0' #stores the availability in a dictionary
                        break
                    else:
                        print("Invalid input. Please enter 'Y' or 'N'.")
        availability_str = ''.join(availability_dict[f"{day}_{shift}"] for day in days for shift in shifts) #converts the availability dictionary to a string

        return availability_str

    def display_availability(self, availability_str): #displays the availability in a readable format
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        shifts = ["Morning", "Afternoon", "Evening"]
        print("\nYour Availability:")
        index = 0
        for day in days: #iterates through the days of the week
            print(f"{day}: ", end="")
            for shift in shifts: #iterates through the shifts
                status = "Available" if availability_str[index] == '1' else "Not Available"
                print(f"{shift} - {status}; ", end="")
                index += 1
            print()
    

class Calendar: #contains the info for the calendar
    def __init__(self, year: int, month: int, filename="events.txt"):
        if not (1 <= month <= 12):
            raise ValueError("Month must be between 1 and 12.")
        self.year = year
        self.month = month
        self.events = {}
        self.filename = filename

    def display(self): #This is the display for the calendar
        cal = calendar.TextCalendar(calendar.SUNDAY)
        month_str = cal.formatmonth(self.year, self.month)
        print(month_str)

        if self.events: #If there are events scheduled, they are printed here
            print("Events:")
            for day in sorted(self.events): #iterates through the days with events
                date_str = f"{self.year}-{self.month:02d}-{day:02d}"
                print(f" {date_str}: {', '.join(self.events[day])}")
        else:
            print("No events scheduled.")
    
    def load_event(self): #This function loads events from a text file
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as f: #opens the events file
                    for line in f:
                        date_str, event = line.strip().split(":", 1) #splits the line into date and event
                        year, month, day = map(int, date_str.split("-")) #splits the date into year, month, and day
                        if year == self.year and month == self.month: #checks if the event is in the current month and year
                            self.events.setdefault(day, []).append(event.strip()) #stores the event in a dictionary
            except Exception as e:
                print(f"Error loading events: {e}")

    def save_event(self): #This function saves events to a text file)
        try:
            with open(self.filename, "w") as f: #opens the events file for writing
                for day in sorted(self.events): #iterates through the days with events
                    date_str = f"{self.year}-{self.month:02d}-{day:02d}" #formats the date string
                    for event in self.events[day]: #iterates through the events for the day
                        f.write(f"{date_str}: {event}\n") #writes the event to the file
        except Exception as e:
            print(f"Error saving events: {e}")


    def add_event(self, day: int, event: str): #This is the function to add events. If admin returns false, then an error is thrown
            
        if not (1 <= day <= calendar.monthrange(self.year, self.month)[1]): #checks if the day is valid for the month
            raise ValueError("Invalid day for this month.")
        self.events.setdefault(day, []).append(event) #adds the event to the dictionary
        self.save_event()
        print(f"Event added on {self.year}-{self.month:02d}-{day:02d}: {event}")

    def remove_event(self, day: int, event: str): #This is the function to remove events. is_admin check does the same thing here as above
        
        if day in self.events and event in self.events[day]: #checks if the event exists for the specified day
            self.events[day].remove(event) #removes the event from the dictionary
            if not self.events[day]: #if there are no more events for the day, remove the day from the dictionary
                del self.events[day] #removes the day from the dictionary
            self.save_event() #saves the updated events to the file
            print(f"Event removed from {self.year}-{self.month:02d}-{day:02d}: {event}")
        else:
            print("Event not found.")





class Login: #main login system class
    def __init__(self, accounts_file="accounts.txt"):
        self.accounts_file = accounts_file
        self.admin_username = "admin"
        self.admin_password = "admin123"
        if not os.path.exists(self.accounts_file):
            with open(self.accounts_file, "w") as f:
                pass


    def run(self): #main login loop
        while True: #main menu
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

    def login(self): #handles the login process
        username = input("Enter username: ").strip()
        password = input("Enter password: ").strip()

        if username == self.admin_username and password == self.admin_password: #checks if the username and password match the admin credentials
            print("\n Admin login successful!")
            self.admin_menu(username, password)

        if self.check_credentials(username, password): #checks if the username and password match an existing account
            print("\n Login successful!")
            self.general_user_menu(username, password)
        else:
            print("\n Invalid username or password.")

    def create_account(self): #creates a new account for a general user
        username = input("Choose a username: ").strip()
        password = input("Choose a password: ").strip() 
        availability = 000000000000000000000 #default availability string (all unavailable)

        if not username or not password: #checks if the username and password are not empty
            print("Username and password cannot be empty.")
            return

        if self.username_exists(username): #checks if the username already exists
            print("Username already exists. Please choose another.")
            return

        with open(self.accounts_file, "a") as f:
            f.write(f"{username},{password},{availability}\n")
        print("Account created successfully!")

    def check_credentials(self, username, password): #checks if the username and password match an existing account
        try:
            with open(self.accounts_file, "r") as f:
                for line in f:
                    stored_user, stored_pass, stored_availability = line.strip().split(",", 2) #splits the line into username, password, and availability
                    if stored_user == username and stored_pass == password: #checks if the username and password match
                        return True
        except FileNotFoundError:
            pass
        return False

    def username_exists(self, username): #checks if the username already exists
        try:
            with open(self.accounts_file, "r") as f:
                for line in f:
                    stored_user, stored_pass, stored_availability = line.strip().split(",", 2) #splits the line into username, password, and availability
                    if stored_user == username: #checks if the username matches
                        return True
        except FileNotFoundError:
            pass
        return False
        
    def general_user_menu(self, username, password): #menu used by general users
        print("1. Open user profile")
        print("2. Open avalibility menu")
        print("3. Open shift schedule")
        print("4. Open calendar")
        choice = str(input("Input the number corresponding which window you wish to view")) #gets user input for menu choice
        match choice: 
            case '1': #opens the user profile
                while True:
                    print(f"Username {username}.")
                    print(f"Password {password}.")
                    sub_choice = str(input("Press 1 to exit.").strip())
                    match sub_choice:
                        case '1':
                            break
                self.general_user_menu(username, password)

            case '2': #opens the availability menu
                availability = Availability()
                while True:
                    print("1. View Availability")
                    print("2. Update Availability")
                    print("3. Back to User Menu")
                    sub_choice = str(input("Enter choice (1-3): ").strip())
                    match sub_choice:
                        case '1': #views the user's availability
                            accounts = availability.load_accounts()
                            if username in accounts:
                                availability.display_availability(accounts[username]['availability'])
                            else:
                                print("Username not found.")
                        case '2': #updates the user's availability
                            new_availability = availability.get_availability()
                            availability.update_availability(username, new_availability)
                        case '3': #goes back to the user menu
                            break
                        case _:
                            print("Bad input. Try again")
                self.general_user_menu(username, password)

            case '3': #opens the shift schedule
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

            case '4': #opens the calendar
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
        choice = str(input("Input the number corresponding which window you wish to view")) #gets user input for menu choice
        match choice:
            case '1': #opens the admin profile
                while True:
                    print(f"Username {username}.")
                    print(f"Password {password}.")
                    sub_choice = str(input("Press 1 to exit.").strip())
                    match sub_choice:
                        case '1':
                            break
                self.admin_menu(username, password)


            case '2': #opens the availability menu
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

            case '3': #opens the shift schedule
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

            case '4': #opens the calendar
                now = datetime.now()
                cal = Calendar(now.year, now.month)
                while True:
                    print("1. Add Event")
                    print("2. Remove Event")
                    print("3. Display Calendar")
                    print("4. Back")
                    cal_choice = input("Enter choice (1-4): ").strip()
                    match cal_choice:
                        case '1': #add event
                            try:
                                day = int(input("Enter day of the month: ").strip())
                                event = input("Enter event description: ").strip()
                                cal.add_event(day, event)
                            except Exception as e:
                                print(f"Error: {e}")
                        case '2': #remove event
                            try:
                                day = int(input("Enter day of the month: ").strip())
                                event = input("Enter event description to remove: ").strip()
                                cal.remove_event(day, event)
                            except Exception as e:
                                print(f"Error: {e}")
                        case '3': #display calendar
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
