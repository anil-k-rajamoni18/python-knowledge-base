from bank.bank import Bank

bank = Bank("OpenAI Bank")


def menu():
    print("\n===== BANK MENU =====")
    print("1. Create Account")
    print("2. Deposit")
    print("3. Withdraw")
    print("4. View Balance")
    print("5. View Transaction History")
    print("6. Apply Interest to All Accounts")
    print("7. Exit")
    print("=====================")


def main():
    while True:
        menu()
        choice = input("Enter choice: ")

        if choice == "1":
            name = input("Enter owner name: ")
            acc_no = input("Enter account number: ")
            bal = float(input("Initial balance: "))
            bank.create_account(name, acc_no, bal)
            print("Account created successfully!")

        elif choice == "2":
            acc_no = input("Account number: ")
            amt = float(input("Deposit amount: "))
            acc = bank.get_account(acc_no)
            acc.deposit(amt)
            bank.save_accounts()
            print("Deposit successful!")

        elif choice == "3":
            acc_no = input("Account number: ")
            amt = float(input("Withdraw amount: "))
            acc = bank.get_account(acc_no)
            acc.withdraw(amt)
            bank.save_accounts()
            print("Withdrawal successful!")

        elif choice == "4":
            acc_no = input("Account number: ")
            acc = bank.get_account(acc_no)
            print("Balance:", acc.view_balance())

        elif choice == "5":
            acc_no = input("Account number: ")
            acc = bank.get_account(acc_no)
            print("\n".join(acc.view_transactions()))

        elif choice == "6":
            bank.apply_interest()
            print("Interest applied to all accounts.")

        elif choice == "7":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
