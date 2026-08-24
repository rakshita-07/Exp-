# data_handler.py
import json
import os


class DataHandler:
    def __init__(self, filename="pennywise_database.json"):
        self.filename = filename
        self.ensure_file_exists()

    def ensure_file_exists(self):
        # If the file doesn't exist yet, create it with empty templates
        if not os.path.exists(self.filename):
            initial_data = {
                "expenses": [],
                "trip_costs": {}
            }
            self.save_data(initial_data)

    def load_data(self):
        # Read the data from the file
        with open(self.filename, 'r') as file:
            return json.load(file)

    def save_data(self, data):
        # Write the updated data back to the file
        with open(self.filename, 'w') as file:
            json.dump(data, file, indent=4)
