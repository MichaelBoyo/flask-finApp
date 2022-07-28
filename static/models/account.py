from datetime import datetime

from static import utils


class Account:
    uid = 0

    def __init__(self, email="", password=""):
        self.transaction_history = []
        Account.uid += 1
        self.account_number = Account.uid
        self._password = password
        self.email = email

    @property
    def balance(self) -> float:
        credit = sum([a["amount"] for a in self.transaction_history
                      if a["type"] == "Deposit" or a["type"] == "Transfer-in"])

        debits = sum([a["amount"] for a in self.transaction_history
                      if a["type"] == "Withdraw" or a["type"] == "Transfer-out"])
        return credit-debits

    @property
    def password(self):
        return utils.hash_password(self._password)

    def validatePassword(self, password, hashed_pwd=''):
        return utils.validate_password(password, hashed_pwd)

    @password.setter
    def password(self, password):
        self._password = password

    def gbq(self):
        return self._password

    def deposit(self, amount: int):
        if amount <= 0:
            raise ValueError("invalid amount")
        transaction = dict(amount=amount,
                           date=datetime.now().strftime(f"%Y-%m-%d {'time->'} %H:%M"), type="Deposit")
        self.transaction_history.append(transaction)

    def withdraw(self, amount: int):
        if amount > self.balance:
            raise ValueError("amount greater than balance")
        transaction = dict(amount=amount,
                           date=datetime.now().strftime(f"%Y-%m-%d {'time->'} %H:%M"), type="Withdraw")
        self.transaction_history.append(transaction)
