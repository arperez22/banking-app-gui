import logic

class Account:
    """
    A class used to represent a checking account for a banking application

    Attributes:
        line_number (int): The number of the line that the account information is stored on in a csv file
        first_name  (str): The first name of the account owner
        last_name   (str): The last name of the account owner
        balance   (float): The balance of the account
    """

    def __init__(self, line_number: int, first_name: str, last_name: str, account_number: int, balance: float = 0.00) -> None:
        """
        Initializes an account object

        :param line_number    (int): The number of the line that the account's information is stored on in a csv file
        :param first_name     (str): The first name of the account owner
        :param last_name      (str): The last name of the account owner
        :param account_number (int): The identification number of the account
        :param balance       (float): The balance of the account
        """

        self.__account_line_number = line_number
        self.__account_first_name = first_name
        self.__account_last_name = last_name
        self.__account_number = account_number
        self.__account_balance = balance

        self.set_balance(balance)

    def deposit(self, amount: float) -> bool:
        """
        Deposits amount into account.  If deposit is successful, the method returns True.
        Otherwise, it returns False.
        :param amount: The amount to be deposited
        :return: A boolean value indicating whether the deposit was successful or not
        """

        if amount <= 0:
            return False

        self.__account_balance += amount

        logic.adjust_balance(self)

        return True

    def withdraw(self, amount: float) -> bool:
        """
        Withdraws amount from account.  If withdrawal is successful, the method returns True.
        Otherwise, it returns False.
        :param amount: The amount to be withdrawn
        :return: A boolean value indicating whether the withdrawal was successful or not
        """

        if amount <= 0 or self.__account_balance < amount:
            return False

        self.__account_balance -= amount

        logic.adjust_balance(self)

        return True

    def get_balance(self) -> float:
        """
        Accesses the private variable, balance.
        :return: The account's balance
        """

        return self.__account_balance

    def get_first_name(self) -> str:
        """
        Accesses the private variable, first_name
        :return: The first name of the account owner
        """

        return self.__account_first_name

    def get_last_name(self) -> str:
        """
        Accesses the private variable, last_name.
        :return: The last name of the account owner
        """

        return self.__account_last_name

    def get_account_number(self) -> int:
        """
        Accesses the private variable, account_number
        :return: The identification number of the account
        """

        return self.__account_number

    def get_line_number(self) -> int:
        """
        Accesses the private variable, line_number.
        :return: The line number that the account information is located on
        """

        return self.__account_line_number

    def set_balance(self, value: float) -> None:
        """
        Sets the account's balance to the value provided.
        :param value: The amount that the account's balance will be set to
        """

        if value < 0:
            self.__account_balance = 0
            return

        self.__account_balance = value
        return

    def set_name(self, first_name: str ='', last_name: str ='') -> None:
        """
        Sets the first_name and last_name variables to the strings provided.  If empty strings are provided,
        the names will remain unchanged.
        :param first_name: The name that the current first_name will be changed to
        :param last_name: The name that the current last_name will be changed to
        """

        if first_name:
            self.__account_first_name = first_name

        if last_name:
            self.__account_last_name = last_name

        return

    def __str__(self) -> str:
        """
        Formats the account into a string
        :return: A string representation of the account object
        """
        return (f'Account name = {self.get_first_name() + '' + self.get_last_name()},'
                f' Account balance = {self.get_balance():.2f}')

