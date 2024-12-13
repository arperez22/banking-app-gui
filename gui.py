from tkinter import *
from logic import *
from PIL import ImageTk, Image

user_account: Account = None

class Gui:
    NAME_FRAMES_EXIST: bool = False
    ACCOUNT_FRAMES_EXIST: bool = False

    def __init__(self, window) -> None:
        self.window= window
        self.sign_in_frame = None
        self.create_button = Button()

        self.front_page()


    def front_page(self) -> None:
        """
        Clears widgets then initializes and displays the welcome page of the banking app
        """

        self.clear_gui()

        global user_account
        user_account = None

        img = Image.open('images/bank.png')
        img = img.resize((300, 211))
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
        self.button_register:  Button = Button(self.window, text='REGISTER', command=self.registration_page)

        self.button_sign_in.pack(side='left', padx=75)
        self.button_register.pack(side='right', padx=70)

        return


    def choose_sign_in_mode(self) -> None:
        """
        Handles the sign-in choice from the user by displaying radio buttons with
        two sign-in options.  If the First/Last Names option is chosen, the first name,
        last name, and password entries are displayed.  If the Account Number option
        is chosen, the account number and password entries are displayed.
        """

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
        """
        Clears widgets then initializes and displays the sign-in page of the banking app
        """

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
        """
        Validates the sign-in information from the user.  If the information
        does not match any found in the csv file, an error is shown and the
        user is notified.
        """

        global user_account

        if self.login_answer.get() == 1:
            first_name: str = self.firstname_input.get().strip()
            last_name:  str = self.lastname_input.get().strip()
            password:   str = self.password_input.get().strip()

            # Check for empty inputs
            if not first_name or not last_name or not password:
                self.notif.config(fg='red', text='All fields are required')
                return

            user_account = search_existing_accounts(first_name=first_name, last_name=last_name,
                                                    account_number='', password=password)

            if not user_account:
                self.notif.config(fg='red', text='Account does not exist')
                return

            self.account_view_page()

        elif self.login_answer.get() == 2:
            account_number: str = self.account_input.get().strip()
            password:       str = self.password_input.get().strip()

            # Check for empty inputs
            if not account_number or not password:
                self.notif.config(fg='red', text='All fields are required')
                return

            user_account = search_existing_accounts(first_name='', last_name='',
                                                    account_number=account_number, password=password)

            if not user_account:
                self.notif.config(fg='red', text='Account does not exist')
                return

            self.account_view_page()

        return


    def account_view_page(self) -> None:
        """
        Clears widgets and initializes and displays the account-view page
        """

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

        Button(self.window, text='ENTER', command=self.handle_cash_input).pack()

        self.balance_frame: Frame = Frame(self.window)

        self.adjustment_label: Label = Label(self.balance_frame, font='Helvetica 10')

        self.adjustment_label.pack()

        self.balance_label: Label = Label(self.balance_frame, text=f'Your current account balance is ${user_account.get_balance():.2f}',
              font='Helvetica 10')

        self.balance_label.pack()

        self.balance_frame.pack()

        Button(self.window, text='SIGN OUT', command=self.front_page).pack(pady=15)

        return


    def handle_cash_input(self) -> None:
        """
        Validates the deposit/withdrawal information from the user.
        If the user enters any value that isn't a number or a negative
        number in the amount entry, an error is shown and the user is
        notified.
        """

        amount = 0
        global user_account

        try:
            amount: float = float(self.amount_input.get())
            self.flag.config(text='')

            if amount <= 0:
                raise TypeError

        except ValueError:
            self.flag.config(fg='red', text='Please enter a valid number')
            self.adjustment_label.config(fg='red', text='')
            return

        except TypeError:
            self.flag.config(fg='red', text='Please enter a positive number')
            self.adjustment_label.config(fg='red', text='')
            return

        if self.account_choice.get() == 'N/A' or not self.amount_input.get():
            self.flag.config(fg='red', text='All fields are required')
            return

        if self.account_choice.get() == 'Deposit':
            user_account.deposit(amount)
            self.adjustment_label.config(fg='black', text=f'You just deposited ${amount:.2f}')

        else:
            if not user_account.withdraw(amount):
                self.adjustment_label.config(fg='red',text='Insufficient Funds')

            else:
                self.adjustment_label.config(fg='black', text=f'You just withdrew ${amount:.2f}')

        self.balance_label.config(text=f'Your current account balance is ${user_account.get_balance():.2f}')

        return


    def registration_page(self) -> None:
        """
        Clears widgets and initializes and displays the registration
        page
        """

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
        """
        Validates registration information from the user.  If the
        input names from the user are already in the csv file, an
        error will occur and the user will be notified.
        """

        global user_account

        first_name: str = self.firstname_input.get().strip()
        last_name:  str = self.lastname_input.get().strip()
        password:   str = self.password_input.get().strip()

        # Check for empty inputs
        if not first_name or not last_name or not password:
            self.notif.config(fg='red', text='All fields are required')
            return

        user_account = search_existing_accounts(first_name=first_name, last_name=last_name,
                                                account_number='', password='')

        if user_account is not None:
            self.notif.config(fg='red', text='Account Already Exists')
            return

        account_number = save_account_info(first_name, last_name, password)

        self.notif.config(fg='black', text=f'Welcome, {first_name} {last_name}!\n '
                                           f'Your account number is {account_number}')

        user_account = None

        return


    def clear_gui(self) -> None:
        """
        Destroys all widgets that exist on the window.  Sets
        NAME_FRAMES_EXIST and ACCOUNT_FRAMES_EXIST class
        variables to False.
        """

        for widget in self.window.winfo_children():
            widget.destroy()

        self.NAME_FRAMES_EXIST = False
        self.ACCOUNT_FRAMES_EXIST = False

        return


    def create_name_frames(self) -> None:
        """
        Creates frames for first name input and last name
        input.  These frames are shown on the sign-in page
        and registration page.  After the frames are
        created, NAME_FRAMES_EXIST is set to True.
        """

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
        """
        Packs the name and password frames after creating them if they don't
        already exist.  Also destroys the account frames if they exist.
        """

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
        """
        Creates frames for the account number input.
        These frames are shown on the sign-in page
        and registration page.  After the frames are
        created, ACCOUNT_FRAMES_EXIST is set to True.
        """

        # Create account frame
        self.account_frame: Frame = Frame(self.window)
        self.account_label: Label = Label(self.account_frame, text='Account Number', font='Helvetica 10 bold')
        self.account_input: Entry = Entry(self.account_frame)

        self.ACCOUNT_FRAMES_EXIST = True

        return


    def create_account_entry(self) -> None:
        """
        Packs the account and password frames after creating them if they don't
        already exist.  Also destroys the name frames if they exist.
        """

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
        """
        Creates frame for the password input.
        This frame is shown on the sign-in page
        and registration page.
        """

        # Password
        self.password_frame: Frame = Frame(self.window)
        self.password_label: Label = Label(self.password_frame, text='Enter Password', font='Helvetica 10 bold')
        self.password_input: Entry = Entry(self.password_frame, show='\u2022')

        return


    def create_password_entry(self) -> None:
        """
        Packs the password frame
        """

        # Pack password frame
        self.password_label.pack(side='left')
        self.password_input.pack(side='left', padx=35)
        self.password_frame.pack(anchor='w')

        if self.create_button:
            self.sign_in_frame.pack()

        return


    def destroy_name_frames(self) -> None:
        """
        Destroys the names frames if they exist.
        Sets NAME_FRAMES_EXIST to False.
        """

        # Destroy name and password frames
        self.firstname_frame.destroy()
        self.lastname_frame.destroy()

        self.NAME_FRAMES_EXIST = False

        return


    def destroy_account_frame(self) -> None:
        """
        Destroys the account frame if it exists.
        Sets ACCOUNT_FRAMES_EXIST to False.
        """

        # Destroy account frame
        self.account_frame.destroy()

        self.ACCOUNT_FRAMES_EXIST = False

        return


    def destroy_password_frame(self) -> None:
        """
        Destroys the password frame if it exists
        """

        # Destroy password frame
        self.password_frame.destroy()

        return