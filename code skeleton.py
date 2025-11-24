class Shift_schedule: #contains all the info on the shift schedule
    def empty(self):
        return



class User_profile: #contains the info for a user, including their name, ID, position, etc.
    def empty(self):
        return



class Calendar: #contains the info for the calendar
    def empty(self):
        return



def load_info(): #loads the info from the data files into the program
    return


def export_info(): #exports all of the data into the data files
    return

def is_admin(): #will check if the user ID is the admin ID (I believe we should hardcode this)
    return False


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


def open_calendar(): #the calendar is printed here
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


def edit_display_schedule(): #code for editing the schedule
    return


def admin_open_calendar(): #code for opening and editing the calendar
    display_calendar()
    edit_calendar()
    return

def display_calendar(): #code for displaying the calendar
    return

def edit_calendar(): #code for editing the calendar
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
