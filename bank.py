from account import *
from gui import *
from random import randint
import csv

class Bank(Gui):


    def __init__(self, window) -> None:
        super().__init__(window)
        self.user_account: Account = None
        self.front_page()


    def front_page(self) -> None:
        """
        Clears widgets then initializes and displays the welcome page of the banking app
        """

        self.clear_gui()
        self.user_account = None

        self.welcome_frame.pack()

        self.start_frame.pack()

        self.button_sign_in.config(command=self.sign_in)
        self.button_register.config(command=self.registration_page)

        self.front_button_frame.pack()

        return
    

    def sign_in(self) -> None:
        """
        Clears widgets then initializes and displays the sign-in page of the banking app
        """

        self.clear_gui()
        self.user_account = None

        self.login_answer.set(0)
        self.radio_names.config(command=self.create_sign_in_entries)
        self.radio_account.config(command=self.create_sign_in_entries)
        self.login_frame.pack()

        self.notif = Label(self.window, font='Helvetica 10')
        self.notif.pack(anchor='center')

        self.sign_in_button.config(command=self.validate_sign_in)
        self.to_home_button.config(command=self.front_page)

        self.sign_in_frame.pack()

        return
    

    def validate_sign_in(self) -> None:
        """
        Validates the sign-in information from the user.  If the information
        does not match any found in the csv file, an error is shown and the
        user is notified.
        """

        if self.login_answer.get() == 1:
            first_name: str = self.firstname_input.get().strip()
            last_name:  str = self.lastname_input.get().strip()
            password:   str = self.password_input.get().strip()

            # Check for empty inputs
            if not first_name or not last_name or not password:
                self.notif.config(fg='red', text='All fields are required')
                return
            
            self.user_account = search_existing_accounts(first_name=first_name, last_name=last_name,
                                                         account_number='', password=password)
            
            if self.user_account is None:
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
            
            self.user_account = search_existing_accounts(first_name='', last_name='',
                                                         account_number=account_number, password=password)
            
            if self.user_account is None:
                self.notif.config(fg='red', text='Account does not exist')
                return
            
            self.account_view_page()

        return
    

    def account_view_page(self) -> None:
        """
        Clears widgets and initializes and displays the account-view page
        """

        self.clear_gui()

        self.welcome_back_label.config(text=f'Welcome back, {self.user_account.get_first_name()} {self.user_account.get_last_name()}!')
        self.account_info_label.config(text=f'Account Number: {self.user_account.get_account_number()}')
        self.welcome_back_frame.pack()

        self.radio_frame.pack(pady=10)

        self.amount_frame.pack(pady=10)

        self.notif = Label(self.window, text='', font='Helvetica 10')
        self.notif.pack(anchor='center')

        self.enter_button.config(command=self.handle_cash_input)
        self.enter_button.pack()

        self.balance_label.config(text=f'Your current account balance is ${self.user_account.get_balance():.2f}')

        self.balance_frame.pack()

        self.sign_out_button.config(command=self.front_page)

        self.sign_out_button.pack(pady=15)

        return

    
    def handle_cash_input(self) -> None:
        """
        Validates the deposit/withdrawal information from the user.
        If the user enters any value that isn't a number or a negative
        number in the amount entry, an error is shown and the user is
        notified.
        """
                
        if self.account_choice.get() == 'N/A' and not self.amount_input.get():
            self.notif.config(fg='red', text='All fields are required')
            return

        amount = 0

        try:
            amount: float = float(self.amount_input.get())
            self.notif.config(text='')

            if amount <= 0:
                raise TypeError
            
        except ValueError:
            self.notif.config(fg='red', text='Please enter a valid number')
            self.adjustment_label.config(fg='red', text='')
            return
        
        except TypeError:
            self.notif.config(fg='red', text='Please enter a positive number')
            self.adjustment_label.config(fg='red', text='')
            return
        
        if self.account_choice.get() == 'Deposit':
            self.user_account.deposit(amount)
            self.adjustment_label.config(fg='black', text=f'You just deposited ${amount:.2f}')

        else:
                if not self.user_account.withdraw(amount):
                    self.adjustment_label.config(fg='red', text='Insufficient Funds')

                else:
                    self.adjustment_label.config(fg='black', text=f'You just withdrew ${amount:.2f}')

        self.balance_label.config(text=f'Your current account balance is ${self.user_account.get_balance():.2f}')

        return


    def registration_page(self) -> None:
        """
        Clears widgets and initializes and displays the registration
        page
        """

        self.clear_gui()
        self.user_account = None

        self.register_frame.pack()

        self.create_name_entries()

        # Notification
        self.notif: Label = Label(self.window, font='Helvetica 10')
        self.notif.pack(anchor='center')

        # Buttons
        self.create_button.config(command=self.validate_registration)
        self.back_button.config(command=self.front_page)
        self.register_buttons_frame.pack()

        return    


    def validate_registration(self) -> None:
        """
        Validates registration information from the user.  If the
        input names from the user are already in the csv file, an
        error will occur and the user will be notified.
        """

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
        Forgets all widgets that exist on the window.
        """

        for widget in self.window.winfo_children():
            widget.pack_forget()


        return


    def create_sign_in_entries(self) -> None:
        self.password_frame.pack_forget()
        self.sign_in_frame.pack_forget()

        if self.login_answer.get() == 1:

            self.account_frame.pack_forget()
            self.create_name_entries()

        elif self.login_answer.get() == 2:

            self.firstname_frame.pack_forget()
            self.lastname_frame.pack_forget()
            self.create_account_entry()

        self.sign_in_frame.pack()

        return
    

    def create_name_entries(self) -> None:
        """
        Packs the name and password frames after creating them if they don't
        already exist.  Also destroys the account frames if they exist.
        """

        # Pack first name frame
        self.firstname_input.delete(0, END)
        self.firstname_frame.pack(anchor='w')

        # Pack last name frame
        self.lastname_input.delete(0, END)
        self.lastname_frame.pack(anchor='w')

        self.create_password_entry()

        return


    def create_account_entry(self) -> None:
        """
        Packs the account and password frames after creating them if they don't
        already exist.  Also destroys the name frames if they exist.
        """

        # Pack account frame
        self.account_input.delete(0, END)
        self.account_frame.pack(anchor='w')

        self.create_password_entry()

        return


    def create_password_entry(self) -> None:
        """
        Packs the password frame
        """

        # Pack password frame
        self.password_input.delete(0, END)
        self.password_frame.pack(anchor='w')

        return


def get_existing_account_numbers() -> set[int]:
    """
    Create a set with the existing account numbers
    :return: A set of 8-digit integers containing all the account numbers listed in the accounts database
    """

    account_numbers = set()

    with open('accounts.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            account_numbers.add(int(row[2]))

    return account_numbers


def create_account(line_number: int) -> Account:
    """
    Creates a new account object from the accounts database
    :param line_number: Specifies the line on which the account information is located in the accounts database
    :return: An account object with the account information found on the line specified by line number
    """

    with open('accounts.csv', 'r') as file:
        reader = csv.reader(file)

        for index, row in enumerate(reader):
            if index == line_number:
                first_name = row[0]
                last_name = row[1]
                account_number = int(row[2])
                balance = float(row[4])
                break

    user_account = Account(line_number, first_name, last_name, account_number, balance)

    return user_account


def adjust_balance(user_account: Account) -> None:
    """
    Changes the balance shown in the accounts database for the provided account
    :param user_account: The account for which the balance will be adjusted
    """

    with open('accounts.csv', 'r') as file:
        reader = csv.reader(file)
        data = list(reader)

    data[user_account.get_line_number()][4] = user_account.get_balance()

    with open('accounts.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)


def search_existing_accounts(first_name: str, last_name: str, account_number: str, password: str) -> Account:
    """
    Searches csv file for user login information.  Users can either sign in with
    first name, last name, and password or account number and password.  Both cases
    are handled by this function.  This function also searches for duplicate names when users
    register a new account.
    :param first_name: The first name associated with the target account
    :param last_name: The last name associated with the target account
    :param account_number: The account number associated with the target account
    :param password: The password associated with the target account
    :return: If a matching account is found, an account object is created and returned.
             If not, None is returned.
    """

    if not account_number and not password:
        with open('accounts.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader) # Skip header

            for line_number, row in enumerate(reader):
                if first_name == row[0] and last_name == row[1]:
                    return create_account(line_number + 1)

    elif not first_name and not last_name:
        with open('accounts.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader) # Skip header

            for line_number, row in enumerate(reader):
                if account_number == row[2] and password == row[3]:
                    return create_account(line_number + 1)

    elif not account_number:
        with open('accounts.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader) # Skip header

            for line_number, row in enumerate(reader):
                if first_name == row[0] and last_name == row[1] and password == row[3]:
                    return create_account(line_number + 1)

    else:
        return None


def save_account_info(first_name: str, last_name: str, password: str) -> str:
    """
    Writes new account information to the csv file.  Generates a unique 8-digit
    account number that can be used to identify the account.
    :param first_name:  The first name that will be associated with the new account
    :param last_name: The last name that will be associated with the new account
    :param password: The password that will be associated with the new account
    :return: A unique 8-digit account number that can be used to sign in to the new account
    """

    existing_account_numbers: set[int] = get_existing_account_numbers()

    account_number= randint(10000000, 99999999)

    while account_number in existing_account_numbers:
        account_number = randint(10000000, 99999999)

    account_number = str(account_number)

    with open('accounts.csv', 'a', newline='') as file:
        content = csv.writer(file)

        content.writerow([first_name, last_name, account_number, password, '0.00'])

    return account_number