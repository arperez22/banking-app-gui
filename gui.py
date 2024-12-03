from tkinter import *
import csv, random, account

existing_accounts = account.get_existing_accounts()

class Gui:
    NAME_FRAMES_EXIST = False
    ACCOUNT_FRAMES_EXIST = False

    def __init__(self, window):
        self.window = window

        self.front_page()


        # Create control loop architecture for this application
        # Starting window should be constructed using a function

    def front_page(self):
        self.clear_gui()

        self.welcome_frame = Frame(self.window)
        self.welcome_label = Label(self.welcome_frame, text='Welcome!', font='Helvetica 10 bold')

        self.welcome_label.pack(side='left', padx=10)
        self.welcome_frame.pack()

        self.start_frame = Frame(self.window)
        self.start_label = Label(self.start_frame, text='Sign in or Create a New Account')

        self.start_label.pack(side='left', padx=10)
        self.start_frame.pack()

        self.button_sign_in = Button(self.window, text='SIGN IN', command=self.sign_in)
        self.button_create = Button(self.window, text='REGISTER', command=self.register)

        self.button_sign_in.pack(side='left', padx=75)
        self.button_create.pack(side='right', padx=50)

        return

    def choose_sign_in_mode(self):
        self.login_frame = Frame(self.window)
        self.login_label = Label(self.login_frame, text='Sign in with Name or Account Number',
                                 font='Helvetica 10 bold')
        self.login_answer = IntVar()
        self.login_answer.set(0)

        self.radio_names = Radiobutton(self.login_frame, text='First/Last Names', variable=self.login_answer,
                                       value=1, command=self.create_name_entries)
        self.radio_account = Radiobutton(self.login_frame, text='Account Number', variable=self.login_answer,
                                       value=2, command=self.create_account_entry)

        self.login_label.pack(anchor='center', padx=0, pady=0)
        self.radio_names.pack(side='left', padx=10, pady=0)
        self.radio_account.pack(side='left', padx=10, pady=0)

        self.login_frame.pack()


    def sign_in(self):
        self.clear_gui()
        self.choose_sign_in_mode()

        # Notification
        self.notif = Label(self.window, font='Helvetica 10')
        self.notif.pack(anchor='center')

        # Buttons
        Button(self.window, text='SIGN IN', command=self.validate_sign_in).pack(padx=10, pady=0, side='right')
        Button(self.window, text='BACK', command=self.front_page).pack(padx=10, pady=0, side='left')

    def validate_sign_in(self):

        if self.login_answer.get() == 1:
            first_name = self.firstname_input.get().strip()
            last_name = self.lastname_input.get().strip()
            password = self.password_input.get().strip()

            # Check for empty inputs
            if not first_name or not last_name or not password:
                self.notif.config(fg='red', text='All fields are required')
                return

            with open('accounts.csv', 'r') as file:
                reader = csv.reader(file)
                next(reader) # Skip header

                for line_number, row in enumerate(reader):
                    if first_name == row[0] and last_name == row[1] and password == row[3]:
                        self.account_view_page(row[0], row[1], line_number + 1)

            self.notif.config(fg='red', text='Account does not exist')

        elif self.login_answer.get() == 2:
            account_number = self.account_input.get().strip()
            password = self.password_input.get().strip()

            # Check for empty inputs
            if not account_number or not password:
                self.notif.config(fg='red', text='All fields are required')
                return

            with open('accounts.csv', 'r') as file:
                reader = csv.reader(file)
                next(reader) # Skip reader

                for line_number, row in enumerate(reader):
                    if account_number == row[2] and password == row[3]:
                        self.account_view_page(row[0], row[1], line_number + 1)

            self.notif.config(fg='red', text='Account does not exist')

        return


    def account_view_page(self, first_name, last_name, line_number):
        self.clear_gui()
        Label(self.window, text=f'Welcome back, {first_name} {last_name}!', font='Helvetica 10').pack()

        current_account = account.create_account(line_number)



        #Label(self.window, text=f'balance = {current_account.get_balance():.2f}, name = {current_account.get_name()}').pack()



    def register(self):
        self.clear_gui()
        self.create_name_entries()

        # Notification
        self.notif = Label(self.window, font='Helvetica 10')
        self.notif.pack(anchor='center')

        # Buttons
        Button(self.window, text='CREATE ACCOUNT', command=self.validate_registration).pack(expand=True)
        Button(self.window, text='BACK', command=self.front_page).pack(expand=True)



    def validate_registration(self):
        first_name = self.firstname_input.get().strip()
        last_name = self.lastname_input.get().strip()
        password = self.password_input.get().strip()

        # Check for empty inputs
        if not first_name or not last_name or not password:
            self.notif.config(fg='red', text='All fields are required')
            return

        # Check CSV file to prevent duplicate accounts
        with open('accounts.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader) # Skip header

            for row in reader:
                if first_name == row[0] and last_name == row[1]:
                    self.notif.config(fg='red', text='*Account Already Exists')
                    return

        account_number = random.randint(10000000, 90000000)

        while account_number in existing_accounts:
            account_number = random.randint(10000000, 90000000)

        existing_accounts.add(account_number)

        self.notif.config(fg='black', text=f'Welcome, {first_name} {last_name}!\n '
                                           f'Your account number is {account_number}')

        with open('accounts.csv', 'a', newline='') as file:
            content = csv.writer(file, delimiter=',')

            content.writerow([first_name, last_name, str(account_number), password, '0.00'])


    def clear_gui(self):

        for widget in self.window.winfo_children():
            widget.destroy()

        self.NAME_FRAMES_EXIST = False
        self.ACCOUNT_FRAMES_EXIST = False

        return

    def create_name_frames(self):
        # Create first name frame
        self.firstname_frame = Frame(self.window)
        self.firstname_label = Label(self.firstname_frame, text='First Name', font='Helvetica 8 bold')
        self.firstname_input = Entry(self.firstname_frame)

        # Create last name frame
        self.lastname_frame = Frame(self.window)
        self.lastname_label = Label(self.lastname_frame, text='Last Name', font='Helvetica 8 bold')
        self.lastname_input = Entry(self.lastname_frame)

        self.NAME_FRAMES_EXIST = True

        return

    def create_name_entries(self):
        # Check if account frame currently exists
        if self.ACCOUNT_FRAMES_EXIST:
            self.destroy_account_frame()
            self.destroy_password_frame()
        # Check if name frame currently exists.  In case user clicks radio button multiple times in a row.
        if self.NAME_FRAMES_EXIST:
            return

        # Create name and password frames if they don't already exist
        self.create_name_frames()
        self.create_password_frame()

        # Pack first name frame

        self.firstname_label.pack(side='left')
        self.firstname_input.pack(side='left')
        self.firstname_frame.pack(anchor='w')

        # Pack last name frame
        self.lastname_label.pack(side='left')
        self.lastname_input.pack(side='left')
        self.lastname_frame.pack(anchor='w')

        self.create_password_entry()

        return

    def create_account_frame(self):
        # Create account frame
        self.account_frame = Frame(self.window)
        self.account_label = Label(self.account_frame, text='Account Number', font='Helvetica 8 bold')
        self.account_input = Entry(self.account_frame)

        self.ACCOUNT_FRAMES_EXIST = True

        return

    def create_account_entry(self):
        # Check if name frames currently exist
        if self.NAME_FRAMES_EXIST:
            self.destroy_name_frames()
            self.destroy_password_frame()
        # Check if account frame currently exists. In case user clicks radio button multiple times in a row.
        if self.ACCOUNT_FRAMES_EXIST:
            return

        # Create account and password frames if it doesn't already exist
        self.create_account_frame()
        self.create_password_frame()

        # Pack account frame
        self.account_label.pack(side='left')
        self.account_input.pack(side='left')
        self.account_frame.pack(anchor='w')

        self.create_password_entry()

        return

    def create_password_frame(self):
        # Password
        self.password_frame = Frame(self.window)
        self.password_label = Label(self.password_frame, text='Enter Password', font='Helvetica 8 bold')
        self.password_input = Entry(self.password_frame, show='\u2022')

        return

    def create_password_entry(self):
        # Pack password frame
        self.password_label.pack(side='left')
        self.password_input.pack(side='left')
        self.password_frame.pack(anchor='w')

        return

    def destroy_name_frames(self):
        # Destroy name and password frames
        self.firstname_frame.destroy()
        self.lastname_frame.destroy()
        #self.password_frame.destroy()

        self.NAME_FRAMES_EXIST = False

        return

    def destroy_account_frame(self):
        # Destroy account frame
        self.account_frame.destroy()

        self.ACCOUNT_FRAMES_EXIST = False

        return

    def destroy_password_frame(self):
        # Destroy password frame
        self.password_frame.destroy()

        return