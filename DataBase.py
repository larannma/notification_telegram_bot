class DataBase:
    def __init__(self):
        self.data = {}
    
    def add_person(self, id):
        self.data[id] = {}
        self.data[id]["Notifications"] = {}

    def add_person_name(self, id, name):
        self.data[id]["name"] = name

    def add_person_notification(self, id, text, date, rate):
        self.data[id]["Notifications"]["text"] = text
        self.data[id]["Notifications"]["date"] = date
        self.data[id]["Notifications"]["rate"] = rate