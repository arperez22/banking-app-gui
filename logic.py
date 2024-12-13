from account import *
from random import randint
import csv

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


def search_existing_accounts(first_name, last_name, account_number, password) -> Account:
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


def save_account_info(first_name, last_name, password) -> str:
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