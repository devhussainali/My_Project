import json
import os
import uuid
from datetime import datetime
import matplotlib.pyplot as plt

# Global expense list
expenses = []
DATA_FILE = 'expenses.json'

# ========== Utility Functions ==========

def load_expenses():
    global expenses
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            expenses = json.load(f)

        # Ensure all old entries have a string ID
        for i, exp in enumerate(expenses, start=1):
            if 'id' not in exp:
                exp['id'] = int(i)
        save_expenses()


def save_expenses():
    with open(DATA_FILE, 'w') as f:
        json.dump(expenses, f, indent=4)

def generate_id():
    return str(uuid.uuid4())[:8]

def print_expense(expense):
    print(f"ID: {expense['id']} | Category: {expense['category']} | Amount: {expense['amount']} | Date: {expense['date']}")

# ========== Core Functionalities ==========

def add_expense():
    category = input("Enter category: ")
    try:
        amount = float(input("Enter amount: "))
    except ValueError:
        print("Invalid amount. Please enter a number.")
        return
    
    date_input = input("Enter date (YYYY-MM-DD) or press enter for today: ")
    try:
        date = date_input if date_input else datetime.today().strftime('%Y-%m-%d')
        # Validate date
        datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        print("Invalid date format.")
        return

    expense = {
    "id": len(expenses) + 1,
    "category": category,
    "amount": amount,
    "date": date
}

    expenses.append(expense)
    save_expenses()
    print("Expense added successfully!")

def show_expenses():
    # Ensure every expense has an 'id'
    for i, exp in enumerate(expenses, start=1):
        if 'id' not in exp:
            exp['id'] = i

    print("Your Expenses:")
    for exp in expenses:
        print_expense(exp)


def show_graph():
    if not expenses:
        print("No data to show graph.")
        return
    monthly_totals = {}
    for exp in expenses:
        month = exp['date'][:7]  # Extract YYYY-MM
        monthly_totals[month] = monthly_totals.get(month, 0) + exp['amount']
    
    months = sorted(monthly_totals.keys())
    totals = [monthly_totals[m] for m in months]

    plt.bar(months, totals)
    plt.xlabel('Month')
    plt.ylabel('Total Expense')
    plt.title('Monthly Expenses')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def delete_expense_by_id():
    print("Your Expenses:")
    for exp in expenses:
        print(f"ID: {exp['id']} | Category: {exp['category']} | Amount: {exp['amount']} | Date: {exp['date']}")

    try:
        delete_id = int(input("Enter ID of expense to delete: "))
        found = False
        for i, exp in enumerate(expenses):
            if exp["id"] == delete_id:
                del expenses[i]
                print("Expense deleted successfully.")
                found = True
                break
        if not found:
            print("No expense found with that ID.")
    except ValueError:
        print("Invalid input. Please enter a valid number.")



def filter_expenses():
    category = input("Enter category to filter (leave blank to skip): ")
    start_date = input("Enter start date (YYYY-MM-DD, leave blank to skip): ")
    end_date = input("Enter end date (YYYY-MM-DD, leave blank to skip): ")

    filtered = expenses
    if category:
        filtered = [exp for exp in filtered if exp['category'].lower() == category.lower()]
    if start_date:
        try:
            datetime.strptime(start_date, '%Y-%m-%d')
            filtered = [exp for exp in filtered if exp['date'] >= start_date]
        except ValueError:
            print("Invalid start date format.")
            return
    if end_date:
        try:
            datetime.strptime(end_date, '%Y-%m-%d')
            filtered = [exp for exp in filtered if exp['date'] <= end_date]
        except ValueError:
            print("Invalid end date format.")
            return

    if not filtered:
        print("No matching records.")
        return
    print("\n--- Filtered Expenses ---")
    for exp in filtered:
        print_expense(exp)

# ========== Main Program ==========

def main():
    load_expenses()
    while True:
        print("\n===== Personal Expense Tracker =====")
        print("1. Add Expense")
        print("2. Show Expenses")
        print("3. Show Monthly Graph")
        print("4. Delete Expense by ID")
        print("5. Filter Expenses")
        print("6. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            add_expense()
        elif choice == '2':
            show_expenses()
        elif choice == '3':
            show_graph()
        elif choice == '4':
            delete_expense_by_id()
        elif choice == '5':
            filter_expenses()
        elif choice == '6':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# ========== Run App ==========
if __name__ == "__main__":
    main()
