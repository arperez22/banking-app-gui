import csv

class Account:

    def __init__(self, line_number, first_name, last_name, balance = 0.00):
        self.__account_line_number = line_number
        self.__account_first_name = first_name
        self.__account_last_name = last_name
        self.__account_balance = balance

        self.set_balance(balance)

    def deposit(self, amount):
        if amount <= 0:
            return False

        self.__account_balance += amount

        adjust_balance(self.__account_balance, self.__account_line_number)

        return True

    def withdraw(self, amount):
        if amount <= 0 or self.__account_balance < amount:
            return False

        self.__account_balance -= amount

        adjust_balance(self.__account_balance, self.__account_line_number)

        return True

    def get_balance(self):
        return self.__account_balance

    def get_first_name(self):
        return self.__account_first_name

    def get_last_name(self):
        return self.__account_last_name

    def get_line_number(self):
        return self.__account_line_number

    def set_balance(self, value):
        if value < 0:
            self.__account_balance = 0
            return

        self.__account_balance = value
        return

    def set_name(self, first_name='', last_name=''):
        if first_name:
            self.__account_first_name = first_name

        if last_name:
            self.__account_last_name = last_name

        return

    def __str__(self):
        return (f'Account name = {self.get_first_name() + '' + self.get_last_name()},'
                f' Account balance = {self.get_balance():.2f}')

def get_existing_accounts():
    account_numbers = set()

    with open('accounts.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            account_numbers.add(int(row[2]))

    return account_numbers

def create_account(line_number):
    with open('accounts.csv', 'r') as file:
        reader = csv.reader(file)

        for index, row in enumerate(reader):
            if index == line_number:
                first_name = row[0]
                last_name = row[1]
                balance = float(row[4])
                break

    user_account = Account(line_number, first_name, last_name, balance)

    return user_account


def adjust_balance(value, user_account):
    with open('accounts.csv', 'r') as file:
        reader = csv.reader(file)
        data = list(reader)

    data[user_account.get_line_number()][4] = user_account.get_balance() + value

    with open('accounts.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)


