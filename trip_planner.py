# trip_planner.py

class TripPlanner:
    def __init__(self, data_handler):
        self.dh = data_handler
        self.data = self.dh.load_data()
        self.costs = self.data.get("trip_costs", {})

    def save_changes(self):
        self.data["trip_costs"] = self.costs
        self.dh.save_data(self.data)

    def add_or_update_category(self, category, amount):
        self.costs[category] = amount
        self.save_changes()

    def remove_category(self, category):
        if category in self.costs:
            del self.costs[category]
            self.save_changes()

    def calculate_total(self):
        total = 0.0
        for key in self.costs:
            total += self.costs[key]
        return total

    def get_all_costs(self):
        return self.costs
