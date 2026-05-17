from .transaction import Deposit, Withdraw, load_transactions_from_csv
from datetime import datetime


class Account:
    def __init__(self, owner, account_number, initial_balance=0):
        self.owner = owner
        self.account_number = account_number
        self.__balance = initial_balance
        self.transactions = []

        self.load_transaction_history()

    def load_transaction_history(self):
        rows = load_transactions_from_csv(self.account_number)

        for r in rows:
            amount = float(r["Amount"])
            timestamp = datetime.fromisoformat(r["Timestamp"])

            if r["Type"] == "DEPOSIT":
                txn = Deposit(amount, timestamp)
            else:
                txn = Withdraw(amount, timestamp)

            self.transactions.append(txn)

    def deposit(self, amount):
        txn = Deposit(amount)
        txn.apply(self)
        self.transactions.append(txn)

    def withdraw(self, amount):
        txn = Withdraw(amount)
        txn.apply(self)
        self.transactions.append(txn)

    def view_balance(self):
        return self.__balance

    def view_transactions(self):
        return [str(t) for t in self.transactions]

    def to_dict(self):
        return {
            "owner": self.owner,
            "account_number": self.account_number,
            "balance": self.__balance,
        }

    def __str__(self):
        return f"Account({self.owner}, #{self.account_number}, Balance={self.__balance})"
