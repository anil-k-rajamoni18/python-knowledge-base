import json
import os
from .account import Account

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
JSON_FILE = os.path.join(DATA_DIR, "accounts.json")


class Bank:
    interest_rate = 0.05

    def __init__(self, name):
        self.name = name
        self.accounts = {}

        os.makedirs(DATA_DIR, exist_ok=True)
        self.load_accounts()

    def save_accounts(self):
        data = {acc_no: acc.to_dict() for acc_no, acc in self.accounts.items()}

        with open(JSON_FILE, "w") as f:
            json.dump(data, f, indent=4)

    def load_accounts(self):
        if not os.path.exists(JSON_FILE):
            return

        with open(JSON_FILE, "r") as f:
            accounts = json.load(f)

        for acc_no, data in accounts.items():
            acc = Account(
                owner=data["owner"],
                account_number=data["account_number"],
                initial_balance=data["balance"],
            )
            self.accounts[acc_no] = acc

    def create_account(self, owner, account_number, initial_balance=0):
        if account_number in self.accounts:
            raise ValueError("Account number already exists")

        acc = Account(owner, account_number, initial_balance)
        self.accounts[account_number] = acc
        self.save_accounts()
        return acc

    def get_account(self, account_number):
        if account_number not in self.accounts:
            raise ValueError("Account not found")

        return self.accounts[account_number]

    def apply_interest(self):
        for acc in self.accounts.values():
            interest = acc.view_balance() * Bank.interest_rate
            acc.deposit(interest)
        self.save_accounts()

    def __str__(self):
        return f"Bank({self.name}, Accounts={len(self.accounts)})"
