from datetime import date, datetime


class Round:
    def __init__(self, name, pairs):
        self.name = name
        self.pairs = pairs
        self.start_date = date.today()
        self.start_hour = datetime.now().strftime("%H:%M:%S")
        self.end_date = None
        self.end_hour = None
        self.matches = self.generate_matches()

    def generate_matches(self):
        return [([0.0, 0.0], players) for players in self.pairs]

    def end(self):
        self.end_date = date.today()
        self.end_hour = datetime.now().strftime("%H:%M:%S")
