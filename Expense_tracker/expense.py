import json
from datetime import datetime



expenses = load_expenses()



def add_expense():
    amount = float(input("Enter amount: "))
    category = input("Enter category: ")
    description = input("Enter description: ")
    date = datetime.now().strftime("%Y-%m-%d")  # Current date

    expense = {
        "amount": amount,
        "category": category,
        "description": description,
        "date": date
    }

    expenses.append(expense)
    save_expenses(expenses)  # Save to file

    
def load_expenses():
    try:
        with open("expenses.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_expenses(expenses):
    with open("expenses.json", "w") as f:
        json.dump(expenses, f, indent=4)



def show_expenses():
    for e in expenses:
        print(f"{e['date']} | {e['category']} | Rs.{e['amount']} | {e['description']}")


while True:
    print("\n1. Add Expense")
    print("2. Show Expenses")
    print("3. Exit")
    
    choice = input("Choose an option: ")

    if choice == "1":
        add_expense()
    elif choice == "2":
        show_expenses()
    elif choice == "3":
        break
    else:
        print("Invalid choice. Try again.")
