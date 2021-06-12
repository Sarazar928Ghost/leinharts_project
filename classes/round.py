from datetime import datetime


class Round:
    def __init__(self, name: str, pairs: list, matches: tuple = None) -> None:
        self.name = name
        self.start_date = datetime.now().strftime("%Y/%m/%d")
        self.start_hour = datetime.now().strftime("%H:%M:%S")
        self.end_date = None
        self.end_hour = None
        self.matches = matches if matches is not None else self.generate_matches(pairs)

    def generate_matches(self, pairs: list) -> tuple:
        return tuple([([players_id[0], 0.0], [players_id[1], 0.0]) for players_id in pairs])

    def end(self) -> None:
        self.end_date = datetime.now().strftime("%Y/%m/%d")
        self.end_hour = datetime.now().strftime("%H:%M:%S")

    def serialize(self) -> dict:
        return {
            "name": self.name,
            "start_date": self.start_date,
            "start_hour": self.start_hour,
            "end_date": self.end_date,
            "end_hour": self.end_hour,
            "matches": [[[match[0][0], match[0][1]], [match[1][0], match[1][1]]] for match in self.matches]
        }

    def __str__(self):
        return f"{self.name}, {self.start_date}, {self.start_hour}, {self.end_date}, {self.end_hour}"
