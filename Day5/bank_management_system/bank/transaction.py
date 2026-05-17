from abc import ABC, abstractmethod
from datetime import datetime
from .exceptions import InvalidAmountError, InsufficientBalanceError
import csv
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
CSV_FILE = os.path.join(DATA_DIR, "transactions.csv")


def ensure_data_folder():
    os.makedirs(DATA_DIR, exist_ok=True)


def log_transaction_to_csv(account_number, txn_type, amount, timestamp):
    ensure_data_folder()

    file_exists = os.path.isfile(CSV_FILE)

    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(["Account", "Type", "Amount", "Timestamp"])

        writer.writerow([account_number, txn_type, amount, timestamp])


def load_transactions_from_csv(account_number):
    """Reads CSV and returns list of dicts for a specific account."""
    if not os.path.exists(CSV_FILE):
        return []

    results = []
    with open(CSV_FILE, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["Account"] == account_number:
                results.append(row)
    return results


class Transaction(ABC):
    def __init__(self, amount, timestamp=None):
        self.amount = amount
        self.timestamp = timestamp or datetime.now()

    @abstractmethod
    def apply(self, account):
        pass

    def log(self, account, txn_type):
        log_transaction_to_csv(
            account_number=account.account_number,
            txn_type=txn_type,
            amount=self.amount,
            timestamp=self.timestamp,
        )

    def __str__(self):
        return f"{self.__class__.__name__}: {self.amount} at {self.timestamp}"


class Deposit(Transaction):
    def apply(self, account):
        if self.amount <= 0:
            raise InvalidAmountError()
        account._Account__balance += self.amount
        self.log(account, "DEPOSIT")


class Withdraw(Transaction):
    def apply(self, account):
        if self.amount <= 0:
            raise InvalidAmountError()
        if self.amount > account._Account__balance:
            raise InsufficientBalanceError()
        account._Account__balance -= self.amount
        self.log(account, "WITHDRAW")
