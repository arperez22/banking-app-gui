from tkinter import *
from PIL import Image, ImageTk, ImageFile

class Gui:

    def __init__(self, window) -> None:
        self.window: Tk = window

        # Notification Declaration
        self.notif: Label = None

        # Name Frame, Label, and Entry Declarations
        self.firstname_frame: Frame = Frame(self.window)
        self.firstname_label: Label = Label(self.firstname_frame, text='First Name', font='Helvetica 10 bold')
        self.firstname_input: Entry = Entry(self.firstname_frame)

        self.firstname_label.pack(side='left')
        self.firstname_input.pack(side='left', padx=65)

        self.lastname_frame: Frame = Frame(self.window)
        self.lastname_label: Label = Label(self.lastname_frame, text='Last Name', font='Helvetica 10 bold')
        self.lastname_input: Entry = Entry(self.lastname_frame)

        self.lastname_label.pack(side='left')
        self.lastname_input.pack(side='left', padx=66)

        # Account Frame, Label, and Entry Declarations
        self.account_frame: Frame = Frame(self.window)
        self.account_label: Label = Label(self.account_frame, text='Account Number', font='Helvetica 10 bold')
        self.account_input: Entry = Entry(self.account_frame)

        self.account_label.pack(side='left')
        self.account_input.pack(side='left', padx=28)

        # Password Frame, Label, and Entry Declarations
        self.password_frame: Frame = Frame(self.window)
        self.password_label: Label = Label(self.password_frame, text='Enter Password', font='Helvetica 10 bold')
        self.password_input: Entry = Entry(self.password_frame, show='\u2022')

        self.password_label.pack(side='left')
        self.password_input.pack(side='left', padx=35)

        # Front Page Variable Declarations
        self.img: ImageFile = ImageTk.PhotoImage(Image.open('images/bank.png').resize((300, 211)))

        self.welcome_frame: Frame = Frame(self.window)
        self.welcome_label: Label = Label(self.welcome_frame, text='Welcome to the Bank!', font='Helvetica 10 bold')
        self.welcome_label.pack(side='left', padx=10, pady=10)        

        self.start_frame: Frame = Frame(self.window)
        self.start_label: Label = Label(self.start_frame, text='Sign in or Register a New Account')
        self.start_label.pack(padx=10)

        self.bank_label: Label = Label(self.start_frame, image=self.img)
        self.bank_label.image = self.img
        self.bank_label.pack(pady=25)

        self.front_button_frame: Frame = Frame(self.window)
        self.button_sign_in: Button = Button(self.front_button_frame, text='SIGN IN')
        self.button_register: Button = Button(self.front_button_frame, text='REGISTER')
        self.button_sign_in.pack(side='left', padx=75)
        self.button_register.pack(side='right', padx=70)

        # Registration Page Variable Declarations
        self.register_frame: Frame = Frame(self.window)

        self.register_label: Label = Label(self.register_frame, text='Create a Bank Account', font='Helvetica 10 bold')
        self.register_label.pack(pady=10)

        self.register_buttons_frame: Frame = Frame(self.window)

        self.create_button: Button = Button(self.register_buttons_frame, text='CREATE ACCOUNT')
        self.back_button: Button = Button(self.register_buttons_frame, text='BACK')
        self.create_button.pack(side='right', padx=50, pady=20)
        self.back_button.pack(side='left', padx=50, pady=20)

        # Sign-in Page Variable Declarations
        self.sign_in_frame: Frame = Frame(self.window)

        self.login_frame: Frame = Frame(self.window)

        self.login_label: Label = Label(self.login_frame, text='Sign in with Name or Account Number', font='Helvetica 10 bold')
        self.login_answer: IntVar = IntVar()
        self.login_answer.set(0)

        self.radio_names: Radiobutton = Radiobutton(self.login_frame, text='First/Last Names', font='Helvetica 10',
                                                    variable=self.login_answer, value=1)
        self.radio_account: Radiobutton = Radiobutton(self.login_frame, text='Account Number', font='Helvetica 10',
                                                      variable=self.login_answer, value=2)
        
        self.login_label.pack(anchor='center', pady=10)
        self.radio_names.pack(side='left', padx=10, pady=10)
        self.radio_account.pack(side='left', padx=10, pady=10)

        self.sign_in_button: Button = Button(self.sign_in_frame, text='SIGN IN')
        self.to_home_button: Button = Button(self.sign_in_frame, text='BACK')

        self.sign_in_button.pack(side='right', padx=75, pady=30)
        self.to_home_button.pack(side='left', padx=75, pady=30)

        # Account View Variable Declarations
        self.welcome_back_frame: Frame = Frame(self.window)

        self.welcome_back_label: Label = Label(self.welcome_back_frame, font='Helvetica 10')
        self.account_info_label: Label = Label(self.welcome_back_frame, font='Helvetica 10')
        self.question_label: Label = Label(self.welcome_back_frame, text='What would you like to do today?', font='Helvetica 10')

        self.welcome_back_label.pack(pady=5)
        self.account_info_label.pack(pady=5)
        self.question_label.pack(pady=5)

        self.radio_frame: Frame = Frame(self.window)

        self.account_choice: StringVar = StringVar()
        self.account_choice.set('N/A')

        self.account_deposit: Radiobutton = Radiobutton(self.radio_frame, text='Deposit',
                                                        variable=self.account_choice, value='Deposit')

        self.account_withdrawal: Radiobutton = Radiobutton(self.radio_frame, text='Withdraw',
                                                           variable=self.account_choice, value='Withdrawal')

        self.account_deposit.pack(side='left')
        self.account_withdrawal.pack(side='right')

        self.amount_frame: Frame = Frame(self.window)

        self.amount_label: Label = Label(self.amount_frame, text='Amount', font='Helvetica 10 bold')
        self.amount_input: Entry = Entry(self.amount_frame)

        self.amount_label.pack(side='left')
        self.amount_input.pack(side='right')

        self.enter_button: Button = Button(self.window, text='ENTER')

        self.balance_frame: Frame = Frame(self.window)

        self.adjustment_label: Label = Label(self.balance_frame, font='Helvetica 10')
        self.balance_label: Label = Label(self.balance_frame, font='Helvetica 10')

        self.adjustment_label.pack()
        self.balance_label.pack()

        self.sign_out_button: Button = Button(self.window, text='SIGN OUT')