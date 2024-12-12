from tkinter import *
from account import *
from PIL import ImageTk, Image
import csv, random


existing_accounts: set[int] = get_existing_accounts()

class Gui:
    NAME_FRAMES_EXIST: bool = False
    ACCOUNT_FRAMES_EXIST: bool = False

    def __init__(self, window) -> None:
        self.window: Misc = window
        self.sign_in_frame = None
        self.create_button = Button()

        self.front_page()


    def front_page(self) -> None:
        self.clear_gui()

        img = Image.open('images/bank.png')
        img = img.resize((300, 211), Image.LANCZOS)
        img = ImageTk.PhotoImage(img)

        self.welcome_frame: Frame = Frame(self.window)
        self.welcome_label: Label = Label(self.welcome_frame, text='Welcome to the Bank!', font='Helvetica 10 bold')

        self.welcome_label.pack(side='left', padx=10, pady=10)
        self.welcome_frame.pack()

        self.start_frame: Frame = Frame(self.window)
        self.start_label: Label = Label(self.start_frame, text='Sign in or Register a New Account')

        self.start_label.pack(padx=10)


        self.bank_label: Label = Label(self.start_frame, image=img)
        self.bank_label.image = img
        self.bank_label.pack(pady=10)
        self.start_frame.pack()

        self.button_sign_in: Button = Button(self.window, text='SIGN IN', command=self.sign_in)
        self.button_register:  Button = Button(self.window, text='REGISTER', command=self.register)

        self.button_sign_in.pack(side='left', padx=75)
        self.button_register.pack(side='right', padx=70)

        return

    def choose_sign_in_mode(self) -> None:
        self.login_frame: Frame = Frame(self.window)
        self.login_label: Label = Label(self.login_frame, text='Sign in with Name or Account Number',
                                 font='Helvetica 10 bold')
        self.login_answer: IntVar = IntVar()
        self.login_answer.set(0)

        self.radio_names:   Radiobutton = Radiobutton(self.login_frame, text='First/Last Names',
                                                      font='Helvetica 10',variable=self.login_answer, value=1,
                                                      command=self.create_name_entries)

        self.radio_account: Radiobutton = Radiobutton(self.login_frame, text='Account Number',font='Helvetica 10',
                                                      variable=self.login_answer, value=2,
                                                      command=self.create_account_entry)

        self.login_label.pack(anchor='center', padx=0, pady=10)
        self.radio_names.pack(side='left', padx=10, pady=10)
        self.radio_account.pack(side='left', padx=10, pady=10)

        self.login_frame.pack()

        return


    def sign_in(self) -> None:
        self.clear_gui()
        self.choose_sign_in_mode()

        # Notification
        self.notif: Label = Label(self.window, font='Helvetica 10')
        self.notif.pack(anchor='center')

        # Buttons
        self.sign_in_frame = Frame(self.window)

        self.sign_in_button = Button(self.sign_in_frame, text='SIGN IN', command=self.validate_sign_in)
        self.to_home_button = Button(self.sign_in_frame, text='BACK', command=self.front_page)

        self.sign_in_button.pack(padx=75, pady=30, side='right')
        self.to_home_button.pack(padx=75, pady=30, side='left')
        self.sign_in_frame.pack()

    def validate_sign_in(self) -> None:

        if self.login_answer.get() == 1:
            first_name: str = self.firstname_input.get().strip()
            last_name:  str = self.lastname_input.get().strip()
            password:   str = self.password_input.get().strip()

            # Check for empty inputs
            if not first_name or not last_name or not password:
                self.notif.config(fg='red', text='All fields are required')
                return

            with open('accounts.csv', 'r') as file:
                reader = csv.reader(file)
                next(reader) # Skip header

                for line_number, row in enumerate(reader):
                    if first_name == row[0] and last_name == row[1] and password == row[3]:
                        user_account: Account = create_account(line_number + 1)
                        self.account_view_page(user_account)

            self.notif.config(fg='red', text='Account does not exist')

        elif self.login_answer.get() == 2:
            account_number: str = self.account_input.get().strip()
            password:       str = self.password_input.get().strip()

            # Check for empty inputs
            if not account_number or not password:
                self.notif.config(fg='red', text='All fields are required')
                return

            with open('accounts.csv', 'r') as file:
                reader = csv.reader(file)
                next(reader) # Skip reader

                for line_number, row in enumerate(reader):
                    if account_number == row[2] and password == row[3]:
                        user_account: Account = create_account(line_number + 1)
                        self.account_view_page(user_account)

            self.notif.config(fg='red', text='Account does not exist')

        return


    def account_view_page(self, user_account: Account) -> None:
        self.clear_gui()

        Label(self.window, text=f'Welcome back, {user_account.get_first_name()} {user_account.get_last_name()}!',
              font='Helvetica 10').pack(pady=5)

        Label(self.window, text=f'Account Number: {user_account.get_account_number()}',
              font='Helvetica 10').pack(pady=5)

        Label(self.window, text='What would you like to do today?', font='Helvetica 10').pack(pady=5)


        self.radio_frame: Frame = Frame(self.window)

        self.account_choice: StringVar = StringVar()
        self.account_choice.set('N/A')

        self.account_deposit: Radiobutton = Radiobutton(self.radio_frame, text='Deposit',
                                                        variable=self.account_choice, value='Deposit')

        self.account_withdrawal: Radiobutton = Radiobutton(self.radio_frame, text='Withdraw',
                                                           variable=self.account_choice, value='Withdrawal')

        self.account_deposit.pack(side='left')
        self.account_withdrawal.pack(side='right')

        self.radio_frame.pack(pady=10)

        self.amount_frame: Frame = Frame(self.window)

        self.amount_label: Label = Label(self.amount_frame, text='Amount', font='Helvetica 10 bold')
        self.amount_input: Entry = Entry(self.amount_frame)

        self.amount_label.pack(side='left')
        self.amount_input.pack(side='right')

        self.amount_frame.pack(pady=10)

        self.flag: Label = Label(self.window, text='', font='Helvetica 10')

        self.flag.pack(anchor='center')

        Button(self.window, text='ENTER', command=lambda: self.handle_cash_input(user_account)).pack()

        self.balance_frame: Frame = Frame(self.window)

        self.adjustment_label: Label = Label(self.balance_frame, font='Helvetica 10')

        self.adjustment_label.pack()

        self.balance_label: Label = Label(self.balance_frame, text=f'Your current account balance is ${user_account.get_balance():.2f}',
              font='Helvetica 10')

        self.balance_label.pack()

        self.balance_frame.pack()

        Button(self.window, text='SIGN OUT', command=self.front_page).pack(pady=15)

        return


    def handle_cash_input(self, user_account: Account) -> None:
        amount = 0

        try:
            amount: float = float(self.amount_input.get())
            self.flag.config(text='')

            if amount <= 0:
                raise TypeError

        except ValueError:
            self.flag.config(fg='red', text='Please enter a valid number')

        except TypeError:
            self.flag.config(fg='red', text='Please enter a positive number')

        if self.account_choice.get() == 'N/A' or not self.amount_input.get():
            self.flag.config(fg='red', text='All fields are required')
            return

        if self.account_choice.get() == 'Deposit':
            user_account.deposit(amount)
            self.adjustment_label.config(fg='black', text=f'You just deposited ${amount:.2f}')

        else:
            if not user_account.withdraw(amount):
                self.adjustment_label.config(fg='red',text=f'Insufficient Funds')

            else:
                self.adjustment_label.config(fg='black', text=f'You just withdrew ${amount:.2f}')

        self.balance_label.config(text=f'Your current account balance is ${user_account.get_balance():.2f}')

        return


    def register(self) -> None:
        self.clear_gui()
        self.create_button = None

        self.register_label = Label(self.window, text='Create a Bank account', font='Helvetica 10 bold')
        self.register_label.pack(pady=10)

        self.create_name_entries()

        # Notification
        self.notif: Label = Label(self.window, font='Helvetica 10')
        self.notif.pack(anchor='center')

        # Buttons
        self.register_frame = Frame(self.window)

        self.create_button = Button(self.register_frame, text='CREATE ACCOUNT', command=self.validate_registration)
        self.create_button.pack(side='right', padx=50, pady=20)
        Button(self.register_frame, text='BACK', command=self.front_page).pack(side='left', padx=50, pady=20)

        self.register_frame.pack()

        return


    def validate_registration(self) -> None:
        first_name: str = self.firstname_input.get().strip()
        last_name:  str = self.lastname_input.get().strip()
        password:   str = self.password_input.get().strip()

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

        account_number: int = random.randint(10000000, 90000000)

        while account_number in existing_accounts:
            account_number = random.randint(10000000, 90000000)

        existing_accounts.add(account_number)

        self.notif.config(fg='black', text=f'Welcome, {first_name} {last_name}!\n '
                                           f'Your account number is {account_number}')

        with open('accounts.csv', 'a', newline='') as file:
            content = csv.writer(file, delimiter=',')

            content.writerow([first_name, last_name, str(account_number), password, '0.00'])

        return


    def clear_gui(self) -> None:

        for widget in self.window.winfo_children():
            widget.destroy()

        self.NAME_FRAMES_EXIST = False
        self.ACCOUNT_FRAMES_EXIST = False

        return

    def create_name_frames(self) -> None:
        # Create first name frame
        self.firstname_frame: Frame = Frame(self.window)
        self.firstname_label: Label = Label(self.firstname_frame, text='First Name', font='Helvetica 10 bold')
        self.firstname_input: Entry = Entry(self.firstname_frame)

        # Create last name frame
        self.lastname_frame: Frame = Frame(self.window)
        self.lastname_label: Label = Label(self.lastname_frame, text='Last Name', font='Helvetica 10 bold')
        self.lastname_input: Entry = Entry(self.lastname_frame)

        self.NAME_FRAMES_EXIST = True

        return

    def create_name_entries(self) -> None:
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

        if self.sign_in_frame:
            self.sign_in_frame.forget()

        # Pack first name frame
        self.firstname_label.pack(side='left')
        self.firstname_input.pack(side='left', padx=65)
        self.firstname_frame.pack(anchor='w')

        # Pack last name frame
        self.lastname_label.pack(side='left')
        self.lastname_input.pack(side='left', padx=66)
        self.lastname_frame.pack(anchor='w')

        self.create_password_entry()

        return

    def create_account_frame(self) -> None:
        # Create account frame
        self.account_frame: Frame = Frame(self.window)
        self.account_label: Label = Label(self.account_frame, text='Account Number', font='Helvetica 10 bold')
        self.account_input: Entry = Entry(self.account_frame)

        self.ACCOUNT_FRAMES_EXIST = True

        return

    def create_account_entry(self) -> None:
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

        self.sign_in_frame.forget()

        # Pack account frame
        self.account_label.pack(side='left')
        self.account_input.pack(side='left', padx=28)
        self.account_frame.pack(anchor='w')

        self.create_password_entry()

        return

    def create_password_frame(self) -> None:
        # Password
        self.password_frame: Frame = Frame(self.window)
        self.password_label: Label = Label(self.password_frame, text='Enter Password', font='Helvetica 10 bold')
        self.password_input: Entry = Entry(self.password_frame, show='\u2022')

        return

    def create_password_entry(self) -> None:
        # Pack password frame
        self.password_label.pack(side='left')
        self.password_input.pack(side='left', padx=35)
        self.password_frame.pack(anchor='w')

        if self.create_button:
            self.sign_in_frame.pack()

        return

    def destroy_name_frames(self) -> None:
        # Destroy name and password frames
        self.firstname_frame.destroy()
        self.lastname_frame.destroy()

        self.NAME_FRAMES_EXIST = False

        return

    def destroy_account_frame(self) -> None:
        # Destroy account frame
        self.account_frame.destroy()

        self.ACCOUNT_FRAMES_EXIST = False

        return

    def destroy_password_frame(self) -> None:
        # Destroy password frame
        self.password_frame.destroy()

        return