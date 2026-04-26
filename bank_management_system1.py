# Bank Management System using OOP and JSON storage

import json
import os
import random
from faker import Faker
from datetime import datetime

# Represents a single bank account
class BankAccount:
    def __init__(self, acc_no, name, password, balance=0, transactions=None):
        self.__acc_no = acc_no
        self.__name = name
        self.__password = password
        self.__balance = balance
        self.__transactions = transactions if transactions else []
        
    def get_acc_no(self):
        return self.__acc_no

    def get_password(self):
        return self.__password

    def get_balance(self):
        return self.__balance

    def get_transactions(self):
        return self.__transactions
        
    # Add money and record transaction
    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Invalid deposit amount")
        self.__balance += amount
        self.__transactions.append(f"{datetime.now()} - Deposited {amount}")

    # Deduct money if sufficient balance
    def withdraw(self, amount):
        if amount <= 0 or amount > self.__balance:
            raise ValueError("Invalid withdrawal")
        self.__balance -= amount
        self.__transactions.append(f"{datetime.now()} - Withdrawn {amount}")

    # Convert object to dictionary for JSON storage
    def to_dict(self):
        return {
            "acc_no": self.__acc_no,
            "name": self.__name,
            "password": self.__password,
            "balance": self.__balance,
            "transactions": self.__transactions
        }

# Handles all banking operations and file storage
class Bank:
    file_name = r"C:\Users\ritesh nalawade\Desktop\BANK_FILE.json"
    admin_password = "analyst99"
    
     # Load data from JSON file
    def load_data(self):
        if not os.path.exists(self.file_name):
            return {}
        with open(self.file_name, "r") as file:
            return json.load(file)

    # Save data to JSON file
    def save_data(self, data):
        with open(self.file_name, "w") as file:
            json.dump(data, file, indent=4)

    def get_account(self, acc_no, data):
        return BankAccount(**data[acc_no])
        
    # Create account
    def create_account(self):
        data = self.load_data()

        acc_no = input("Enter account number: ")
        if acc_no in data:
            print("Account already exists")
            return

        name = input("Enter your name: ")
        password = input("Set password: ")
        balance = float(input("Enter initial balance: "))

        account = BankAccount(acc_no, name, password, balance)
        data[acc_no] = account.to_dict()

        self.save_data(data)
        print("Account created successfully!")

    # Authenticate user
    def login(self):
        data = self.load_data()

        acc_no = input("Enter account number: ")
        password = input("Enter password: ")

        if acc_no in data and data[acc_no]["password"] == password:
            return acc_no, data
        else:
            raise ValueError("Invalid credentials")

    def deposit(self):
        try:
            acc_no, data = self.login()
            amount = float(input("Enter amount: "))

            acc = self.get_account(acc_no, data)
            acc.deposit(amount)

            data[acc_no] = acc.to_dict()
            self.save_data(data)

            print("Deposit successful")
        except Exception as e:
            print("Error:", e)

    def withdraw(self):
        try:
            acc_no, data = self.login()
            amount = float(input("Enter amount: "))

            acc = self.get_account(acc_no, data)
            acc.withdraw(amount)

            data[acc_no] = acc.to_dict()
            self.save_data(data)

            print("Withdrawal successful")
        except Exception as e:
            print("Error:", e)

    def show_balance(self):
        try:
            acc_no, data = self.login()
            print("Balance:", data[acc_no]["balance"])
        except Exception as e:
            print("Error:", e)

    def transaction_history(self):
        try:
            acc_no, data = self.login()
            for t in data[acc_no]["transactions"]:
                print(t)
        except Exception as e:
            print("Error:", e)

    def mini_statement(self):
        try:
            acc_no, data = self.login()
            for t in data[acc_no]["transactions"][-5:]:
                print(t)
        except Exception as e:
            print("Error:", e)

    # Transfer money between two accounts
    def transfer_money(self):
        try:
            sender_acc, data = self.login()
            receiver_acc = input("Enter receiver account: ")

            if receiver_acc not in data:
                raise ValueError("Receiver not found")

            amount = float(input("Enter amount: "))

            sender = self.get_account(sender_acc, data)
            receiver = self.get_account(receiver_acc, data)

            sender.withdraw(amount)
            receiver.deposit(amount)

            time = str(datetime.now())
            sender.get_transactions().append(f"{time} - Sent {amount} to {receiver_acc}")
            receiver.get_transactions().append(f"{time} - Received {amount} from {sender_acc}")

            data[sender_acc] = sender.to_dict()
            data[receiver_acc] = receiver.to_dict()

            self.save_data(data)
            print("Transfer successful")

        except Exception as e:
            print("Error:", e)

    # Generate fake data for testing
    def generate_bulk_data(self, num_customers=1000, transactions_per_customer=10):
        fake = Faker()
        data = self.load_data()

        account_numbers = []

        for _ in range(num_customers):
            acc_no = str(random.randint(1000000000, 9999999999))
            if acc_no in data:
                continue

            acc = BankAccount(acc_no, fake.name(), "1234", 0, [])
            data[acc_no] = acc.to_dict()
            account_numbers.append(acc_no)

        for acc_no in account_numbers:
            acc = self.get_account(acc_no, data)

            for _ in range(transactions_per_customer):
                amount = round(random.uniform(100, 5000), 2)

                if random.choice([True, False]):
                    acc.deposit(amount)
                else:
                    if acc.get_balance() >= amount:
                        acc.withdraw(amount)

            data[acc_no] = acc.to_dict()

        self.save_data(data)
        print(f"Generated {len(account_numbers)} customers with transactions")
        
# menu driven program 
def main():
    bank = Bank()

    while True:
        print("\n--- BANK MENU ---")
        print("1. Create Account")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Balance")
        print("5. Mini Statement")
        print("6. Full History")
        print("7. Transfer")
        print("8. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            bank.create_account()
        elif choice == "2":
            bank.deposit()
        elif choice == "3":
            bank.withdraw()
        elif choice == "4":
            bank.show_balance()
        elif choice == "5":
            bank.mini_statement()
        elif choice == "6":
            bank.transaction_history()
        elif choice == "7":
            bank.transfer_money()
        elif choice == "8":
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    # to generate random data 
    #bank = Bank()
    #bank.generate_bulk_data(1000, 10)
    #comment main() when generating random data once done comment it and run main()
    main()