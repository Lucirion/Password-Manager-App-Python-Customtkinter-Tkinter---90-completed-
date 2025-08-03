

# entry_manager.py
class EntryManager:
    def __init__(self):
        self.entries = {}  # or load from file/database

    def update_entry(self, label, updated_data):
        self.entries[label] = updated_data
        print(f"Updated '{label}':", updated_data)
