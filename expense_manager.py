# expense_manager.py

class ExpenseManager:
    def __init__(self, data_handler):
        self.dh = data_handler
        self.data = self.dh.load_data()
        self.expenses = self.data.get("expenses", [])

    def save_changes(self):
        # Update the main data dictionary and save to file
        self.data["expenses"] = self.expenses
        self.dh.save_data(self.data)

    def add_expense(self, name, amount, category):
        self.expenses.append(
            {"name": name, "amount": amount, "category": category})
        self.save_changes()

    def delete_expense(self, index):
        if 0 <= index < len(self.expenses):
            self.expenses.pop(index)
            self.save_changes()

    def get_total(self):
        total = 0.0
        for item in self.expenses:
            total += item["amount"]
        return total

    def get_all_expenses(self):
        return self.expenses

    def get_expenses_by_category(self):
        # Aggregates totals per category for our dashboard chart
        category_totals = {}
        for item in self.expenses:
            cat = item["category"]
            if cat in category_totals:
                category_totals[cat] += item["amount"]
            else:
                category_totals[cat] = item["amount"]
        return category_totals
