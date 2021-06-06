from datetime import date, datetime


class Round:
    def __init__(self, name, pairs, matches=[]):
        self.name = name
        self.start_date = date.today().strftime("%Y/%m/%d")
        self.start_hour = datetime.now().strftime("%H:%M:%S")
        self.end_date = None
        self.end_hour = None
        self.matches = matches if len(matches) != 0 else self.generate_matches(pairs)

    def generate_matches(self, pairs):
        return [([0.0, 0.0], players) for players in pairs]

    def end(self):
        self.end_date = date.today()
        self.end_hour = datetime.now().strftime("%H:%M:%S")

    def serialize(self):
        return {
            "name": self.name,
            "start_date": self.start_date,
            "start_hour": self.start_hour,
            "end_date": self.end_date,
            "end_hour": self.end_hour,
            "matches": [[match[0], [match[1][0].id, match[1][1].id]] for match in self.matches]
        }
